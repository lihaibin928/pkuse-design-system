declare namespace Api {
  /** 接口通用返回结构 */
  interface Response<T = undefined> {
    code: number;
    message?: string;
    msg?: string;
    data: T;
    success?: boolean;
  }
}
