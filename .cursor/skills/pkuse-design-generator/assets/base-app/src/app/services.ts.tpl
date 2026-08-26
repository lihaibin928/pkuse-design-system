import { MockEntityService } from "../mocks/entity.mock";
import { ApiEntityService } from "../services/api";
import type { AppServices } from "../services/contracts";
import type { MicroAppProps } from "../micro-app/contracts";

export type ServiceMode = "mock" | "api";

export function createServices(
  mode: ServiceMode,
  props: MicroAppProps = {},
): AppServices {
  return {
    entities:
      mode === "mock"
        ? new MockEntityService()
        : new ApiEntityService(props.authToken, () => props.navigate?.("/login")),
  };
}
