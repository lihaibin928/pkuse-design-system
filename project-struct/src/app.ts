// 运行时配置

export { request } from '@/utils/request';

// 全局初始化数据配置，用于 Layout 用户信息和权限初始化
// 更多信息见文档：https://umijs.org/docs/api/runtime-config#getinitialstate
export async function getInitialState(): Promise<App.InitialState> {
  return { name: '@umijs/max' };
}

export const layout = () => {
  const isDev = process.env.NODE_ENV === 'development';

  return {
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
