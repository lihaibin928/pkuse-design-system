import React from 'react';

import { useAccess } from '@umijs/max';
import { Empty, Table } from 'antd';

import { DEFAULT_PAGINATION_PARAMS } from '@/features/shared/constants';
import { User, UserListInfo } from '@/features/user/types';
import { buildUserColumns } from './_columns';

interface UserTableProps {
  userListInfo?: UserListInfo;
  loading?: boolean;
  onPageChange: (pageNo: number, pageSize: number) => void;
  onEdit: (record: User) => void;
  onDetail: (record: User) => void;
}

const UserTable: React.FC<UserTableProps> = (props) => {
  const { userListInfo = {}, loading, onPageChange, onEdit, onDetail } = props;
  const access = useAccess();

  const columns = buildUserColumns({
    onEdit,
    onDetail,
    canEdit: access.canEditUser,
  });

  return (
    <Table
      rowKey="id"
      columns={columns}
      dataSource={userListInfo?.list}
      loading={loading}
      locale={{ emptyText: <Empty description="暂无数据" /> }}
      pagination={{
        current: userListInfo.pageNo || DEFAULT_PAGINATION_PARAMS.pageNo,
        pageSize: userListInfo.pageSize || DEFAULT_PAGINATION_PARAMS.pageSize,
        total: userListInfo.total,
        onChange: onPageChange,
        showSizeChanger: true,
      }}
    />
  );
};

export default UserTable;
