export function can(
  permissions: readonly string[],
  required?: string,
): boolean {
  return required === undefined || permissions.includes(required);
}
