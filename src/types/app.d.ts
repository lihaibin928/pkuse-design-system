/** The global namespace for the app */
declare namespace App {
  /** 全局初始化状态，与 getInitialState / access 共用 */
  interface InitialState {
    name: string;
  }

  /** Theme namespace */
  namespace Theme {}

  /** Global namespace */
  namespace Global {}
}
