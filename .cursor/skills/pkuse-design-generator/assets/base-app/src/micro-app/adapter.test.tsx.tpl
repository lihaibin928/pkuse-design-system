import { beforeEach, describe, expect, it, vi } from "vitest";
import {
  createRequestController,
  registerCleanup,
} from "./cleanup";

const mocks = vi.hoisted(() => ({
  roots: [] as Array<{
    render: ReturnType<typeof vi.fn>;
    unmount: ReturnType<typeof vi.fn>;
  }>,
  renderFailure: false,
  onRender: undefined as (() => void) | undefined,
}));

vi.mock("react-dom/client", () => ({
  createRoot: vi.fn(() => {
    const root = {
      render: vi.fn(() => {
        mocks.onRender?.();
        if (mocks.renderFailure) throw new Error("render failed");
      }),
      unmount: vi.fn(),
    };
    mocks.roots.push(root);
    return root;
  }),
}));

vi.mock("../app/App", () => ({ App: () => null }));
vi.mock("../mocks/roles", () => ({
  LOCAL_USERS: {
    admin: {
      id: "admin",
      displayName: "Admin",
      roles: ["admin"],
      permissions: [],
    },
  },
}));

import { mount, unmount } from "./adapter";
import type { MicroAppProps } from "./contracts";

const container = {
  querySelector: vi.fn(() => ({ nodeType: 1 })),
} as unknown as Element;

describe("micro-app lifecycle", () => {
  beforeEach(async () => {
    await unmount();
    mocks.roots.length = 0;
    mocks.renderFailure = false;
    mocks.onRender = undefined;
    vi.clearAllMocks();
  });

  it("cleans the previous instance before a repeated mount", async () => {
    const firstOff = vi.fn(() => true);
    const secondOff = vi.fn(() => true);

    await mount({ container, offGlobalStateChange: firstOff });
    await mount({ container, offGlobalStateChange: secondOff });

    expect(mocks.roots).toHaveLength(2);
    expect(mocks.roots[0].unmount).toHaveBeenCalledOnce();
    expect(firstOff).toHaveBeenCalledOnce();
    expect(secondOff).not.toHaveBeenCalled();
  });

  it("rolls back subscriptions, roots, requests and resources on render failure", async () => {
    const onGlobalStateChange = vi.fn();
    const offGlobalStateChange = vi.fn(() => true);
    const cleanup = vi.fn();
    let request: AbortController | undefined;
    mocks.onRender = () => {
      request = createRequestController();
      registerCleanup(cleanup);
    };
    mocks.renderFailure = true;

    await expect(
      mount({
        container,
        onGlobalStateChange,
        offGlobalStateChange,
      } as MicroAppProps),
    ).rejects.toThrow("render failed");

    expect(mocks.roots[0].unmount).toHaveBeenCalledOnce();
    expect(onGlobalStateChange).toHaveBeenCalledOnce();
    expect(offGlobalStateChange).toHaveBeenCalledOnce();
    expect(request?.signal.aborted).toBe(true);
    expect(cleanup).toHaveBeenCalledOnce();
  });
});
