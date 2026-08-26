import { afterEach, describe, expect, it, vi } from "vitest";
import {
  BusinessError,
  ForbiddenError,
  NetworkError,
  NotFoundError,
  ProtocolError,
  ServerError,
  UnauthorizedError,
} from "./errors";
import {
  ApiEntityService,
  mapHttpError,
  mapNetworkError,
} from "./api";

describe("API error mapping", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it.each([
    [401, UnauthorizedError],
    [403, ForbiddenError],
    [404, NotFoundError],
    [500, ServerError],
    [503, ServerError],
    [422, BusinessError],
  ])("maps HTTP %s to a typed error", async (status, ErrorType) => {
    const response = new Response(JSON.stringify({ message: "detail" }), {
      status,
      headers: {
        "content-type": "application/json",
        "x-request-id": "request-1",
      },
    });

    const error = await mapHttpError(response);

    expect(error).toBeInstanceOf(ErrorType);
    expect(error.requestId).toBe("request-1");
  });

  it("maps fetch failures to NetworkError", () => {
    expect(mapNetworkError(new TypeError("fetch failed"))).toBeInstanceOf(
      NetworkError,
    );
  });

  it("maps a fetch rejection to NetworkError at the adapter boundary", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("offline")));

    await expect(new ApiEntityService().list()).rejects.toBeInstanceOf(
      NetworkError,
    );
  });

  it.each([
    new Response(null, { status: 204 }),
    new Response("not-json", {
      status: 200,
      headers: { "content-type": "application/json" },
    }),
  ])("maps an invalid 2xx payload to ProtocolError", async (response) => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response));

    await expect(new ApiEntityService().list()).rejects.toBeInstanceOf(
      ProtocolError,
    );
  });
});
