import {
  Alert,
  Badge,
  Button,
  Card,
  Col,
  Divider,
  Dropdown,
  Empty,
  Form,
  Input,
  Menu,
  Modal,
  Result,
  Row,
  Select,
  Space,
  Spin,
  Table,
  Tabs,
  Tag,
  Tooltip,
  Typography,
  theme,
} from "antd";
import { useState, type CSSProperties, type ReactNode } from "react";

const { Title, Paragraph, Text } = Typography;

function Swatch({
  label,
  value,
  radius,
  border,
}: {
  label: string;
  value: string;
  radius: number;
  border: string;
}) {
  return (
    <Col xs={12} sm={8} md={6} xl={4}>
      <div
        style={{
          border: `1px solid ${border}`,
          borderRadius: radius,
          overflow: "hidden",
        }}
      >
        <div style={{ height: 56, background: value }} />
        <div style={{ padding: "8px 12px" }}>
          <Text strong>{label}</Text>
          <br />
          <Text type="secondary" code>
            {value}
          </Text>
        </div>
      </div>
    </Col>
  );
}

function TypeRow({
  label,
  children,
  border,
}: {
  label: string;
  children: ReactNode;
  border: string;
}) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "minmax(160px, 200px) 1fr",
        gap: 16,
        alignItems: "baseline",
        padding: "12px 0",
        borderBottom: `1px solid ${border}`,
      }}
    >
      <Text type="secondary">{label}</Text>
      <div>{children}</div>
    </div>
  );
}

function Rule({ ok, children }: { ok: boolean; children: ReactNode }) {
  return (
    <Alert
      type={ok ? "success" : "error"}
      showIcon
      message={ok ? "做" : "不做"}
      description={children}
      style={{ height: "100%" }}
    />
  );
}

export function DesignPreview() {
  const { token } = theme.useToken();
  const [modalOpen, setModalOpen] = useState(false);
  const radius = token.borderRadius;
  const border = token.colorBorder;
  const split = token.colorSplit;
  const presets: Array<[string, string]> = [
    ["blue", token.blue],
    ["purple", token.purple],
    ["cyan", token.cyan],
    ["green", token.green],
    ["magenta", token.magenta],
    ["red", token.red],
    ["orange", token.orange],
    ["yellow", token.yellow],
    ["volcano", token.volcano],
    ["geekblue", token.geekblue],
    ["gold", token.gold],
    ["lime", token.lime],
  ];

  const motionPreview = (duration: string): CSSProperties => ({
    width: 140,
    height: 48,
    display: "grid",
    placeItems: "center",
    color: token.colorTextLightSolid,
    background: token.colorPrimary,
    borderRadius: radius,
    transition: `transform ${duration} ${token.motionEaseInOut}`,
  });

  return (
    <Space orientation="vertical" size={24} style={{ display: "flex" }}>
      <div>
        <Title level={3}>设计规范预览</Title>
        <Paragraph type="secondary">
          对照 ant-design-v6.md（Ant Design v6 默认浅色主题）。运行时 Token 来自
          ConfigProvider。主色必须是默认蓝，成功绿只表示状态。
        </Paragraph>
        <Space wrap size={8}>
          {[
            ["概述", "#overview"],
            ["价值观", "#values"],
            ["色彩", "#colors"],
            ["字体", "#type"],
            ["布局", "#layout"],
            ["海拔与动效", "#elevation"],
            ["形状", "#shapes"],
            ["组件选用", "#choose"],
            ["组件外观", "#components"],
            ["对与错", "#rules"],
            ["定制", "#customize"],
          ].map(([label, href]) => (
            <Button key={href} type="link" href={href} style={{ paddingInline: 0 }}>
              {label}
            </Button>
          ))}
        </Space>
      </div>

      <div id="overview">
        <Card title="概述">
          <Paragraph>
            本文描述 <Text strong>Ant Design v6</Text>{" "}
            默认浅色主题。大版本表示设计语言重构，小版本与补丁保持文档稳定。
            Ant Design 面向中后台控制台、看板和运营工具：给大型团队一套有主张的共同基础，使密集、数据丰富的界面不必在每个屏幕上重新决定基础规则。
          </Paragraph>
        </Card>
      </div>

      <div id="values">
        <Card title="价值观">
          <Row gutter={[16, 16]}>
            {[
              [
                "Natural",
                "界面遵循既有惯例，不让回头用户感到意外。优先采用操作系统和前代企业软件中已存在的模式。",
              ],
              [
                "Certain",
                "用户始终知道自己处于什么状态、输入产生了什么结果、下一步是什么。悬停、焦点、加载和错误状态明确且一致。",
              ],
              [
                "Meaningful",
                "视觉强调只留给行动。不传达信息的装饰一律去掉。",
              ],
              [
                "Growing",
                "系统可以从小表单扩到密表格、再扩到多租户管理控制台，而不失去一致性。",
              ],
            ].map(([name, copy]) => (
              <Col key={name} xs={24} md={12}>
                <Card size="small" title={name}>
                  {copy}
                </Card>
              </Col>
            ))}
          </Row>
        </Card>
      </div>

      <div id="colors">
        <Card title="色彩">
          <Paragraph>
            色板由一个主色种子、四个语义状态种子，以及文字与表面的中性色构成。改种子，派生色一起移动。主色用于操作、链接、焦点环、选中导航和激活
            Tab。
          </Paragraph>
          <Alert
            type="info"
            showIcon
            message="无障碍"
            description="部分品牌色组合（白字配主色、主文字配浅选中底）低于 WCAG AA 小字 4.5:1。严格无障碍时通过 ConfigProvider 加深 colorPrimary，或做组件级覆盖，不要发明一次性颜色。"
            style={{ marginBottom: token.padding }}
          />
          <Title level={5}>品牌与语义</Title>
          <Row gutter={[16, 16]}>
            {[
              ["primary", token.colorPrimary],
              ["success · 仅状态", token.colorSuccess],
              ["warning", token.colorWarning],
              ["error", token.colorError],
              ["info", token.colorInfo],
              ["选中底", token.colorPrimaryBg],
            ].map(([label, value]) => (
              <Swatch
                key={label}
                label={label}
                value={value}
                radius={radius}
                border={border}
              />
            ))}
          </Row>
          <Title level={5}>中性：文字与表面</Title>
          <Row gutter={[16, 16]}>
            {[
              ["on-surface · 0.88", token.colorText],
              ["on-surface-variant · 0.65", token.colorTextSecondary],
              ["描述 · 0.45", token.colorTextTertiary],
              ["disabled · 0.25", token.colorTextQuaternary],
              ["surface / elevated", token.colorBgContainer],
              ["elevated", token.colorBgElevated],
              ["layout", token.colorBgLayout],
              ["container fill", token.colorFillAlter],
              ["outline", token.colorBorder],
              ["outline-variant", token.colorBorderSecondary],
            ].map(([label, value]) => (
              <Swatch
                key={label}
                label={label}
                value={value}
                radius={radius}
                border={border}
              />
            ))}
          </Row>
          <Paragraph type="secondary" style={{ marginTop: token.padding }}>
            运行时中性文字用透明黑叠层，而不是实心灰，以免切断浅底或彩色单元格。文档 hex
            是叠在白底上的等效结果。
          </Paragraph>
          <Row gutter={[16, 16]}>
            {[
              ["主文字 0.88", token.colorText],
              ["次文字 0.65", token.colorTextSecondary],
              ["描述 0.45", token.colorTextTertiary],
              ["占位 0.25", token.colorTextQuaternary],
            ].map(([label, value]) => (
              <Col key={label} xs={24} sm={12} md={6}>
                <div
                  style={{
                    border: `1px solid ${border}`,
                    borderRadius: radius,
                    overflow: "hidden",
                  }}
                >
                  <div style={{ padding: 12, color: value }}>{label}</div>
                  <div
                    style={{
                      padding: 12,
                      color: value,
                      background: token.colorPrimaryBg,
                    }}
                  >
                    叠在选中底上
                  </div>
                </div>
              </Col>
            ))}
          </Row>
          <Title level={5}>预设色 · 只给标签、图表和分类</Title>
          <Paragraph type="secondary">
            不要把预设色当成主操作色。状态用语义色，主操作只用 primary。pink 是 magenta
            的已弃用别名。
          </Paragraph>
          <Row gutter={[16, 16]}>
            {presets.map(([label, value]) => (
              <Swatch
                key={label}
                label={label}
                value={value}
                radius={radius}
                border={border}
              />
            ))}
          </Row>
        </Card>
      </div>

      <div id="type">
        <Card title="字体">
          <Paragraph>
            基础字号是 <Text strong>14px</Text>
            ，不是 16。产品界面只用两个字重：400 与 600。细体、700+
            粗体和斜体不用于界面骨架。选中态用颜色和描边，不用字重。
          </Paragraph>
          <TypeRow label={`display / heading1 ${token.fontSizeHeading1}/600`} border={split}>
            <span
              style={{
                fontSize: token.fontSizeHeading1,
                lineHeight: token.lineHeightHeading1,
                fontWeight: token.fontWeightStrong,
              }}
            >
              展示级标题
            </span>
          </TypeRow>
          <TypeRow label={`headline-lg ${token.fontSizeHeading2}/600`} border={split}>
            <span
              style={{
                fontSize: token.fontSizeHeading2,
                lineHeight: token.lineHeightHeading2,
                fontWeight: token.fontWeightStrong,
              }}
            >
              企业后台标题
            </span>
          </TypeRow>
          <TypeRow label={`headline-md ${token.fontSizeHeading3}/600`} border={split}>
            <span
              style={{
                fontSize: token.fontSizeHeading3,
                lineHeight: token.lineHeightHeading3,
                fontWeight: token.fontWeightStrong,
              }}
            >
              页面中标题
            </span>
          </TypeRow>
          <TypeRow label={`headline-sm ${token.fontSizeHeading4}/600`} border={split}>
            <span
              style={{
                fontSize: token.fontSizeHeading4,
                lineHeight: token.lineHeightHeading4,
                fontWeight: token.fontWeightStrong,
              }}
            >
              区块标题
            </span>
          </TypeRow>
          <TypeRow label={`title-lg ${token.fontSizeLG}/600`} border={split}>
            <span
              style={{
                fontSize: token.fontSizeLG,
                lineHeight: token.lineHeightLG,
                fontWeight: token.fontWeightStrong,
              }}
            >
              卡片标题 / 导航品牌
            </span>
          </TypeRow>
          <TypeRow label="title-md 14/600" border={split}>
            <span style={{ fontWeight: token.fontWeightStrong }}>表格表头 / 强调</span>
          </TypeRow>
          <TypeRow label={`body-lg ${token.fontSizeLG}/400`} border={split}>
            <span style={{ fontSize: token.fontSizeLG, lineHeight: token.lineHeightLG }}>
              宽松正文
            </span>
          </TypeRow>
          <TypeRow label="body-md 14/400" border={split}>
            默认正文。企业后台用 14px，不是 16px。
          </TypeRow>
          <TypeRow label={`body-sm ${token.fontSizeSM}/400`} border={split}>
            <Text type="secondary" style={{ fontSize: token.fontSizeSM }}>
              辅助说明、标签
            </Text>
          </TypeRow>
          <TypeRow label="code" border={split}>
            <Text code>const colorPrimary = token.colorPrimary</Text>
          </TypeRow>
          <Paragraph type="secondary" style={{ marginTop: token.paddingSM }}>
            字体栈：{token.fontFamily}
          </Paragraph>
          <Paragraph type="secondary">代码字体：{token.fontFamilyCode}</Paragraph>
        </Card>
      </div>

      <div id="layout">
        <Card title="布局">
          <Paragraph>
            所有间距对齐 <Text strong>4px 网格</Text>。六档为 4 / 4 / 8 / 16 / 24 /
            32。不要写魔法数字。输入框 11px 水平内边距是网格确立前的历史值，予以保留。
          </Paragraph>
          <Space align="end" size={16} wrap>
            {(
              [
                ["unit", token.sizeUnit],
                ["xs", token.paddingXXS],
                ["sm", token.paddingXS],
                ["md", token.padding],
                ["lg", token.paddingLG],
                ["xl", token.paddingXL],
              ] as const
            ).map(([label, size]) => (
              <div
                key={label}
                style={{
                  width: Math.max(size, token.sizeUnit),
                  height: 24 + size,
                  background: token.colorPrimaryBg,
                  border: `1px dashed ${token.colorPrimary}`,
                  color: token.colorPrimary,
                  fontSize: token.fontSizeSM,
                  display: "grid",
                  placeItems: "center",
                }}
              >
                {label} {size}
              </div>
            ))}
          </Space>
          <Paragraph type="secondary" style={{ marginTop: token.padding }}>
            控件高度 controlHeight = {token.controlHeight}px。
          </Paragraph>
          <Title level={5}>三层表面模型</Title>
          <Paragraph>
            不要在产品代码里写死白色或浅灰。读 Token。三层模型让暗色算法可以翻转表面阶梯而不拆布局。
          </Paragraph>
          <div
            style={{
              background: token.colorBgLayout,
              borderRadius: token.borderRadiusLG,
              padding: token.paddingLG,
            }}
          >
            <Text type="secondary">1. bg-layout — 页面背景</Text>
            <div
              style={{
                background: token.colorBgContainer,
                borderRadius: token.borderRadiusLG,
                padding: token.paddingLG,
                marginTop: token.padding,
              }}
            >
              <Paragraph>2. bg-container — 卡片、面板、表格、表单</Paragraph>
              <div
                style={{
                  background: token.colorBgElevated,
                  borderRadius: token.borderRadiusLG,
                  padding: "20px 24px",
                  boxShadow: token.boxShadow,
                  maxWidth: 360,
                }}
              >
                <Text strong>3. bg-elevated</Text>
                <Paragraph type="secondary" style={{ marginBottom: 0 }}>
                  与 container 同色，靠阴影区分。用于对话框、下拉、气泡。
                </Paragraph>
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div id="elevation">
        <Card title="海拔与动效">
          <Paragraph>
            Ant Design 是 flat-first。层级由边框和色调对比承担。阴影只出现在真正浮于上下文之上的表面。
          </Paragraph>
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <div
                style={{
                  background: token.colorBgContainer,
                  borderRadius: token.borderRadiusLG,
                  padding: token.padding,
                  boxShadow: token.boxShadowTertiary,
                }}
              >
                <Text strong>Tertiary · boxShadowTertiary</Text>
                <Paragraph type="secondary" style={{ marginBottom: 0 }}>
                  轻抬起 / 卡片分离
                </Paragraph>
              </div>
            </Col>
            <Col xs={24} md={12}>
              <div
                style={{
                  background: token.colorBgElevated,
                  borderRadius: token.borderRadiusLG,
                  padding: token.padding,
                  boxShadow: token.boxShadow,
                }}
              >
                <Text strong>Popup · boxShadow</Text>
                <Paragraph type="secondary" style={{ marginBottom: 0 }}>
                  标准浮层。另有 boxShadowSecondary、boxShadowCard、Drawer / Tabs overflow、Popover
                  arrow。
                </Paragraph>
              </div>
            </Col>
          </Row>
          <Title level={5}>动效</Title>
          <Paragraph type="secondary">
            Fast {token.motionDurationFast}（hover / press）· Mid {token.motionDurationMid}（折叠 /
            淡入）· Slow {token.motionDurationSlow}（对话框 / 抽屉）。缓动用命名 Token，不要自造
            cubic-bezier。悬停色块查看位移。
          </Paragraph>
          <Space wrap size={16}>
            {(
              [
                [token.motionDurationFast, `Fast ${token.motionDurationFast}`],
                [token.motionDurationMid, `Mid ${token.motionDurationMid}`],
                [token.motionDurationSlow, `Slow ${token.motionDurationSlow}`],
              ] as const
            ).map(([duration, label]) => (
              <div
                key={label}
                style={motionPreview(duration)}
                onMouseEnter={(event) => {
                  event.currentTarget.style.transform = "translateX(8px)";
                }}
                onMouseLeave={(event) => {
                  event.currentTarget.style.transform = "translateX(0)";
                }}
              >
                {label}
              </div>
            ))}
          </Space>
          <Paragraph type="secondary" style={{ marginTop: token.paddingSM }}>
            缓动：{token.motionEaseInOut} · {token.motionEaseOut} · {token.motionEaseOutBack} ·{" "}
            {token.motionEaseOutCirc} · {token.motionEaseInBack}
          </Paragraph>
        </Card>
      </div>

      <div id="shapes">
        <Card title="形状">
          <Paragraph>
            默认圆角 6px。控件 6px，表面 8px，标签 / Tooltip 4px。全胶囊只给头像、徽标和圆点，不给按钮或标签。直角留给表格和分段控件内边。相邻元素不要混用圆角。
          </Paragraph>
          <Space align="end" size={16} wrap>
            {[
              ["none", 0],
              ["xs", token.borderRadiusXS],
              ["sm", token.borderRadiusSM],
              ["DEFAULT", token.borderRadius],
              ["lg", token.borderRadiusLG],
              ["outer", token.borderRadiusOuter],
            ].map(([label, value]) => (
              <div
                key={label}
                style={{
                  width: 96,
                  height: 48,
                  display: "grid",
                  placeItems: "center",
                  background: token.colorPrimaryBg,
                  border: `1px solid ${token.colorPrimary}`,
                  color: token.colorPrimary,
                  fontSize: token.fontSizeSM,
                  borderRadius: value,
                }}
              >
                {label} {value}
              </div>
            ))}
            <div
              style={{
                width: token.controlHeight,
                height: token.controlHeight,
                borderRadius: token.controlHeight,
                background: token.colorError,
              }}
              aria-label="full 圆点只给 Badge"
            />
          </Space>
        </Card>
      </div>

      <div id="choose">
        <Card title="组件选用">
          <Paragraph type="secondary">
            后台常用对照。实现时打开 references/components/INDEX.md
            和对应组件文件，不要整份阅读官网全文快照。
          </Paragraph>
          <Table
            pagination={false}
            size="small"
            dataSource={[
              {
                key: "button",
                scene: "主操作 / 次操作 / 危险操作",
                use: "主按钮只留一个。次操作用 default / text / link。删除用 danger + Popconfirm。",
                avoid: "同一决策面两个 primary。用绿色实心按钮当主操作。",
              },
              {
                key: "table",
                scene: "结构化列表、排序、分页、批量",
                use: "Table",
                avoid: "用卡片宫格替代主表。用 List 承载八列密数据。",
              },
              {
                key: "list",
                scene: "短队列、意见流、排行",
                use: "List；审批队列也可用 Table。",
                avoid: "为排行再复制一张完整 CRUD 表。",
              },
              {
                key: "desc",
                scene: "只读对象摘要",
                use: "Descriptions",
                avoid: "用禁用表单冒充详情。",
              },
              {
                key: "edit",
                scene: "列表上新增 / 编辑",
                use: "短表单用 Drawer 或 Modal。",
                avoid: "默认再拆 /new 路由。",
              },
              {
                key: "modal",
                scene: "打断工作流的确认 / 决策",
                use: "Modal；驳回强制填意见。",
                avoid: "通过 / 驳回不确认。",
              },
              {
                key: "tag",
                scene: "分类、非关键状态",
                use: "Tag 或带文字的 Badge",
                avoid: "用 Tag 表示关键失败。圆点代替必读文字。",
              },
              {
                key: "alert",
                scene: "页级成功 / 警告 / 错误说明",
                use: "Alert",
                avoid: "把整页做成成功绿。",
              },
              {
                key: "state",
                scene: "加载 / 空 / 无权限 / 失败",
                use: "Spin、Empty（保留查询区）、不同 Result 区分 401/403/404/5xx。",
                avoid: "绿色骨架屏。401 和 403 收成同一句。",
              },
            ]}
            columns={[
              { title: "场景", dataIndex: "scene", width: "28%" },
              { title: "用这个", dataIndex: "use" },
              { title: "不要用这个", dataIndex: "avoid" },
            ]}
          />
        </Card>
      </div>

      <div id="components">
        <Card title="组件外观">
          <Title level={5}>Button · 同一决策面只有一个主按钮</Title>
          <Paragraph type="secondary">
            主按钮：实心主色、白字、32px、6px。悬停变亮，按下变 dark。次按钮改文字和描边，不改填充。
          </Paragraph>
          <Space>
            <Button type="primary">查询</Button>
            <Button>重置</Button>
            <Button disabled>无权限</Button>
          </Space>

          <Divider />
          <Title level={5}>Input / Select</Title>
          <Paragraph type="secondary">
            高度与按钮对齐。焦点加主色描边。Select 在交互前看起来像 Input。占位符用禁用文字色。
          </Paragraph>
          <Form layout="inline">
            <Form.Item label="关键词">
              <Input placeholder="请输入关键词" />
            </Form.Item>
            <Form.Item label="仓库">
              <Select
                defaultValue="all"
                style={{ width: 160 }}
                options={[
                  { value: "all", label: "全部仓库" },
                  { value: "east", label: "华东仓" },
                ]}
              />
            </Form.Item>
          </Form>

          <Divider />
          <Title level={5}>Card / Modal</Title>
          <Paragraph type="secondary">
            Card：白表面、8px、内边距 24px。Modal：同样表面和圆角，用次级阴影，居中叠在 45%
            遮罩上，主体上下 20px、左右 24px。
          </Paragraph>
          <Space>
            <Button type="primary" onClick={() => setModalOpen(true)}>
              打开对话框
            </Button>
          </Space>
          <Modal
            title="确认提交"
            open={modalOpen}
            onOk={() => setModalOpen(false)}
            onCancel={() => setModalOpen(false)}
            okText="确定"
            cancelText="取消"
          >
            对话框使用 elevated 表面与 popup 阴影，不要手写遮罩色。
          </Modal>

          <Divider />
          <Title level={5}>Menu · 选中项</Title>
          <Paragraph type="secondary">
            选中底 + 主色文字，是导航里“你在这里”的唯一视觉线索。
          </Paragraph>
          <Menu
            mode="inline"
            selectedKeys={["stock"]}
            style={{ width: 240, border: `1px solid ${border}`, borderRadius: radius }}
            items={[
              { key: "stock", label: "库存查询" },
              { key: "io", label: "出入库" },
              { key: "audit", label: "盘点任务" },
            ]}
          />

          <Divider />
          <Title level={5}>Tabs · 激活项</Title>
          <Paragraph type="secondary">
            主色文字 + 2px 主色下划线。未激活为次文字。任何状态下 Tab 都没有背景填充。
          </Paragraph>
          <Tabs
            items={[
              { key: "overview", label: "概览", children: "概览内容" },
              { key: "detail", label: "明细", children: "明细内容" },
              { key: "log", label: "日志", children: "日志内容" },
            ]}
          />

          <Divider />
          <Title level={5}>Table · 表头</Title>
          <Paragraph type="secondary">
            表头用 container 浅底和 title-md。表体只在悬停时变底，默认不做斑马纹。
          </Paragraph>
          <Table
            pagination={false}
            dataSource={[
              { key: "1", name: "劳保手套", status: "正常" },
              { key: "2", name: "扫描枪", status: "盘点中" },
            ]}
            columns={[
              { title: "名称", dataIndex: "name" },
              {
                title: "状态",
                dataIndex: "status",
                render: (status: string) => (
                  <Tag color={status === "正常" ? "success" : "blue"}>{status}</Tag>
                ),
              },
              {
                title: "操作",
                render: () => <Button type="link">详情</Button>,
              },
            ]}
          />

          <Divider />
          <Title level={5}>Tag / Alert / Badge</Title>
          <Paragraph type="secondary">
            Tag 是分类标签，不是关键状态。Alert 用浅语义底 + 正常文字。Badge
            圆点不能在无障碍关键流程里代替文字。
          </Paragraph>
          <Space wrap>
            <Tag>默认</Tag>
            <Tag color="blue">分类 · blue</Tag>
            <Tag color="success">分类 · 非主操作</Tag>
            <Badge status="error" text="故障" />
            <Badge status="success" text="正常" />
            <Badge status="warning" text="降级" />
          </Space>
          <Space orientation="vertical" style={{ display: "flex", marginTop: token.padding }}>
            <Alert type="success" message="成功：只用 success 绿提示结果，不要把整页做成绿色。" />
            <Alert type="warning" message="警告：空数据用 Empty，保留查询区。" />
            <Alert type="error" message="错误：用 Result；401 和 403 分开。" />
            <Alert type="info" message="信息：加载中用 Spin，不要换一套绿色骨架屏。" />
          </Space>

          <Divider />
          <Title level={5}>Tooltip / Dropdown</Title>
          <Paragraph type="secondary">
            Tooltip：反相表面，由框架定位，不要手动钉死。Dropdown
            项悬停只用浅底，不改文字色。
          </Paragraph>
          <Space>
            <Tooltip title="保存后立即生效">
              <Button>悬停查看提示</Button>
            </Tooltip>
            <Dropdown
              menu={{
                items: [
                  { key: "edit", label: "编辑" },
                  { key: "export", label: "导出" },
                  { key: "delete", label: "删除" },
                ],
              }}
            >
              <Button>更多</Button>
            </Dropdown>
          </Space>

          <Divider />
          <Title level={5}>加载 / 空 / 错误 / 无权限</Title>
          <Space orientation="vertical" style={{ display: "flex" }}>
            <Spin spinning>
              <Alert type="info" message="加载中使用 Spin，不要换绿色骨架屏。" />
            </Spin>
            <Empty description="暂无数据" />
            <Result status="error" title="加载失败" subTitle="区分网络、业务和权限错误。" />
            <Result status="403" title="无权访问此页面" />
          </Space>
        </Card>
      </div>

      <div id="rules">
        <Card title="对与错">
          <Row gutter={[16, 16]}>
            <Col xs={24} md={12}>
              <Space orientation="vertical" style={{ display: "flex" }}>
                <Rule ok>
                  用四个设计价值观当平局裁决。更能让用户状态确定、更易读的做法胜出。
                </Rule>
                <Rule ok>
                  从 surface / surface-container / surface-layout 读表面，对应三层模型。
                </Rule>
                <Rule ok>
                  找不到更具体 Token 时，组件级过渡用 motionDurationMid。
                </Rule>
                <Rule ok>预设色板只留给标签、图表和分类可视化。</Rule>
                <Rule ok>每一个间隙、内边距和槽都通过间距刻度对齐 4px 网格。</Rule>
              </Space>
            </Col>
            <Col xs={24} md={12}>
              <Space orientation="vertical" style={{ display: "flex" }}>
                <Rule ok={false}>
                  同一表面不要叠两个主色按钮。只留一个，其余降为 default。
                </Rule>
                <Rule ok={false}>
                  不要硬编码白色或浅灰。hex 是附带结果，角色才重要。
                </Rule>
                <Rule ok={false}>不要发明自定义 cubic-bezier。用已命名缓动。</Rule>
                <Rule ok={false}>
                  不要在预设色板外铸造强调色。若某屏看起来需要，多半该改布局。
                </Rule>
                <Rule ok={false}>
                  不要用魔法数字。刻度缺一档时，该重看设计，而不是一像素覆盖。
                </Rule>
              </Space>
            </Col>
          </Row>
          <Alert
            style={{ marginTop: token.padding }}
            type="warning"
            showIcon
            message="PKUSE 叠加"
            description="不要用自定义墨绿做顶栏或品牌块，也不要把页面底改成绿灰。成功绿只出现在 Tag、Alert、状态点。"
          />
        </Card>
      </div>

      <div id="customize">
        <Card title="定制">
          <Paragraph>
            YAML 中的每个值都是 defaultAlgorithm 产出的默认浅色主题。主题化包括算法派生、组件级覆盖、动态切换、嵌套作用域、CSS
            变量、静态消费和零运行时提取。入口是 ConfigProvider 的 theme。
          </Paragraph>
          <ol>
            <li>
              <Text strong>Seed token 覆盖。</Text> 传 theme.token 替换种子。主色和语义色会展开派生阶梯；colorBgBase /
              colorTextBase 驱动中性表面和文字。
            </li>
            <li>
              <Text strong>算法切换。</Text> defaultAlgorithm / darkAlgorithm / compactAlgorithm
              可单独或组成数组。不要手工反色。
            </li>
            <li>
              <Text strong>组件级覆盖。</Text> theme.components.Button
              等可覆盖单个组件，不影响其他组件。
            </li>
            <li>
              <Text strong>运行时作用域。</Text> 嵌套 ConfigProvider
              创建局部主题。静态 message / Modal / notification API 需 hook、App 或
              holder 才能拿到上下文。
            </li>
            <li>
              <Text strong>Token 消费与输出。</Text> React 内用 theme.useToken()，React 外用
              theme.getDesignToken()。需要 CSS 变量时用 theme.cssVar。
            </li>
          </ol>
          <Paragraph>
            先保住交互结构、密度、状态反馈和组件语义，再改最小种子集。本页当前主色{" "}
            <Text code>{token.colorPrimary}</Text>，圆角 <Text code>{String(token.borderRadius)}</Text>
            ，字号 <Text code>{String(token.fontSize)}</Text>。
          </Paragraph>
        </Card>
      </div>
    </Space>
  );
}
