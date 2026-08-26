import type {
  Entity,
  EntityService,
  ServiceResult,
} from "../services/contracts";

const entities: Entity[] = [
  { id: "PK-001", name: "示例业务对象", status: "active" },
  { id: "PK-002", name: "待处理对象", status: "paused" },
];

export class MockEntityService implements EntityService<Entity> {
  async list(signal?: AbortSignal): Promise<ServiceResult<Entity[]>> {
    signal?.throwIfAborted();
    return { data: entities.map((item) => ({ ...item })), requestId: "mock-list" };
  }

  async get(
    id: string,
    signal?: AbortSignal,
  ): Promise<ServiceResult<Entity>> {
    signal?.throwIfAborted();
    const entity = entities.find((item) => item.id === id);
    if (!entity) {
      throw new Error(`Mock handler has no entity for id "${id}"`);
    }
    return { data: { ...entity }, requestId: `mock-${id}` };
  }
}
