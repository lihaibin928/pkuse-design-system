import React from 'react';

import { PageContainer } from '@ant-design/pro-components';
import { Result, Spin } from 'antd';
import { useSearchParams } from 'umi';

import UserDetailCard from '@/features/user/components/UserDetailCard';
import useUserDetail from '@/features/user/hooks/useUserDetail';

const UserDetail: React.FC = () => {
  const [params] = useSearchParams();
  const id = Number(params.get('id'));

  const { loading, userDetailInfo } = useUserDetail(id);

  if (!id) {
    return <Result status="404" title="用户不存在" />;
  }

  if (!loading && !userDetailInfo) {
    return <Result status="404" title="用户不存在" />;
  }

  return (
    <Spin spinning={loading}>
      <PageContainer>
        <UserDetailCard userDetailInfo={userDetailInfo} />
      </PageContainer>
    </Spin>
  );
};

export default UserDetail;
