import React from 'react';

import { PageContainer } from '@ant-design/pro-components';
import { Form } from 'antd';

import UserListWithModal from '@/features/user/components/UserListWithModal';
import UserSearchForm from '@/features/user/components/UserSearchForm';

import useUserList from '@/features/user/hooks/useUserList';

const UserList: React.FC = () => {
  const [form] = Form.useForm();

  const { loading, userListInfo, onPageChange, onSearch, refresh } =
    useUserList({
      form,
    });

  return (
    <PageContainer>
      <UserSearchForm onSearch={onSearch} form={form} />
      <UserListWithModal
        loading={loading}
        userListInfo={userListInfo}
        onPageChange={onPageChange}
        onRefresh={refresh}
      />
    </PageContainer>
  );
};

export default UserList;
