import { PERMISSIONS } from "../auth/permissions";
import type { UserIdentity } from "../micro-app/contracts";

export const LOCAL_USERS = {
  admin: {
    id: "local-admin",
    displayName: "本地管理员",
    roles: ["admin"],
    permissions: Object.values(PERMISSIONS),
  },
  viewer: {
    id: "local-viewer",
    displayName: "只读访客",
    roles: ["viewer"],
    permissions: [PERMISSIONS.HOME_VIEW, PERMISSIONS.ENTITY_VIEW],
  },
} satisfies Record<string, UserIdentity>;
