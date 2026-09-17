import { useCallback, useEffect, useState } from 'react';

import type { FormInstance } from 'antd';

import { DEFAULT_PAGINATION_PARAMS } from '@/features/shared/constants';
import { fetchUserList } from '../services';
import type { UserListInfo } from '../types';

function getValues(form: FormInstance) {
  return form.getFieldsValue();
}

interface UseUserListOptions {
  form: FormInstance;
}

const useUserList = (options: UseUserListOptions) => {
  const { form } = options;

  const [userListInfo, setUserListInfo] = useState<UserListInfo>();
  const [loading, setLoading] = useState(true);

  const fetchList = useCallback(
    async (
      params: { pageNo?: number; pageSize?: number } = {},
      withFormValues = true,
    ) => {
      setLoading(true);

      try {
        const values = withFormValues ? getValues(form) : {};
        const res = await fetchUserList({
          ...DEFAULT_PAGINATION_PARAMS,
          ...params,
          ...values,
        });

        setUserListInfo({
          list: res.list,
          total: res.total,
          pageNo:
            params.pageNo ?? res.pageNo ?? DEFAULT_PAGINATION_PARAMS.pageNo,
          pageSize:
            params.pageSize ??
            res.pageSize ??
            DEFAULT_PAGINATION_PARAMS.pageSize,
        });
      } finally {
        setLoading(false);
      }
    },
    [form],
  );

  useEffect(() => {
    fetchList({}, false);
  }, [fetchList]);

  const onPageChange = (pageNo: number, pageSize: number) => {
    fetchList({ pageNo, pageSize });
  };

  const onSearch = () => {
    fetchList({ pageNo: 1 });
  };

  return {
    loading,
    userListInfo,
    onPageChange,
    onSearch,
    refresh: fetchList,
  };
};

export default useUserList;
