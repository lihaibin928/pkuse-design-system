export interface ServiceResult<T> {
  data: T;
  requestId: string;
}

export interface Entity {
  id: string;
  name: string;
  status: "active" | "paused";
}

export interface EntityService<T> {
  list(signal?: AbortSignal): Promise<ServiceResult<T[]>>;
  get(id: string, signal?: AbortSignal): Promise<ServiceResult<T>>;
}

export interface AppServices {
  entities: EntityService<Entity>;
}
