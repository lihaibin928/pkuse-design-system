import { useCallback, useEffect, useState } from 'react';

import type { FormInstance } from 'antd';

import { DEFAULT_PAGINATION_PARAMS } from '@/features/shared/constants';
import { fetchOrderList } from '../services';
import type { OrderListInfo } from '../types';

function getValues(form: FormInstance) {
  return form.getFieldsValue();
}

interface UseOrderListOptions {
  form: FormInstance;
}

const useOrderList = (options: UseOrderListOptions) => {
  const { form } = options;

  const [orderListInfo, setOrderListInfo] = useState<OrderListInfo>();
  const [loading, setLoading] = useState(true);

  const fetchList = useCallback(
    async (
      params: { pageNo?: number; pageSize?: number } = {},
      withFormValues = true,
    ) => {
      setLoading(true);

      try {
        const values = withFormValues ? getValues(form) : {};
        const res = await fetchOrderList({
          ...DEFAULT_PAGINATION_PARAMS,
          ...params,
          ...values,
        });

        setOrderListInfo({
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
    orderListInfo,
    onPageChange,
    onSearch,
    refresh: fetchList,
  };
};

export default useOrderList;
