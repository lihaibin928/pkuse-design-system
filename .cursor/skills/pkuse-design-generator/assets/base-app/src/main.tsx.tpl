import {
  qiankunWindow,
  renderWithQiankun,
} from "vite-plugin-qiankun/dist/helper";
import {
  bootstrap,
  mount,
  render,
  unmount,
  update,
} from "./micro-app/adapter";
import "./styles/global.css";

export const appTitle = "__APP_TITLE__";

renderWithQiankun({ bootstrap, mount, unmount, update });

if (!qiankunWindow.__POWERED_BY_QIANKUN__) {
  render();
}

export { bootstrap, mount, unmount, update };
