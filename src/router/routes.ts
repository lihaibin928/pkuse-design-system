export default [
  {
    path: '/',
    redirect: '/home',
  },
  {
    name: '首页',
    path: '/home',
    component: './Home',
    icon: 'HomeOutlined',
  },
  {
    name: '权限演示',
    path: '/access',
    component: './Access',
    icon: 'SettingOutlined',
  },
  {
    name: '订单列表',
    path: '/order/list',
    component: './Order/OrderList',
    icon: 'ShoppingCartOutlined',
  },
  {
    name: '用户列表',
    path: '/user/list',
    component: './User/UserList',
    icon: 'UserOutlined',
  },
  {
    name: '用户详情',
    path: '/user/detail',
    component: './User/UserDetail',
    hideInMenu: true,
    icon: 'IdcardOutlined',
  },
];
