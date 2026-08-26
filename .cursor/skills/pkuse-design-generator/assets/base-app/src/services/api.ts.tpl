import {
  createRequestController,
  releaseRequestController,
} from "../micro-app/cleanup";
import type {
  Entity,
  EntityService,
  ServiceResult,
} from "./contracts";
import {
  BusinessError,
  ForbiddenError,
  NetworkError,
  NotFoundError,
  ProtocolError,
  ServerError,
  ServiceError,
  UnauthorizedError,
} from "./errors";

async function readErrorMessage(response: Response): Promise<string | undefined> {
  try {
    const body = (await response.json()) as { message?: unknown };
    return typeof body.message === "string" ? body.message : undefined;
  } catch {
    return undefined;
  }
}

export async function mapHttpError(response: Response): Promise<ServiceError> {
  const requestId = response.headers.get("x-request-id") ?? undefined;
  const message = await readErrorMessage(response);
  switch (response.status) {
    case 401:
      return new UnauthorizedError(message, requestId);
    case 403:
      return new ForbiddenError(message, requestId);
    case 404:
      return new NotFoundError(message, requestId);
    default:
      if (response.status >= 500) {
        return new ServerError(message, response.status, requestId);
      }
      return new BusinessError(message, response.status, requestId);
  }
}

export function mapNetworkError(error: unknown): NetworkError {
  return new NetworkError("无法连接到服务，请检查网络后重试", {
    cause: error,
  });
}

export class ApiEntityService implements EntityService<Entity> {
  constructor(
    private readonly authToken?: string,
    private readonly onUnauthorized?: () => void,
  ) {}

  list(signal?: AbortSignal): Promise<ServiceResult<Entity[]>> {
    return this.request<Entity[]>("/api/entities", signal);
  }

  get(id: string, signal?: AbortSignal): Promise<ServiceResult<Entity>> {
    return this.request<Entity>(`/api/entities/${encodeURIComponent(id)}`, signal);
  }

  private async request<T>(
    path: string,
    externalSignal?: AbortSignal,
  ): Promise<ServiceResult<T>> {
    const controller = createRequestController();
    const abort = () => controller.abort();
    externalSignal?.addEventListener("abort", abort, { once: true });
    try {
      let response: Response;
      try {
        response = await fetch(path, {
          signal: controller.signal,
          headers: this.authToken
            ? { Authorization: `Bearer ${this.authToken}` }
            : undefined,
        });
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          throw error;
        }
        throw mapNetworkError(error);
      }
      const requestId = response.headers.get("x-request-id") ?? "unknown";
      if (!response.ok) {
        const error = await mapHttpError(response);
        if (error instanceof UnauthorizedError) this.onUnauthorized?.();
        throw error;
      }
      let data: T;
      try {
        data = (await response.json()) as T;
      } catch (error) {
        throw new ProtocolError(
          "服务返回的 JSON 无法解析",
          requestId,
        );
      }
      if (data === null || data === undefined) {
        throw new ProtocolError("服务返回了空 JSON", requestId);
      }
      return { data, requestId };
    } finally {
      externalSignal?.removeEventListener("abort", abort);
      releaseRequestController(controller);
    }
  }
}
