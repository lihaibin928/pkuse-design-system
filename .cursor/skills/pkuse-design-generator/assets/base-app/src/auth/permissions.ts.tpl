export const PERMISSIONS = {
  HOME_VIEW: "home:view",
  ENTITY_VIEW: "entity:view",
  ENTITY_EDIT: "entity:edit",
} as const;

export type Permission = (typeof PERMISSIONS)[keyof typeof PERMISSIONS];
