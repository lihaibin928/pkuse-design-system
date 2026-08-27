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
    access: 'canSeeAdmin',
  },
  {
    name: '订单列表',
    path: '/order/list',
    component: './Order/OrderList',
    icon: 'ShoppingCartOutlined',
    access: 'canViewOrder',
  },
  {
    name: '用户列表',
    path: '/user/list',
    component: './User/UserList',
    icon: 'UserOutlined',
    access: 'canViewUser',
  },
  {
    name: '用户详情',
    path: '/user/detail',
    component: './User/UserDetail',
    hideInMenu: true,
    icon: 'IdcardOutlined',
    access: 'canViewUser',
  },
  {
    name: '设计系统',
    path: '/design-system',
    component: './DesignSystem',
    hideInMenu: true,
  },
];
