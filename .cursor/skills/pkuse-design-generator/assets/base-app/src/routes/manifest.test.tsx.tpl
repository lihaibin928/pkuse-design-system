import { describe, expect, it, vi } from "vitest";
import { PERMISSIONS } from "../auth/permissions";
import type { UserIdentity } from "../micro-app/contracts";
import type { Entity, EntityService } from "../services/contracts";
import {
  buildVisibleMenu,
  createRouteManifest,
} from "./manifest";

const service = {
  list: vi.fn(),
  get: vi.fn(),
} as unknown as EntityService<Entity>;

const user: UserIdentity = {
  id: "viewer",
  displayName: "Viewer",
  roles: ["viewer"],
  permissions: [PERMISSIONS.HOME_VIEW],
};

describe("route manifest", () => {
  it("uses HOME_VIEW for the home route and menu", () => {
    const manifest = createRouteManifest({ service, user });

    expect(manifest[0].permissions).toEqual([PERMISSIONS.HOME_VIEW]);
    expect(buildVisibleMenu(manifest, user.permissions)).toEqual([
      expect.objectContaining({ path: "/", title: "业务概览" }),
      expect.objectContaining({ path: "/design-system", title: "设计规范" }),
    ]);
    expect(buildVisibleMenu(manifest, [])).toEqual([]);
  });

  it("keeps route, entity and action permissions independent", () => {
    expect(PERMISSIONS.HOME_VIEW).not.toBe(PERMISSIONS.ENTITY_VIEW);
    expect(PERMISSIONS.ENTITY_VIEW).not.toBe(PERMISSIONS.ENTITY_EDIT);
  });
});
