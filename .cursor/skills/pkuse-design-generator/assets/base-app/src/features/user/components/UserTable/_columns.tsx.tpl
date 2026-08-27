import type { TableColumnsType } from 'antd';
import { Button, Space, Tag } from 'antd';
import { Access } from '@umijs/max';

import { User } from '../../types';

interface ColumnOptions {
  onEdit(record: User): void;
  onDetail(record: User): void;
  canEdit: boolean;
}

export function buildUserColumns(
  options: ColumnOptions,
): TableColumnsType<User> {
  return [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80,
    },
    {
      title: '姓名',
      dataIndex: 'name',
    },
    {
      title: '角色',
      dataIndex: 'role',
      render: (role: string) => (role === 'admin' ? '管理员' : '普通用户'),
    },
    {
      title: '状态',
      dataIndex: 'status',
      render: (v: number) => (
        <Tag color={v === 1 ? 'green' : 'default'}>
          {v === 1 ? '启用' : '停用'}
        </Tag>
      ),
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
    },
    {
      title: '操作',
      width: 160,
      render: (_, record) => (
        <Space>
          <Access accessible={options.canEdit}>
            <Button type="link" onClick={() => options.onEdit(record)}>
              编辑
            </Button>
          </Access>
          <Button type="link" onClick={() => options.onDetail(record)}>
            查看
          </Button>
        </Space>
      ),
    },
  ];
}
