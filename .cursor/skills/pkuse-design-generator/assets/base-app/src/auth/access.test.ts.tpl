import { describe, expect, it } from "vitest";
import { can } from "./access";

describe("can", () => {
  it("allows a request without a required permission", () => {
    expect(can([], undefined)).toBe(true);
  });

  it("checks the required permission", () => {
    expect(can(["entity:view"], "entity:view")).toBe(true);
    expect(can(["entity:view"], "entity:edit")).toBe(false);
  });
});
