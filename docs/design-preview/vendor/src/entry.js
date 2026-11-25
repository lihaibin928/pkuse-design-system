// 本地打包入口：渲染预览站全部真实组件演示（antd 6.7.1）
// 构建：npm install && npm run build（esbuild 产出 ../protable.js）
const React = require('react');
const { createRoot } = require('react-dom/client');
const { ConfigProvider, Tag, Button, Popconfirm, Input, Breadcrumb, Cascader,
  DatePicker, Form, InputNumber, Radio, Select, Slider, Switch, TimePicker,
  Transfer, TreeSelect, Upload, Avatar, Badge, Card, Descriptions, Tabs, Dropdown, Alert,
  Empty, Popover, Segmented, Statistic, Timeline, Tooltip, Tour, Tree,
  Drawer, App, Progress, Result, Spin, Watermark, Affix, BorderBeam } = require('antd');
const AntIcons = require('@ant-design/icons');
const { PlusOutlined, ImportOutlined, DeleteOutlined } = AntIcons;
const zhCN = require('antd/locale/zh_CN');
const dayjs = require('dayjs');
require('dayjs/locale/zh-cn');
const { ProTable, ProForm, ProFormText, ProFormSelect, ProFormDatePicker, ProFormTimePicker, ProFormDigit,
  ProFormCheckbox, ProFormRadio, ProFormSwitch, ProFormTextArea, ProFormRate, ProFormSlider, ProFormUploadDragger, ProFormGroup, ProCard, ProDescriptions, ProSkeleton,
  ModalForm, DrawerForm, StatisticCard } = require('@ant-design/pro-components');

const h = React.createElement;
const actionRef = { current: null };
let selectedRowKeys = [];

const data = [
  { no: 'REG-2026091201', name: '张伟', type: '个人登记', status: '正常', time: '2026-09-12 11:18' },
  { no: 'REG-2026091202', name: '李娜', type: '团体登记', status: '待处理', time: '2026-09-12 09:40' },
  { no: 'REG-2026091103', name: '王强', type: '个人登记', status: '正常', time: '2026-09-11 16:22' },
  { no: 'REG-2026091104', name: '赵敏', type: '个人登记', status: '异常', time: '2026-09-11 15:05' },
  { no: 'REG-2026091105', name: '刘洋', type: '团体登记', status: '正常', time: '2026-09-11 10:31' },
  { no: 'REG-2026091006', name: '陈静', type: '个人登记', status: '正常', time: '2026-09-10 17:48' },
  { no: 'REG-2026091007', name: '杨帆', type: '团体登记', status: '待处理', time: '2026-09-10 14:26' },
  { no: 'REG-2026091008', name: '周琪', type: '个人登记', status: '正常', time: '2026-09-10 09:15' },
  { no: 'REG-2026090909', name: '吴迪', type: '团体登记', status: '正常', time: '2026-09-09 15:33' },
  { no: 'REG-2026090910', name: '郑爽', type: '个人登记', status: '异常', time: '2026-09-09 11:57' },
  { no: 'REG-2026090811', name: '孙悦', type: '团体登记', status: '正常', time: '2026-09-08 16:44' },
  { no: 'REG-2026090812', name: '何超', type: '个人登记', status: '待处理', time: '2026-09-08 08:52' }
];

// ===== ProTable 共享列定义 =====
const nameCol = { title: '姓名', dataIndex: 'name' };
const typeCol = {
  title: '类型', dataIndex: 'type', align: 'center',
  valueEnum: { 个人登记: { text: '个人登记' }, 团体登记: { text: '团体登记' } },
  render: (_, record) => h(Tag, record.type === '团体登记' ? { color: 'blue' } : null, record.type)
};
const statusCol = {
  title: '状态', dataIndex: 'status', align: 'center',
  valueEnum: {
    正常: { text: '正常', status: 'Success' },
    待处理: { text: '待处理', status: 'Warning' },
    异常: { text: '异常', status: 'Error' }
  }
};
const timeCol = { title: '登记时间', dataIndex: 'time', search: false, align: 'center' };
const timeRangeCol = {
  title: '登记时间', dataIndex: 'timeRange', valueType: 'dateRange', hideInTable: true,
  search: { transform: (v) => ({ begin: v[0], end: v[1] }) }
};

function tableRequest(params) {
  const rows = data.filter((r) =>
    (!params.name || r.name.includes(params.name)) &&
    (!params.no || r.no.includes(params.no)) &&
    (!params.type || r.type === params.type) &&
    (!params.status || r.status === params.status) &&
    (!params.begin || r.time.slice(0, 10) >= params.begin) &&
    (!params.end || r.time.slice(0, 10) <= params.end));
  return Promise.resolve({ data: rows, total: rows.length, success: true });
}

function batchDelete() {
  selectedRowKeys.forEach((k) => {
    const i = data.findIndex((r) => r.no === k);
    if (i > -1) data.splice(i, 1);
  });
  selectedRowKeys = [];
  if (actionRef.current && actionRef.current.clearSelected) actionRef.current.clearSelected();
  if (actionRef.current && actionRef.current.reload) actionRef.current.reload();
}

// ===== 渲染入口：所有挂载点按 pkInit 防重入 =====
function mountDemo(id, renderFn) {
  const el = document.getElementById(id);
  if (!el || el.dataset.pkInit) return;
  el.dataset.pkInit = '1';
  createRoot(el).render(h(ConfigProvider, { locale: zhCN }, h('div', { style: { maxWidth: 560 } }, renderFn())));
}

function renderAll() {
  // ===== ProTable 复杂数据展示（页面模版 / 表格 共用） =====
  [document.getElementById('protable-mount'), document.getElementById('protable-component-mount')].forEach((el) => {
    if (!el || el.dataset.pkInit) return;
    el.dataset.pkInit = '1';
    const columns = [
      { title: '序号', dataIndex: 'index', valueType: 'index', width: 64, search: false, fixed: 'left', align: 'center' },
      { title: '单号', dataIndex: 'no', copyable: true, ellipsis: true, fixed: 'left', width: 180 },
      nameCol, typeCol, statusCol, timeCol, timeRangeCol,
      { title: '操作', valueType: 'option', fixed: 'right', width: 120,
        render: (_, record) => [
          h('a', { href: 'javascript:void(0)', key: 'edit' }, '编辑'),
          h('a', { href: 'javascript:void(0)', key: 'delete', style: { color: '#FF4D4F', marginLeft: 12 } }, '删除')
        ] }
    ];
    createRoot(el).render(
      h(ConfigProvider, { locale: zhCN },
        h(ProTable, {
          rowKey: 'no', actionRef, columns,
          search: { labelWidth: 70, span: 6 },
          request: tableRequest,
          rowSelection: { fixed: true, onChange: (keys) => { selectedRowKeys = keys; } },
          tableAlertRender: false,
          pagination: { current: 1, pageSize: 5, showSizeChanger: true, pageSizeOptions: [5, 10, 20] },
          scroll: { x: 1100 },
          dateFormatter: 'string',
          options: false,
          toolBarRender: () => [
            h(Button, { type: 'primary', icon: h(PlusOutlined), key: 'new' }, '新建'),
            h(Button, { key: 'import', icon: h(ImportOutlined) }, '导入'),
            h(Popconfirm, { key: 'delete', title: '确定删除选中的记录吗？', disabled: !selectedRowKeys.length, onConfirm: batchDelete },
              h(Button, { danger: true, icon: h(DeleteOutlined), disabled: !selectedRowKeys.length }, '批量删除'))
          ]
        })));
  });

  // ===== ProTable 简易数据展示 =====
  const simpleEl = document.getElementById('protable-simple-mount');
  if (simpleEl && !simpleEl.dataset.pkInit) {
    simpleEl.dataset.pkInit = '1';
    const columns = [
      { title: '序号', dataIndex: 'index', valueType: 'index', width: 64, search: false, fixed: 'left', align: 'center' },
      { title: '单号', dataIndex: 'no', copyable: true, ellipsis: true, search: false, fixed: 'left', width: 180 },
      Object.assign({}, nameCol, { width: 160 }),
      Object.assign({}, typeCol, { width: 120, search: false }),
      Object.assign({}, statusCol, { width: 120 }),
      Object.assign({}, timeCol, { width: 160 }),
      { title: '操作', valueType: 'option', fixed: 'right', width: 80,
        render: (_, record) => [h('a', { href: 'javascript:void(0)', key: 'detail' }, '详情')] }
    ];
    createRoot(simpleEl).render(
      h(ConfigProvider, { locale: zhCN },
        h(ProTable, {
          rowKey: 'no', columns,
          search: { labelWidth: 70, defaultCollapsed: false, defaultColsNumber: 2, collapseRender: () => false },
          request: tableRequest,
          pagination: { current: 1, pageSize: 5, size: 'default', showSizeChanger: true, pageSizeOptions: [5, 10, 20] },
          scroll: { x: 1100 },
          dateFormatter: 'string',
          options: false,
          toolBarRender: false
        })));
  }

  // ===== 图标：尺寸与颜色规范 =====
  const sizeEl = document.getElementById('icon-size-demo');
  if (sizeEl && !sizeEl.dataset.pkInit) {
    sizeEl.dataset.pkInit = '1';
    const rows = [[14, '14px · 行内说明、表格操作'], [16, '16px · 按钮、输入前缀、菜单'], [20, '20px · 列表项、统计卡'], [24, '24px+ · 空状态、结果页']];
    createRoot(sizeEl).render(h(React.Fragment, null,
      rows.map(([size, text]) => h('div', { className: 'icon-size-item', key: size },
        h('span', { style: { fontSize: size + 'px', display: 'inline-flex' } }, h(AntIcons.SettingOutlined)),
        h('span', null, text)))));
  }

  const colorEl = document.getElementById('icon-color-demo');
  if (colorEl && !colorEl.dataset.pkInit) {
    colorEl.dataset.pkInit = '1';
    const rows = [['var(--text)', '默认／正文'], ['var(--text-secondary)', '次要'], ['var(--text-disabled)', '禁用'],
      ['var(--primary)', '主色（操作/选中）'], ['var(--success)', '成功'], ['var(--warning)', '警告'], ['var(--error)', '错误']];
    createRoot(colorEl).render(h(React.Fragment, null,
      rows.map(([color, text]) => h('span', { className: 'icon-color-item', style: { color }, key: text },
        h(AntIcons.CheckCircleFilled), ' ', text))));
  }

  // ===== FormFields 表单项（8 种字段卡片） =====
  const ffEl = document.getElementById('formfields-mount');
  if (ffEl && !ffEl.dataset.pkInit) {
    ffEl.dataset.pkInit = '1';
    const demo = (title, desc, field) => h('div', { className: 'field-demo' },
      h('h4', { style: { margin: '0 0 4px', fontWeight: 600 } }, title),
      h('p', { style: { margin: '0 0 12px', color: 'var(--text-secondary)' } }, desc),
      h(ProForm, { submitter: false }, field));
    createRoot(ffEl).render(h(ConfigProvider, { locale: zhCN },
      h('div', { className: 'field-grid' },
        demo('Input · 输入框', '单行文本录入，用户最常用的控件。长度、格式用 rules 校验。',
          h(ProFormText, { name: 'ff-input', label: '姓名', placeholder: '请输入姓名', rules: [{ required: true, message: '请输入姓名' }], extra: '2-20 个字符，支持中文' })),
        demo('Select · 下拉选择', '选项较多的单选场景。交互前与输入框同形，选中后展示所选值。',
          h(ProFormSelect, { name: 'ff-select', label: '部门', placeholder: '请选择部门', options: [{ label: '研发部', value: 'rd' }, { label: '产品部', value: 'pd' }, { label: '运营部', value: 'op' }], extra: '单选；选项 5 个以内可平铺为单选框' })),
        demo('DatePicker · 日期选择', '选择日期，默认格式 YYYY-MM-DD。日期范围用 RangePicker。',
          h(ProFormDatePicker, { name: 'ff-date', label: '入职日期', placeholder: '请选择日期', extra: '格式 YYYY-MM-DD' })),
        demo('TimePicker · 时间选择', '选择时间，默认格式 HH:mm:ss。时间段用 TimeRangePicker。',
          h(ProFormTimePicker, { name: 'ff-time', label: '预约时间', placeholder: '请选择时间', extra: '格式 HH:mm:ss' })),
        demo('InputNumber · 数字输入', '通过键盘或步进按钮输入数字，可限定范围。金额、数量场景使用。',
          h(ProFormDigit, { name: 'ff-number', label: '随行人数', min: 1, max: 99, placeholder: '请输入数量', extra: '范围 1-99' })),
        demo('Checkbox · 多选', '在一组选项中多选。选项平铺展示，数量多时用下拉多选。',
          h(ProFormCheckbox.Group, { name: 'ff-checkbox', label: '随行设备', options: ['相机', '三脚架', '无人机'], extra: '可多选，全不选允许' })),
        demo('Radio · 单选', '在一组互斥选项中单选。选项少于 5 个时平铺，多于 5 个用下拉。',
          h(ProFormRadio.Group, { name: 'ff-radio', label: '登记类型', options: [{ label: '个人登记', value: 'person' }, { label: '团体登记', value: 'group' }], extra: '互斥选项；默认选中第一个' })),
        demo('Switch · 开关', '两种状态即时切换，切换后立即生效，无需确认按钮。',
          h(ProFormSwitch, { name: 'ff-switch', label: '需要接送', extra: '切换立即生效' }))
      )));
  }

  // ===== 图标画廊（6 类 × 16 = 96 个，可搜索/分类） =====
  const galleryEl = document.getElementById('icon-gallery');
  if (galleryEl && !galleryEl.dataset.pkInit) {
    galleryEl.dataset.pkInit = '1';
    const groups = [
      ['操作', ['PlusOutlined', 'PlusCircleOutlined', 'EditOutlined', 'FormOutlined', 'DeleteOutlined', 'MinusCircleOutlined', 'CopyOutlined', 'SaveOutlined', 'PrinterOutlined', 'ExportOutlined', 'ImportOutlined', 'UploadOutlined', 'DownloadOutlined', 'PaperClipOutlined', 'SendOutlined', 'ShareAltOutlined']],
      ['状态反馈', ['CheckOutlined', 'CloseOutlined', 'CheckCircleFilled', 'CheckCircleOutlined', 'CloseCircleFilled', 'ExclamationCircleFilled', 'ExclamationCircleOutlined', 'InfoCircleFilled', 'InfoCircleOutlined', 'QuestionCircleOutlined', 'WarningOutlined', 'SyncOutlined', 'LoadingOutlined', 'ClockCircleOutlined', 'HourglassOutlined', 'ThunderboltOutlined']],
      ['导航', ['LeftOutlined', 'RightOutlined', 'UpOutlined', 'DownOutlined', 'ArrowLeftOutlined', 'ArrowRightOutlined', 'ArrowUpOutlined', 'ArrowDownOutlined', 'CaretUpOutlined', 'CaretDownOutlined', 'MenuFoldOutlined', 'MenuUnfoldOutlined', 'HomeOutlined', 'AppstoreOutlined', 'MoreOutlined', 'FullscreenOutlined']],
      ['数据与图表', ['SearchOutlined', 'FilterOutlined', 'SortAscendingOutlined', 'SortDescendingOutlined', 'TableOutlined', 'UnorderedListOutlined', 'OrderedListOutlined', 'LineChartOutlined', 'BarChartOutlined', 'PieChartOutlined', 'DotChartOutlined', 'AreaChartOutlined', 'FundOutlined', 'RiseOutlined', 'FallOutlined', 'DashboardOutlined']],
      ['对象与业务', ['UserOutlined', 'TeamOutlined', 'ProfileOutlined', 'IdcardOutlined', 'ContactsOutlined', 'ShopOutlined', 'ShoppingCartOutlined', 'AccountBookOutlined', 'MoneyCollectOutlined', 'BankOutlined', 'PayCircleOutlined', 'FileTextOutlined', 'FolderOutlined', 'FolderOpenOutlined', 'ContainerOutlined', 'InboxOutlined']],
      ['系统与工具', ['SettingOutlined', 'ToolOutlined', 'ReloadOutlined', 'KeyOutlined', 'LockOutlined', 'UnlockOutlined', 'EyeOutlined', 'EyeInvisibleOutlined', 'BellOutlined', 'MailOutlined', 'PhoneOutlined', 'DatabaseOutlined', 'CloudOutlined', 'ApiOutlined', 'DesktopOutlined', 'BugOutlined']]
    ];
    const all = [];
    groups.forEach(([cat, names]) => names.forEach((name) => all.push({ cat, name })));
    const tabs = ['全部'].concat(groups.map((g) => g[0]));
    function IconGallery() {
      const [cat, setCat] = React.useState('全部');
      const [q, setQ] = React.useState('');
      const kw = q.trim().toLowerCase();
      const list = all.filter((i) => (cat === '全部' || i.cat === cat) && (!kw || i.name.toLowerCase().includes(kw)));
      return h('div', null,
        h('div', { className: 'icon-filter-row' },
          h(Input, { placeholder: '搜索图标', allowClear: true, value: q, onChange: (e) => setQ(e.target.value), style: { maxWidth: 240 } }),
          h('div', { className: 'icon-tabs' },
            tabs.map((t) => h('button', { type: 'button', key: t, className: 'icon-tab' + (t === cat ? ' active' : ''), onClick: () => setCat(t) }, t)))),
        h('div', { className: 'icon-grid' },
          list.map((i) => {
            const Ico = AntIcons[i.name];
            return Ico ? h('div', { className: 'icon-cell', key: i.name, title: i.name },
              h('span', { className: 'icon-cell-glyph' }, h(Ico)),
              h('span', { className: 'icon-cell-name' }, i.name)) : null;
          })));
    }
    createRoot(galleryEl).render(h(ConfigProvider, { locale: zhCN }, h(IconGallery)));
  }

  // ===== ModalForm 弹窗表单 =====
  const modalEl = document.getElementById('modalform-mount');
  if (modalEl && !modalEl.dataset.pkInit) {
    modalEl.dataset.pkInit = '1';
    createRoot(modalEl).render(h(ConfigProvider, { locale: zhCN },
      h(ModalForm, { title: '新建用户', trigger: h(Button, { type: 'primary' }, '点击打开弹窗表单'), onFinish: async () => true },
        h(ProFormText, { name: 'name', label: '姓名', rules: [{ required: true, message: '请输入姓名' }] }),
        h(ProFormSelect, { name: 'role', label: '角色', options: [{ label: '管理员', value: 'admin' }, { label: '运营', value: 'op' }] }))));
  }

  // ===== ProCard 高级卡片 =====
  const procardEl = document.getElementById('procard-mount');
  if (procardEl && !procardEl.dataset.pkInit) {
    procardEl.dataset.pkInit = '1';
    createRoot(procardEl).render(h(ConfigProvider, { locale: zhCN },
      h('div', { style: { display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 480 } },
        h(ProCard, {
          title: '用户认证服务',
          variant: 'outlined',
          extra: h(ProFormGroup, null,
            h(ProFormSwitch, { name: 'Enable', noStyle: true, checkedChildren: '运行中', unCheckedChildren: '已停止' })
          ),
          tooltip: '管理用户认证与授权的核心服务',
          style: { maxWidth: 300 }
        },
          h('div', null, '实例数量：3'),
          h('div', null, 'CPU 占用：45%'),
          h('div', null, '内存占用：1.2 GB')
        ),
        h(ProCard, {
          title: '订单处理中心',
          extra: 'v2.3.1',
          tooltip: '处理全站订单的创建、支付与履约',
          style: { maxWidth: 300 },
          boxShadow: true
        },
          h('div', null, '日均订单：52 万'),
          h('div', null, '平均延迟：23ms'),
          h('div', null, '成功率：99.97%')
        ),
        h(ProCard, {
          title: '支付网关',
          extra: 'v1.8.0',
          tooltip: '对接第三方支付渠道的统一网关',
          style: { maxWidth: 300 },
          size: 'small'
        },
          h('div', null, '微信支付：已接入'),
          h('div', null, '支付宝：已接入'),
          h('div', null, '银联：接入中')
        ))));
  }

  // ===== ProDescriptions 高级描述 =====
  const prodescEl = document.getElementById('prodescriptions-mount');
  if (prodescEl && !prodescEl.dataset.pkInit) {
    prodescEl.dataset.pkInit = '1';
    createRoot(prodescEl).render(h(ConfigProvider, { locale: zhCN },
      h(ProDescriptions, {
        title: '登记详情', column: 2, style: { maxWidth: 760 },
        dataSource: { no: 'REG-2026091201', name: '张伟', type: '个人登记', status: '正常', time: '2026-09-12 11:18' },
        columns: [
          { title: '单号', dataIndex: 'no', copyable: true },
          { title: '姓名', dataIndex: 'name' },
          { title: '类型', dataIndex: 'type', valueType: 'tag' },
          { title: '状态', dataIndex: 'status', valueEnum: { 正常: { text: '正常', status: 'Success' }, 待处理: { text: '待处理', status: 'Warning' }, 异常: { text: '异常', status: 'Error' } } },
          { title: '登记时间', dataIndex: 'time', valueType: 'dateTime' }
        ]
      })));
  }

  // ===== StatisticCard 统计卡片 =====
  const statcardEl = document.getElementById('statisticcard-mount');
  if (statcardEl && !statcardEl.dataset.pkInit) {
    statcardEl.dataset.pkInit = '1';
    createRoot(statcardEl).render(h(ConfigProvider, { locale: zhCN },
      h('div', { style: { display: 'flex', gap: 16, flexWrap: 'wrap' } },
        h(StatisticCard, { statistic: { title: '今日登记', value: 128 } }),
        h(StatisticCard, { statistic: { title: '待处理', value: 36, valueStyle: { color: '#FAAD14' } } }),
        h(StatisticCard, { statistic: { title: '已完成', value: 1024, valueStyle: { color: '#52C41A' } } }),
        h(StatisticCard, { statistic: { title: '异常', value: 3, valueStyle: { color: '#FF4D4F' } } }))));
  }

  // ===== Breadcrumb 面包屑（纯层级展示，不做返回跳转） =====
  const bcEl = document.getElementById('breadcrumb-mount');
  if (bcEl && !bcEl.dataset.pkInit) {
    bcEl.dataset.pkInit = '1';
    createRoot(bcEl).render(h(ConfigProvider, { locale: zhCN },
      h('div', { style: { maxWidth: 760 } },
        h(Breadcrumb, { items: [{ title: '首页' }, { title: '应用中心' }, { title: '应用列表' }, { title: '应用' }] }))));
  }

  // ===== ProSkeleton 骨架屏 =====
  const psEl = document.getElementById('proskeleton-mount');
  if (psEl && !psEl.dataset.pkInit) {
    psEl.dataset.pkInit = '1';
    createRoot(psEl).render(h(ConfigProvider, { locale: zhCN },
      h('div', { style: { maxWidth: 760 } },
        h('h4', { style: { margin: '0 0 8px', fontWeight: 600 } }, 'list · 列表形态'),
        h(ProSkeleton, { type: 'list' }),
        h('h4', { style: { margin: '24px 0 8px', fontWeight: 600 } }, 'descriptions · 描述形态'),
        h(ProSkeleton, { type: 'descriptions' }),
        h('h4', { style: { margin: '24px 0 8px', fontWeight: 600 } }, 'result · 结果形态'),
        h(ProSkeleton, { type: 'result' }))));
  }

  // ===== DrawerForm 抽屉表单 =====
  mountDemo('drawerform-mount', () => h(DrawerForm, {
    title: '编辑登记', width: 420, trigger: h(Button, { type: 'primary' }, '编辑'), onFinish: async () => true
  },
    h(ProFormText, { name: 'name', label: '姓名', rules: [{ required: true, message: '请输入姓名' }] }),
    h(ProFormSelect, { name: 'dept', label: '部门', options: [{ label: '研发部', value: 'rd' }, { label: '产品部', value: 'pd' }] })));

  // ===== 数据展示组件（antd 真实组件） =====
  mountDemo('avatar-mount', () => h('div', { style: { display: 'flex', gap: 24, alignItems: 'center' } },
    h(Avatar, { size: 40, icon: h(AntIcons.UserOutlined) }),
    h(Avatar, { size: 40, style: { background: '#1677FF' } }, '张'),
    h(Avatar.Group, { max: { count: 3, style: { color: '#1677FF', backgroundColor: '#E6F4FF' } } },
      h(Avatar, { style: { background: '#1677FF' } }, '张'),
      h(Avatar, { style: { background: '#52C41A' } }, '李'),
      h(Avatar, { style: { background: '#FAAD14' } }, '王'),
      h(Avatar, { style: { background: '#722ED1' } }, '赵'))));

  mountDemo('badge-mount', () => h('div', { style: { display: 'flex', gap: 32, alignItems: 'center' } },
    h(Badge, { count: 5 }, h(Avatar, { shape: 'square', icon: h(AntIcons.BellOutlined) })),
    h(Badge, { count: 128, overflowCount: 99, color: '#1677FF' }, h(Avatar, { shape: 'square', icon: h(AntIcons.MailOutlined) })),
    h(Badge, { status: 'success', text: '正常' }),
    h(Badge, { status: 'warning', text: '待处理' }),
    h(Badge, { status: 'error', text: '异常' }),
    h(Badge, { status: 'default', text: '已停用' })));

  mountDemo('descriptions-mount', () => h(Descriptions, {
    title: '登记详情', column: 2, style: { maxWidth: 560 },
    items: [
      { key: 'no', label: '单号', children: 'REG-2026091201' },
      { key: 'name', label: '姓名', children: '张伟' },
      { key: 'type', label: '类型', children: h(Tag, null, '个人登记') },
      { key: 'status', label: '状态', children: h(Badge, { status: 'success', text: '正常' }) },
      { key: 'time', label: '登记时间', children: '2026-09-12 11:18' }
    ]
  }));

  mountDemo('empty-mount', () => h(Empty, { description: '暂无数据' }));

  mountDemo('popover-mount', () => h(Popover, {
    title: '登记说明',
    content: h('div', { style: { maxWidth: 240 } }, '个人登记适用于单人访客；团体登记需填写领队与人数。'),
    trigger: 'click'
  }, h(Button, null, '点击查看气泡卡片')));

  mountDemo('segmented-mount', () => h(Segmented, { options: ['列表', '卡片', '看板'], defaultValue: '列表' }));

  mountDemo('statistic-mount', () => h('div', { style: { display: 'flex', gap: 48, flexWrap: 'wrap' } },
    h(Statistic, { title: '今日登记', value: 128 }),
    h(Statistic, { title: '待处理', value: 36, valueStyle: { color: '#FAAD14' } }),
    h(Statistic, { title: '已完成', value: 1024, valueStyle: { color: '#52C41A' } }),
    h(Statistic, { title: '异常率', value: 2.3, precision: 1, suffix: '%', valueStyle: { color: '#FF4D4F' } })));

  mountDemo('timeline-mount', () => h(Timeline, { style: { maxWidth: 480 }, items: [
    { color: 'green', children: '提交申请 · 张伟 · 2026-09-12 09:40' },
    { color: 'blue', children: '经理审批通过 · 李娜 · 2026-09-12 10:15' },
    { color: 'gray', children: '等待财务复核 · 预计 09-13 完成' }
  ] }));

  mountDemo('tooltip-mount', () => h('div', { style: { display: 'flex', gap: 24, alignItems: 'center' } },
    h(Tooltip, { title: '保存后立即生效' }, h(Button, { type: 'primary' }, '保存')),
    h(Tooltip, { title: '仅仓库管理员可用' }, h(Button, { disabled: true }, '调整库存')),
    h(Tooltip, { title: '查看登记详情' }, h(AntIcons.QuestionCircleOutlined, { style: { fontSize: 16, color: 'var(--text-secondary)' } }))));

  function TourDemo() {
    const ref1 = React.useRef(null);
    const ref2 = React.useRef(null);
    const [open, setOpen] = React.useState(false);
    return h('div', { style: { maxWidth: 560 } },
      h('div', { style: { display: 'flex', gap: 16, marginBottom: 16 } },
        h(Button, { ref: ref1, type: 'primary' }, '新建登记'),
        h(Button, { ref: ref2 }, '导出')),
      h(Tour, { open, onClose: () => setOpen(false), steps: [
        { title: '新建登记', description: '从这里开始创建一条新的登记记录。', target: () => ref1.current },
        { title: '导出数据', description: '把当前列表导出为 Excel 交给同事。', target: () => ref2.current }
      ] }),
      h(Button, { type: 'link', onClick: () => setOpen(true) }, '点击开始漫游式引导'));
  }
  mountDemo('tour-mount', () => h(TourDemo));

  mountDemo('tree-mount', () => h(Tree, {
    checkable: true, defaultExpandAll: true, defaultCheckedKeys: ['rd-fe'], style: { maxWidth: 320 },
    treeData: [
      { title: '研发部', key: 'rd', children: [{ title: '前端组', key: 'rd-fe' }, { title: '后端组', key: 'rd-be' }] },
      { title: '产品部', key: 'pd', children: [{ title: '交互组', key: 'pd-ux' }] },
      { title: '运营部', key: 'op' }
    ]
  }));

  // ===== 反馈组件 =====
  function DrawerDemo() {
    const [open, setOpen] = React.useState(false);
    return h('div', null,
      h(Button, { type: 'primary', onClick: () => setOpen(true) }, '打开抽屉'),
      h(Drawer, { title: '登记详情', width: 380, open, onClose: () => setOpen(false) },
        h('p', null, '抽屉从右侧滑入，承载局部任务或补充信息；关闭后回到列表上下文。')));
  }
  mountDemo('drawer-mount', () => h(DrawerDemo));

  function MessageDemo() {
    const { message } = App.useApp();
    return h('div', { style: { display: 'flex', gap: 12, flexWrap: 'wrap' } },
      h(Button, { onClick: () => message.success('提交成功') }, '成功提示'),
      h(Button, { onClick: () => message.warning('请先补全必填项') }, '警告提示'),
      h(Button, { onClick: () => message.error('网络异常，请重试') }, '错误提示'));
  }
  mountDemo('message-mount', () => h(App, null, h(MessageDemo)));

  function NotificationDemo() {
    const { notification } = App.useApp();
    return h('div', { style: { display: 'flex', gap: 12, flexWrap: 'wrap' } },
      h(Button, { type: 'primary', onClick: () => notification.success({ message: '审批通过', description: '张伟的登记申请已通过，等待财务复核。' }) }, '成功通知'),
      h(Button, { onClick: () => notification.info({ message: '新的待办', description: '有 3 条登记等待你处理。' }) }, '信息通知'));
  }
  mountDemo('notification-mount', () => h(App, null, h(NotificationDemo)));

  mountDemo('popconfirm-mount', () => h('div', { style: { display: 'flex', gap: 12 } },
    h(Popconfirm, { title: '确定删除该记录吗？', okText: '删除', cancelText: '取消', okButtonProps: { danger: true } },
      h(Button, { danger: true }, '删除')),
    h(Popconfirm, { title: '确认提交？', okText: '提交', cancelText: '取消' },
      h(Button, { type: 'primary' }, '提交'))));

  mountDemo('progress-mount', () => h('div', { style: { maxWidth: 480 } },
    h(Progress, { percent: 60 }),
    h(Progress, { percent: 75, status: 'active' }),
    h(Progress, { percent: 30, status: 'exception' }),
    h(Progress, { type: 'circle', percent: 75, style: { marginTop: 16 } })));

  mountDemo('result-mount', () => h(Result, {
    status: 'success', title: '提交成功',
    subTitle: '登记编号 REG-2026091201，可在列表中查看进度。',
    extra: [h(Button, { type: 'primary', key: 'list' }, '查看列表'), h(Button, { key: 'home' }, '返回首页')]
  }));

  mountDemo('spin-mount', () => h('div', { style: { maxWidth: 480 } },
    h(Spin, { tip: '加载中…' },
      h('div', { style: { padding: 32, border: '1px solid var(--outline-variant)', borderRadius: 8, color: 'var(--text-secondary)' } }, '内容区域加载中')),
    h('div', { style: { marginTop: 16, color: 'var(--text-secondary)' } },
      h(Spin, { size: 'small' }), ' 小尺寸用于局部加载')));

  mountDemo('watermark-mount', () => h(Watermark, { content: 'Pkuse Design', fontColor: 'rgba(0, 0, 0, 0.08)' },
    h('div', { style: { height: 200, border: '1px solid var(--outline-variant)', borderRadius: 8, display: 'grid', placeItems: 'center', color: 'var(--text-secondary)' } }, '被水印覆盖的内容区域')));

  mountDemo('alert-mount', () => h('div', { style: { maxWidth: 560 } },
    h(Alert, { type: 'success', showIcon: true, message: '成功提示', description: '操作已完成，数据已保存。' }),
    h(Alert, { type: 'info', showIcon: true, message: '信息提示', description: '这是一条常规信息。', style: { marginTop: 12 } }),
    h(Alert, { type: 'warning', showIcon: true, message: '警告提示', description: '请检查填写内容。', style: { marginTop: 12 } }),
    h(Alert, { type: 'error', showIcon: true, message: '错误提示', description: '提交失败，请稍后重试。', closable: true, style: { marginTop: 12 } })));

  // ===== 其他组件 =====
  mountDemo('affix-mount', () => h('div', { style: { maxWidth: 560 } },
    h(Affix, { offsetTop: 8 },
      h('div', { style: { display: 'flex', gap: 8, padding: 8, background: '#fff', border: '1px solid var(--outline-variant)', borderRadius: 8 } },
        h(Button, { type: 'primary', size: 'small' }, '批量盘点'),
        h(Button, { size: 'small' }, '导出'),
        h(Button, { size: 'small' }, '打印标签'))),
    h('p', { style: { marginTop: 16, color: 'var(--text-secondary)' } }, '向下滚动页面时，操作栏将固定在视口顶部。')));

  function AppDemo() {
    const { modal, message } = App.useApp();
    return h('div', { style: { display: 'flex', gap: 12, flexWrap: 'wrap' } },
      h(Button, { type: 'primary', onClick: () => modal.confirm({ title: '确认提交？', content: '提交后不可撤销。', okText: '提交', cancelText: '取消' }) }, '弹确认框（App.modal）'),
      h(Button, { onClick: () => message.success('操作成功') }, '全局提示（App.message）'));
  }
  mountDemo('app-mount', () => h(App, null, h(AppDemo)));

  mountDemo('borderbeam-mount', () => h('div', { style: { display: 'flex', flexDirection: 'column', gap: 16, maxWidth: 480 } },
    h(BorderBeam, { count: 3 },
      h(Card, { title: '多光束', style: { width: '100%' } },
        h('div', null, '设置 count 可在容器边框上均匀分布多条光束。'))),
    h(BorderBeam, { count: 2 },
      h(Card, { title: '多光束', style: { width: '100%' } },
        h('div', null, '设置 count 可在容器边框上均匀分布多条光束。')))));

  mountDemo('button-mount', () => h('div', { className: 'btn-row' },
    h(Button, { type: 'primary' }, '主按钮'),
    h(Button, null, '次按钮'),
    h(Button, { variant: 'dashed' }, '虚线按钮'),
    h(Button, { type: 'text' }, '文字按钮'),
    h(Button, { type: 'link' }, '链接按钮'),
    h(Button, { danger: true, type: 'primary' }, '危险按钮'),
    h(Button, { disabled: true }, '禁用按钮')));

  // ===== 新建/编辑表单 操作按钮（真实 antd Button，点击特效与组件一致） =====
  const backActionsMount = document.getElementById('back-actions-mount');
  if (backActionsMount && !backActionsMount.dataset.pkInit) {
    backActionsMount.dataset.pkInit = '1';
    createRoot(backActionsMount).render(
      h(ConfigProvider, { locale: zhCN },
        h('div', { style: { display: 'flex', gap: 8 } },
          h(Button, { onClick: () => { if (window.saveDraft) window.saveDraft(); } }, '暂 存'),
          h(Button, { type: 'primary', onClick: () => { if (window.submitEntry) window.submitEntry(); } }, '提 交'),
          h(Button, { onClick: () => { if (window.resetEntry) window.resetEntry(); } }, '重 置'))));
  }

  // ===== 新建/编辑表单 表单主体（ProForm，组件与交互能力和复杂数据展示同源） =====
  // 版式参考「运营管理平台」手工录入表单页：分组标题 + 两列栅格（栅格由 theme.css 的 .frm 控制），标签 84px 右对齐
  const sceneFormMount = document.getElementById('scene-form-mount');
  if (sceneFormMount && !sceneFormMount.dataset.pkInit) {
    sceneFormMount.dataset.pkInit = '1';
    const sceneFormRef = React.createRef();
    createRoot(sceneFormMount).render(
      h(ConfigProvider, { locale: zhCN },
          h(ProForm, {
            className: 'frm',
            formRef: sceneFormRef,
            layout: 'horizontal',
            colon: false,
            labelCol: { flex: '0 0 84px' },
          wrapperCol: { flex: '1 1 0', minWidth: 0 },
          submitter: false,
          onFinish: async (values) => {
            if (window.showToast) window.showToast('提交成功：' + values.name + ' · ' + (values.regType || '个人登记'));
            if (sceneFormRef.current) sceneFormRef.current.resetFields();
          }
        },
          h('div', { className: 'sect-title' }, '基础信息'),
          h(ProFormText, { name: 'name', label: '姓名', placeholder: '请输入姓名', fieldProps: { allowClear: true, maxLength: 20 }, rules: [{ required: true, message: '请输入姓名' }] }),
          h(ProFormText, { name: 'phone', label: '手机号', placeholder: '请输入11位手机号', fieldProps: { allowClear: true, maxLength: 11 }, rules: [{ required: true, message: '请输入手机号' }, { pattern: /^1\d{10}$/, message: '请输入正确的11位手机号' }] }),
          h(ProFormSelect, { name: 'dept', label: '部门', placeholder: '请选择部门', fieldProps: { allowClear: true }, options: [{ label: '研发部', value: '研发部' }, { label: '产品部', value: '产品部' }, { label: '运营部', value: '运营部' }] }),
          h(ProFormRadio.Group, { name: 'regType', label: '登记类型', initialValue: '个人登记', options: [{ label: '个人登记', value: '个人登记' }, { label: '团体登记', value: '团体登记' }] }),
          h('div', { className: 'sect-title' }, '登记信息'),
          h(ProFormDatePicker, { name: 'entryDate', label: '入职日期', placeholder: '请选择日期', fieldProps: { style: { width: '100%' } } }),
          h(ProFormDigit, { name: 'companions', label: '随行人数', initialValue: 1, extra: '可选 · 默认 1 人，范围 1–99', fieldProps: { min: 1, max: 99, precision: 0 } }),
          h(ProFormSwitch, { name: 'pickup', label: '需要接送' }),
          // 复选框组的选项必须带 value（组件内部按 value 建映射，缺省会导致整组不显示）
          h(ProFormCheckbox.Group, { name: 'devices', label: '随行设备', options: [{ label: '相机', value: '相机' }, { label: '三脚架', value: '三脚架' }, { label: '无人机', value: '无人机' }] }),
          h(ProFormRate, { name: 'serviceRate', label: '服务评分' }),
          h(ProFormSlider, { name: 'weight', label: '物品重量', min: 0, max: 30, extra: '可选 · 单位 kg，范围 0–30' }),
          h('div', { className: 'sect-title' }, '辅助信息'),
          h('div', { className: 'span-2' },
            h(ProFormTextArea, { name: 'remark', label: '备注', placeholder: '选填，补充说明信息', fieldProps: { rows: 2, allowClear: true } })),
          h('div', { className: 'span-2' },
            h(ProFormUploadDragger, { name: 'attachment', max: 1, fieldProps: { beforeUpload: () => false } })))));
    setTimeout(function () {
      const push = function () {
        if (window.setSceneFormRef) { window.setSceneFormRef(sceneFormRef); } else { setTimeout(push, 50); }
      };
      push();
    }, 0);
  }

  // ===== 新建/编辑表单 面包屑（层级位置展示，不做返回链接；样式对齐 breadcrumb style-class demo） =====
  const sceneBreadcrumbMount = document.getElementById('scene-breadcrumb-mount');
  if (sceneBreadcrumbMount && !sceneBreadcrumbMount.dataset.pkInit) {
    sceneBreadcrumbMount.dataset.pkInit = '1';
    createRoot(sceneBreadcrumbMount).render(
      h(ConfigProvider, { locale: zhCN },
        h(Breadcrumb, {
          items: [{ title: '新建表单' }],
          styles: {
            root: { padding: 0 },
            item: { color: '#1890ff' },
            separator: { color: 'rgba(0, 0, 0, 0.45)' }
          }
        })));
  }

  // ===== 应用框架：顶栏一级导航 + 侧边菜单（按 Figma「产品」设计还原） =====
  const appNavMount = document.getElementById('app-nav-mount');
  if (appNavMount && !appNavMount.dataset.pkInit) {
    appNavMount.dataset.pkInit = '1';
    const navItems = [
      { label: '首页', on: true },
      { label: '执法线索管理' },
      { label: '执法行为管理' },
      { label: '执法结果管理' },
      { label: '执法协作管理' },
      { label: '执法辅助支撑' },
      { label: '执法行为预警监督' },
      { label: '低代码配置引擎' },
      { label: '执法评价反馈' }
    ];
    createRoot(appNavMount).render(
      h(ConfigProvider, { locale: zhCN },
        h('nav', { style: { display: 'flex', alignItems: 'center', flex: 1, minWidth: 0 } },
          navItems.map((n, idx) => h('span', { className: 'nav-item' + (n.on ? ' on' : ''), key: idx },
            n.label)))));
  }

  const siderMenuMount = document.getElementById('af-sider-menu-mount');
  if (siderMenuMount && !siderMenuMount.dataset.pkInit) {
    siderMenuMount.dataset.pkInit = '1';
    const page = location.pathname.split('/').pop();
    const links = [
      { label: '新建/编辑表单', href: 'scene-entry.html', icon: 'FormOutlined' },
      { label: '复杂数据展示', href: 'scene-display.html', icon: 'TableOutlined' }
    ];
    const kids = [];
    links.forEach(function (l) {
      kids.push(h('a', { className: 'af-menu-item' + (l.href === page ? ' on' : ''), href: l.href, key: l.href, title: l.label },
        h(AntIcons[l.icon]), h('span', null, l.label)));
    });
    createRoot(siderMenuMount).render(
      h(ConfigProvider, { locale: zhCN }, h('nav', null, kids)));
  }

  mountDemo('tabs-mount', () => h(Tabs, { items: [
    { key: '1', label: '标签一', children: h('p', { style: { margin: 0 } }, '标签一的内容区域') },
    { key: '2', label: '标签二', children: h('p', { style: { margin: 0 } }, '标签二的内容区域') },
    { key: '3', label: '标签三', children: h('p', { style: { margin: 0 } }, '标签三的内容区域') }
  ] }));

  mountDemo('dropdown-mount', () => h(Dropdown, {
    menu: { items: [
      { key: '1', label: '编辑' },
      { key: '2', label: '复制' },
      { type: 'divider' },
      { key: '3', label: '删除', danger: true }
    ] }
  }, h(Button, null, h(AntIcons.DownOutlined), ' 下拉菜单')));

  mountDemo('tag-mount', () => h('div', { className: 'btn-row' },
    h(Tag, null, '默认标签'),
    h(Tag, { color: 'blue' }, '标签 · blue'),
    h(Tag, { color: 'green' }, '标签 · green'),
    h(Tag, { closable: true }, '可关闭标签')));

  // ===== 数据录入组件 =====
  const CASCADER_OPTIONS = [
    { value: 'east', label: '华东区', children: [{ value: 'sh', label: '上海仓' }, { value: 'hz', label: '杭州仓' }] },
    { value: 'north', label: '华北区', children: [{ value: 'bj', label: '北京仓' }, { value: 'tj', label: '天津仓' }] },
    { value: 'south', label: '华南区', children: [{ value: 'gz', label: '广州仓' }, { value: 'sz', label: '深圳仓' }] }
  ];
  mountDemo('cascader-mount', () => h('div', { style: { maxWidth: 480 } },
    h('h4', { style: { margin: '0 0 8px', fontWeight: 600 } }, '单选'),
    h(Cascader, { placeholder: '请选择', options: CASCADER_OPTIONS, style: { width: 240 } }),
    h('h4', { style: { margin: '24px 0 8px', fontWeight: 600 } }, '多选'),
    h(Cascader, { multiple: true, maxTagCount: 'responsive', placeholder: '请选择（可多选）', options: CASCADER_OPTIONS, style: { width: '100%' } })));

  mountDemo('slider-mount', () => h(Slider, { defaultValue: 30, marks: { 0: '0', 30: '30', 60: '60' }, max: 60 }));

  function TransferDemo() {
    const [keys, setKeys] = React.useState(['a']);
    const list = [
      { key: 'a', title: '用户管理' }, { key: 'b', title: '角色权限' },
      { key: 'c', title: '操作日志' }, { key: 'd', title: '系统设置' }
    ];
    return h(Transfer, { dataSource: list, targetKeys: keys, onChange: (k) => setKeys(k),
      render: (item) => item.title, titles: ['待分配', '已分配'] });
  }
  mountDemo('transfer-mount', () => h(TransferDemo));

  mountDemo('treeselect-mount', () => h(TreeSelect, {
    placeholder: '请选择部门', style: { width: 280 }, treeDefaultExpandAll: true,
    treeData: [
      { title: '研发部', value: 'rd', children: [{ title: '前端组', value: 'rd-fe' }, { title: '后端组', value: 'rd-be' }] },
      { title: '产品部', value: 'pd' }
    ]
  }));

  mountDemo('upload-mount', () => h(Upload, {
    beforeUpload: () => false,
    defaultFileList: [
      { uid: '1', name: 'xxx.png', status: 'uploading', percent: 33, url: 'http://www.baidu.com/xxx.png' },
      { uid: '2', name: 'yyy.png', status: 'done', url: 'http://www.baidu.com/yyy.png' },
      { uid: '3', name: 'zzz.png', status: 'error', response: 'Server Error 500', url: 'http://www.baidu.com/zzz.png' }
    ],
    children: h(Button, { icon: h(AntIcons.UploadOutlined) }, '上传')
  }));
}

window.__pkRender = renderAll;
renderAll();
