import React from 'react';

import { PageContainer } from '@ant-design/pro-components';
import { useModel } from '@umijs/max';

import Guide from '@/components/Guide';

const Home: React.FC = () => {
  const {
    initialState: { name },
  } = useModel('@@initialState');
  return (
    <PageContainer ghost>
      <div className="pt-[80px]">
        <Guide name={name} />
      </div>
    </PageContainer>
  );
};

export default Home;
