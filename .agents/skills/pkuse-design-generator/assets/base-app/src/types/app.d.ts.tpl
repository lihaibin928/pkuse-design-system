/** The global namespace for the app */
declare namespace App {
  interface UserIdentity {
    id: string;
    displayName: string;
    roles: string[];
    permissions: string[];
  }

  /** 全局初始化状态，与 getInitialState / access 共用 */
  interface InitialState {
    name: string;
    user?: UserIdentity;
    authToken?: string;
  }

  /** Theme namespace */
  namespace Theme {}

  /** Global namespace */
  namespace Global {}
}
