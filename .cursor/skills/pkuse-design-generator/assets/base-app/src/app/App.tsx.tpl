import { App as AntdApp, ConfigProvider, Layout, Result, Space, Typography } from "antd";
import { useMemo } from "react";
import {
  BrowserRouter,
  Link,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";
import type { MicroAppProps } from "../micro-app/contracts";
import {
  buildVisibleMenu,
  canAccessRoute,
  createRouteManifest,
} from "../routes/manifest";
import { ErrorBoundary } from "./ErrorBoundary";
import { createServices } from "./services";
import { appTheme } from "./theme";

interface AppProps {
  props: MicroAppProps;
  title: string;
  standalone: boolean;
}

function AppContent({ props, title, standalone }: AppProps) {
  const services = useMemo(
    () => createServices(standalone ? "mock" : "api", props),
    [props, standalone],
  );
  const permissions = props.user?.permissions ?? [];
  const manifest = useMemo(
    () => createRouteManifest({ service: services.entities, user: props.user }),
    [props.user, services.entities],
  );
  const menu = buildVisibleMenu(manifest, permissions);

  const content = (
    <main className="pkuse-content">
      <ErrorBoundary>
        <Routes>
          {manifest.map((route) => (
            <Route
              key={route.path}
              path={route.path}
              element={
                canAccessRoute(route, permissions) ? (
                  route.element
                ) : (
                  <Navigate to="/403" replace />
                )
              }
            />
          ))}
          <Route
            path="/403"
            element={<Result status="403" title="无权访问此页面" />}
          />
          <Route
            path="*"
            element={<Result status="404" title="页面不存在" />}
          />
        </Routes>
      </ErrorBoundary>
    </main>
  );

  if (!standalone) return content;

  return (
    <Layout className="pkuse-shell">
      <Layout.Header className="pkuse-header">
        <Space size="large">
          <Typography.Text strong className="pkuse-brand">
            {title}
          </Typography.Text>
          <nav aria-label="本地导航">
            <Space>
              {menu.map((item) => (
                <Link key={item.path} to={item.path}>
                  {item.title}
                </Link>
              ))}
            </Space>
          </nav>
        </Space>
        <Typography.Text className="pkuse-user">
          {props.user?.displayName}
        </Typography.Text>
      </Layout.Header>
      <Layout.Content>{content}</Layout.Content>
    </Layout>
  );
}

export function App(appProps: AppProps) {
  return (
    <div data-pkuse-app="__APP_NAME__">
      <ConfigProvider
        prefixCls="__APP_NAME__"
        theme={{
          ...appTheme,
          cssVar: { ...appTheme.cssVar, key: "__APP_PREFIX__" },
        }}
      >
        <AntdApp>
          <BrowserRouter basename={appProps.props.routeBase ?? "/"}>
            <AppContent {...appProps} />
          </BrowserRouter>
        </AntdApp>
      </ConfigProvider>
    </div>
  );
}
