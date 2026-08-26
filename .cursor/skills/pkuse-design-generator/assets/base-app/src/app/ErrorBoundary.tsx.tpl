import { Button, Result } from "antd";
import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  failed: boolean;
}

export class ErrorBoundary extends Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = { failed: false };

  static getDerivedStateFromError(): ErrorBoundaryState {
    return { failed: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    if (import.meta.env.DEV) {
      console.error("[__APP_NAME__] render failed", error, info);
    }
  }

  render(): ReactNode {
    if (this.state.failed) {
      return (
        <Result
          status="500"
          title="页面暂时无法显示"
          subTitle="请重试；若问题持续，请提供当前页面与操作信息。"
          extra={
            <Button
              type="primary"
              onClick={() => this.setState({ failed: false })}
            >
              重试
            </Button>
          }
        />
      );
    }
    return this.props.children;
  }
}
