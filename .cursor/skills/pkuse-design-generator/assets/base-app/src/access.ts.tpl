export default (initialState: App.InitialState) => {
  const permissions = new Set(initialState?.user?.permissions ?? []);
  const standaloneAdmin = !initialState?.user;

  const has = (code: string) => standaloneAdmin || permissions.has(code);

  return {
    canSeeAdmin: has('admin:view'),
    canViewUser: has('user:view'),
    canEditUser: has('user:edit'),
    canViewOrder: has('order:view'),
  };
};
