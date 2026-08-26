import { createRoot, type Root } from "react-dom/client";
import { App } from "../app/App";
import { LOCAL_USERS } from "../mocks/roles";
import { abortAllRequests, clearAllResources } from "./cleanup";
import type { MicroAppProps } from "./contracts";

let root: Root | undefined;
let activeProps: MicroAppProps | undefined;
let globalState: Record<string, unknown> = {};

function callSafely(action: (() => unknown) | undefined): void {
  try {
    action?.();
  } catch (error) {
    console.error("[__APP_NAME__] lifecycle cleanup failed", error);
  }
}

function disposeResources(
  props: MicroAppProps | undefined,
  mountedRoot: Root | undefined,
): void {
  callSafely(abortAllRequests);
  callSafely(clearAllResources);
  callSafely(() => props?.offGlobalStateChange?.());
  callSafely(() => mountedRoot?.unmount());
  globalState = {};
}

function disposeCurrent(): void {
  const props = activeProps;
  const mountedRoot = root;
  activeProps = undefined;
  root = undefined;
  disposeResources(props, mountedRoot);
}

function getMountElement(props: MicroAppProps): Element {
  const element = props.container
    ? props.container.querySelector("[data-pkuse-root='__APP_NAME__']")
    : document.querySelector("[data-pkuse-root='__APP_NAME__']");
  if (!element) {
    throw new Error("Mount element not found for __APP_NAME__");
  }
  return element;
}

export function render(props: MicroAppProps = {}): void {
  disposeCurrent();
  const standalone = props.container === undefined;
  const nextProps = standalone
    ? { ...props, user: props.user ?? LOCAL_USERS.admin }
    : props;
  let nextRoot: Root | undefined;
  let subscriptionStarted = false;

  try {
    const mountElement = getMountElement(props);
    subscriptionStarted = Boolean(nextProps.onGlobalStateChange);
    nextProps.onGlobalStateChange?.((state) => {
      globalState = state;
    }, true);
    nextRoot = createRoot(mountElement);
    nextRoot.render(
      <App
        props={nextProps}
        title="__APP_TITLE__"
        standalone={standalone}
      />,
    );
    activeProps = nextProps;
    root = nextRoot;
  } catch (error) {
    disposeResources(
      subscriptionStarted ? nextProps : undefined,
      nextRoot,
    );
    throw error;
  }
}

export async function bootstrap(): Promise<void> {
  globalState = {};
}

export async function mount(props: MicroAppProps): Promise<void> {
  render(props);
}

export async function unmount(): Promise<void> {
  disposeCurrent();
}

export async function update(props: MicroAppProps): Promise<void> {
  await unmount();
  render(props);
}
