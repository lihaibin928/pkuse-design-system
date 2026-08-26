import { defineConfig } from '@umijs/max';

import routes from './src/router/routes';

export default defineConfig({
  title: 'temp',
  layout: {
    title: '@umijs/max',
  },
  hash: true,
  antd: {},
  access: {},
  model: {},
  initialState: {},
  request: {},
  mock: {},
  routes,
  npmClient: 'yarn',
  tailwindcss: {},
  proxy: {},
});
