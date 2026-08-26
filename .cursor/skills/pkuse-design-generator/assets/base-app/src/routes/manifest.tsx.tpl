import type { ReactNode } from "react";
import { can } from "../auth/access";
import {
  PERMISSIONS,
  type Permission,
} from "../auth/permissions";
import { DesignPreview } from "../app/DesignPreview";
import { HomePage } from "../features/home/HomePage";
import type { UserIdentity } from "../micro-app/contracts";
import type { Entity, EntityService } from "../services/contracts";

export interface AppRoute {
  path: string;
  title: string;
  permissions: readonly Permission[];
  menu?: {
    order: number;
  };
  element: ReactNode;
}

interface RouteContext {
  service: EntityService<Entity>;
  user?: UserIdentity;
}

export function createRouteManifest({
  service,
  user,
}: RouteContext): AppRoute[] {
  return [
    {
      path: "/",
      title: "业务概览",
      permissions: [PERMISSIONS.HOME_VIEW],
      menu: { order: 10 },
      element: <HomePage service={service} user={user} />,
    },
    {
      path: "/design-system",
      title: "设计规范",
      permissions: [PERMISSIONS.HOME_VIEW],
      menu: { order: 90 },
      element: <DesignPreview />,
    },
  ];
}

export function canAccessRoute(
  route: AppRoute,
  permissions: readonly string[],
): boolean {
  return route.permissions.every((permission) => can(permissions, permission));
}

export function buildVisibleMenu(
  manifest: readonly AppRoute[],
  permissions: readonly string[],
): Array<Pick<AppRoute, "path" | "title">> {
  return manifest
    .filter((route) => route.menu && canAccessRoute(route, permissions))
    .sort((left, right) => (left.menu?.order ?? 0) - (right.menu?.order ?? 0))
    .map(({ path, title }) => ({ path, title }));
}
