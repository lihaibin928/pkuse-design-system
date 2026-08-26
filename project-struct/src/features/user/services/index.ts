import { request } from '@umijs/max';

import { User, UserListInfo, UserListQuery } from '../types';

export async function fetchUserList(
  params: UserListQuery,
): Promise<UserListInfo> {
  const res = await request<Api.Response<UserListInfo>>('/api/users', {
    method: 'GET',
    params,
  });

  return res.data;
}

export async function fetchUserDetail(id: number): Promise<User> {
  const res = await request<Api.Response<User>>(`/api/users/${id}`, {
    method: 'GET',
  });

  return res.data;
}

export async function updateUser(payload: Partial<User>) {
  if (payload.id) {
    const res = await request<Api.Response<User>>(`/api/users/${payload.id}`, {
      method: 'PUT',
      data: payload,
    });

    return res.data;
  }

  const res = await request<Api.Response<User>>('/api/users', {
    method: 'POST',
    data: payload,
  });

  return res.data;
}
