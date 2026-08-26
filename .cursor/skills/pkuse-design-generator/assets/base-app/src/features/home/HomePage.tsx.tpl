import { Button, Empty, Result, Space, Spin, Table, Tag, Typography } from "antd";
import { useCallback, useEffect, useState } from "react";
import { can } from "../../auth/access";
import { PERMISSIONS } from "../../auth/permissions";
import type { UserIdentity } from "../../micro-app/contracts";
import type { Entity, EntityService } from "../../services/contracts";
import {
  BusinessError,
  ForbiddenError,
  NetworkError,
  NotFoundError,
  ProtocolError,
  ServerError,
  ServiceError,
  UnauthorizedError,
} from "../../services/errors";

type ViewState = "loading" | "ready" | "empty" | "error" | "forbidden";

interface HomePageProps {
  service: EntityService<Entity>;
  user?: UserIdentity;
}

export function HomePage({ service, user }: HomePageProps) {
  const [state, setState] = useState<ViewState>("loading");
  const [entities, setEntities] = useState<Entity[]>([]);
  const [failure, setFailure] = useState<ServiceError>();
  const permissions = user?.permissions ?? [];

  const load = useCallback(
    async (signal: AbortSignal) => {
      if (!can(permissions, PERMISSIONS.ENTITY_VIEW)) {
        setState("forbidden");
        return;
      }
      setState("loading");
      setFailure(undefined);
      try {
        const result = await service.list(signal);
        setEntities(result.data);
        setState(result.data.length === 0 ? "empty" : "ready");
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") return;
        setFailure(
          error instanceof ServiceError
            ? error
            : new NetworkError("发生未知网络错误", { cause: error }),
        );
        setState("error");
      }
    },
    [permissions, service],
  );

  useEffect(() => {
    const controller = new AbortController();
    void load(controller.signal);
    return () => controller.abort();
  }, [load]);

  if (state === "loading") {
    return <Spin tip="正在加载业务数据" fullscreen={false} />;
  }
  if (state === "forbidden") {
    return (
      <Result
        status="403"
        title="无权访问"
        subTitle="当前角色缺少业务对象查看权限，请联系管理员。"
      />
    );
  }
  if (state === "error") {
    if (failure instanceof UnauthorizedError) {
      return (
        <Result
          status="warning"
          title="登录状态已失效"
          subTitle="请重新登录后继续。"
        />
      );
    }
    if (failure instanceof ForbiddenError) {
      return (
        <Result
          status="403"
          title="服务拒绝访问"
          subTitle="当前账号无权读取该业务数据。"
        />
      );
    }
    if (failure instanceof NotFoundError) {
      return (
        <Result
          status="404"
          title="业务数据不存在"
          subTitle="数据可能已被删除或地址已失效。"
        />
      );
    }
    if (failure instanceof BusinessError) {
      return (
        <Result
          status="warning"
          title="请求未通过业务校验"
          subTitle={failure.message}
        />
      );
    }
    const retryable =
      failure instanceof ServerError ||
      failure instanceof NetworkError ||
      failure instanceof ProtocolError;
    return (
      <Result
        status="error"
        title={
          failure instanceof NetworkError ? "网络连接失败" : "服务响应异常"
        }
        subTitle={
          failure?.requestId
            ? `请稍后重试；请求编号：${failure.requestId}`
            : "检查网络连接后重试。"
        }
        extra={retryable ? (
          <Button
            type="primary"
            onClick={() => void load(new AbortController().signal)}
          >
            重新加载
          </Button>
        ) : undefined}
      />
    );
  }
  if (state === "empty") {
    return <Empty description="暂无业务对象，可在接入真实 API 后创建数据。" />;
  }

  return (
    <Space direction="vertical" size="large" style={{ width: "100%" }}>
      <div>
        <Typography.Title level={2}>业务概览</Typography.Title>
        <Typography.Text type="secondary">
          由场景模板继续扩展领域页面、筛选与关键操作。
        </Typography.Text>
      </div>
      <Table<Entity>
        rowKey="id"
        dataSource={entities}
        pagination={false}
        columns={[
          { title: "编号", dataIndex: "id" },
          { title: "名称", dataIndex: "name" },
          {
            title: "状态",
            dataIndex: "status",
            render: (status: Entity["status"]) => (
              <Tag color={status === "active" ? "success" : "default"}>
                {status === "active" ? "运行中" : "已暂停"}
              </Tag>
            ),
          },
          {
            title: "操作",
            render: () => (
              <Button
                type="link"
                disabled={!can(permissions, PERMISSIONS.ENTITY_EDIT)}
              >
                编辑
              </Button>
            ),
          },
        ]}
      />
    </Space>
  );
}
