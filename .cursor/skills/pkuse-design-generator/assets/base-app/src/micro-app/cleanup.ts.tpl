const requests = new Set<AbortController>();
const cleanups = new Set<() => void>();

export function createRequestController(): AbortController {
  const controller = new AbortController();
  requests.add(controller);
  controller.signal.addEventListener(
    "abort",
    () => requests.delete(controller),
    { once: true },
  );
  return controller;
}

export function releaseRequestController(controller: AbortController): void {
  requests.delete(controller);
}

export function registerCleanup(cleanup: () => void): () => void {
  cleanups.add(cleanup);
  return () => cleanups.delete(cleanup);
}

export function registerWindowListener<K extends keyof WindowEventMap>(
  type: K,
  listener: (event: WindowEventMap[K]) => void,
): () => void {
  const wrapped = listener as EventListener;
  window.addEventListener(type, wrapped);
  return registerCleanup(() => window.removeEventListener(type, wrapped));
}

export function registerTimeout(
  callback: () => void,
  delay: number,
): number {
  const id = window.setTimeout(() => {
    cleanups.delete(cancel);
    callback();
  }, delay);
  const cancel = () => window.clearTimeout(id);
  registerCleanup(cancel);
  return id;
}

export function abortAllRequests(): void {
  for (const controller of requests) controller.abort();
  requests.clear();
}

export function clearAllResources(): void {
  for (const cleanup of cleanups) cleanup();
  cleanups.clear();
}
