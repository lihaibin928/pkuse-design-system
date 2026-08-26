export class ServiceError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly requestId?: string,
    readonly retryable = false,
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = new.target.name;
  }
}

export class UnauthorizedError extends ServiceError {
  constructor(message = "登录状态已失效", requestId?: string) {
    super(message, 401, requestId);
  }
}

export class ForbiddenError extends ServiceError {
  constructor(message = "无权执行此操作", requestId?: string) {
    super(message, 403, requestId);
  }
}

export class NotFoundError extends ServiceError {
  constructor(message = "请求的资源不存在", requestId?: string) {
    super(message, 404, requestId);
  }
}

export class ServerError extends ServiceError {
  constructor(
    message = "服务暂时不可用",
    status = 500,
    requestId?: string,
  ) {
    super(message, status, requestId, true);
  }
}

export class NetworkError extends ServiceError {
  constructor(message = "网络连接失败", options?: ErrorOptions) {
    super(message, 0, undefined, true, options);
  }
}

export class ProtocolError extends ServiceError {
  constructor(message = "服务返回了无法解析的数据", requestId?: string) {
    super(message, 502, requestId, true);
  }
}

export class BusinessError extends ServiceError {
  constructor(
    message = "请求未通过业务校验",
    status = 422,
    requestId?: string,
  ) {
    super(message, status, requestId);
  }
}
