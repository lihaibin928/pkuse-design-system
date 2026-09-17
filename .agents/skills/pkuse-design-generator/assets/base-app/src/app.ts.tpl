// 运行时配置

export { request } from '@/utils/request';

type QiankunProps = {
  container?: Element;
  user?: App.UserIdentity;
  authToken?: string;
};

let qiankunProps: QiankunProps = {};

export const qiankun = {
  async bootstrap() {},
  async mount(props: QiankunProps = {}) {
    qiankunProps = props;
  },
  async update(props: QiankunProps = {}) {
    qiankunProps = props;
  },
  async unmount() {
    qiankunProps = {};
  },
};

export async function getInitialState(): Promise<App.InitialState> {
  return {
    name: qiankunProps.user?.displayName || '__APP_TITLE__',
    user: qiankunProps.user,
    authToken: qiankunProps.authToken,
  };
}

export const layout = () => {
  const isDev = process.env.NODE_ENV === 'development';

  return {
    title: '__APP_TITLE__',
    logo: 'https://img.alicdn.com/tfs/TB1YHEpwUT1gK0jSZFhXXaAtVXa-28-27.svg',
    menu: {
      locale: false,
    },
    // 仅开发环境渲染侧边菜单；生产环境由主应用导航，子应用不再重复渲染
    ...(isDev
      ? {}
      : {
          menuRender: false,
          menuHeaderRender: false,
        }),
  };
};
