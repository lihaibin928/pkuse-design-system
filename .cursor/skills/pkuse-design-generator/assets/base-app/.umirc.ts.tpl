import { defineConfig } from '@umijs/max';

import routes from './src/router/routes';

export default defineConfig({
  title: '__APP_TITLE__',
  layout: {
    title: '__APP_TITLE__',
  },
  hash: true,
  antd: {
    // antd 6 走 CSS-in-JS，不要再抽 antd 5 的 less 主题
    style: 'css',
    appConfig: {},
  },
  access: {},
  model: {},
  initialState: {},
  request: {},
  mock: {},
  qiankun: {
    slave: {},
  },
  routes,
  npmClient: 'yarn',
  tailwindcss: {},
  proxy: {},
  esbuildMinifyIIFE: true,
});
