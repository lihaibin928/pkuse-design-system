export interface UserIdentity {
  id: string;
  displayName: string;
  roles: string[];
  permissions: string[];
}

export interface GlobalStateActions {
  onGlobalStateChange?: (
    listener: (
      state: Record<string, unknown>,
      previous: Record<string, unknown>,
    ) => void,
    fireImmediately?: boolean,
  ) => void;
  setGlobalState?: (state: Record<string, unknown>) => boolean;
  offGlobalStateChange?: () => boolean;
}

export interface MicroAppProps extends GlobalStateActions {
  container?: Element | ShadowRoot;
  routeBase?: string;
  user?: UserIdentity;
  authToken?: string;
  navigate?: (path: string) => void;
}
