import { message } from 'antd';
import { history, RequestConfig } from 'umi';

const SUCCESS_CODES = new Set([0, 200]);
const LOGIN_PATH = '/login';
const SESSION_EXPIRED_CODE = 100000;

const HTTP_STATUS_MESSAGE: Record<number, string> = {
  400: '请求参数错误',
  401: '登录已失效，请重新登录',
  403: '暂无访问权限',
  404: '资源不存在',
  406: '请求格式错误',
  410: '资源不存在',
  422: '数据校验失败',
  500: '服务异常，请稍后重试',
  502: '服务异常，请稍后重试',
  503: '服务暂不可用，请稍后重试',
  504: '请求超时，请稍后重试',
};

class BizError extends Error {
  info: Api.Response;

  constructor(info: Api.Response) {
    super(getBizErrorMessage(info));
    this.name = 'BizError';
    this.info = info;
  }
}

function getBizErrorMessage(data: Api.Response): string {
  return data.message || data.msg || '请求失败，请稍后重试';
}

function isBizSuccess(data: Api.Response): boolean {
  if (data.success === false) return false;
  if (data.success === true) return true;
  return SUCCESS_CODES.has(data.code);
}

function isBizResponse(data: unknown): data is Api.Response {
  return (
    typeof data === 'object' &&
    data !== null &&
    'code' in data &&
    typeof (data as Api.Response).code === 'number'
  );
}

function redirectToLogin() {
  if (history.location.pathname !== LOGIN_PATH) {
    history.push(LOGIN_PATH);
  }
}

function throwBizErrorIfNeeded(data: Api.Response) {
  if (isBizSuccess(data)) return;

  if (data.code === SESSION_EXPIRED_CODE) {
    redirectToLogin();
  }

  throw new BizError(data);
}

function getHttpErrorMessage(
  status: number,
  statusText?: string,
  data?: unknown,
) {
  if (isBizResponse(data)) {
    const bizMessage = getBizErrorMessage(data);
    if (bizMessage !== '请求失败，请稍后重试') {
      return bizMessage;
    }
  }

  return HTTP_STATUS_MESSAGE[status] || statusText || '操作失败，请稍后重试';
}

export const request: RequestConfig = {
  credentials: 'include',

  errorConfig: {
    // Umi 在 success === false 时自动调用
    errorThrower(res) {
      throwBizErrorIfNeeded(res as Api.Response);
    },

    errorHandler(error, opts) {
      if (opts?.skipErrorHandler) return;

      if (error instanceof BizError) {
        message.error(error.message);
        return;
      }

      if (error.response) {
        const { status, statusText, data } = error.response;
        message.error(getHttpErrorMessage(status, statusText, data));

        if (status === 401) {
          redirectToLogin();
        }
        return;
      }

      if (error.request) {
        message.error('网络异常，请检查网络后重试');
        return;
      }

      message.error(error.message || '请求异常，请稍后重试');
    },
  },

  responseInterceptors: [
    (response) => {
      const { data } = response;

      // 兼容未返回 success 字段、仅通过 code 表示成败的接口
      if (isBizResponse(data) && data.success !== false) {
        throwBizErrorIfNeeded(data);
      }

      return response;
    },
  ],
};
