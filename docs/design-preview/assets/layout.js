(function () {
  var nav = document.getElementById('site-nav');
  if (!nav) return;
  var pages = [
    ['principles', '设计原则'],
    ['design-tokens', '设计令牌', [
      ['colors', '色彩'],
      ['type', '字体'],
      ['layout', '间距'],
      ['elevation', '层级与深度'],
      ['shapes', '形状'],
      ['icons', '图标']
    ]],
    ['app-layout', '布局', 'demo'],
    ['components', '组件', [
      ['通用', [['button', 'Button - 按钮'], ['proskeleton', 'Skeleton - 骨架屏']]],
      ['导航', [['breadcrumb', 'Breadcrumb - 面包屑'], ['tabs', 'Tabs - 标签页'], ['dropdown', 'Dropdown - 下拉菜单']]],
      ['数据录入', [
        ['cascader', 'Cascader - 级联选择'],
        ['form', 'FormFields - 表单项'],
        ['slider', 'Slider - 滑动输入条'],
        ['transfer', 'Transfer - 穿梭框'],
        ['treeselect', 'TreeSelect - 树选择'],
        ['upload', 'Upload - 上传']
      ]],
      ['数据展示', [
        ['avatar', 'Avatar - 头像'],
        ['badge', 'Badge - 徽标数'],
        ['card', 'Card - 卡片'],
        ['descriptions', 'Descriptions - 描述列表'],
        ['empty', 'Empty - 空状态'],
        ['popover', 'Popover - 气泡卡片'],
        ['segmented', 'Segmented - 分段控制器'],
        ['statistic', 'Statistic - 统计数值'],
        ['table', 'Table - 表格'],
        ['tag', 'Tag - 标签'],
        ['timeline', 'Timeline - 时间轴'],
        ['tooltip', 'Tooltip - 文字提示'],
        ['tour', 'Tour - 漫游式引导'],
        ['tree', 'Tree - 树形控件']
      ]],
      ['反馈', [
        ['alert', 'Alert - 警告提示'],
        ['drawer', 'Drawer - 抽屉'],
        ['message', 'Message - 全局提示'],
        ['modal', 'Modal - 对话框'],
        ['notification', 'Notification - 通知提醒框'],
        ['popconfirm', 'Popconfirm - 气泡确认框'],
        ['progress', 'Progress - 进度条'],
        ['result', 'Result - 结果'],
        ['spin', 'Spin - 加载中'],
        ['watermark', 'Watermark - 水印']
      ]],
      ['其他', [
        ['affix', 'Affix - 固钉'],
        ['app', 'App - 包裹组件'],
        ['borderbeam', 'BorderBeam - 边框流光']
      ]]
    ]],
    ['scenes', '页面模版', [
      ['scene-entry', '新建/编辑表单'],
      ['scene-simple', '简易数据展示'],
      ['scene-display', '复杂数据展示']
    ]],
    ['rules', '对与错'],
    ['customize', '定制']
  ];
  var current = document.body.dataset.page || '';
  var html = '<p class="brand">PKUSE 设计规范</p>';
  pages.forEach(function (p) {
    if (p[2] === 'demo') {
      html += '<a href="javascript:void(0)" class="nav-demo" data-demo="' + p[0] + '">' + p[1] + '</a>';
      return;
    }
    if (p[2]) {
      html += '<p class="nav-group">' + p[1] + '</p>';
      p[2].forEach(function (c) {
        if (Object.prototype.toString.call(c[1]) === '[object Array]') {
          html += '<p class="nav-subgroup">' + c[0] + '</p>';
          c[1].forEach(function (item) {
            var subActive = item[0] === current ? ' active' : '';
            html += '<a class="nav-child nav-child-deep' + subActive + '" href="' + item[0] + '.html">' + item[1] + '</a>';
          });
          return;
        }
        var active = c[0] === current ? ' active' : '';
        html += '<a class="nav-child' + active + '" href="' + c[0] + '.html">' + c[1] + '</a>';
      });
      return;
    }
    var active = p[0] === current ? ' class="active"' : '';
    html += '<a href="' + p[0] + '.html"' + active + '>' + p[1] + '</a>';
  });
  nav.innerHTML = html;

  function showLayoutDemo(link) {
    var main = document.querySelector('main');
    if (!main) return;
    main.innerHTML = '';
    var frame = document.createElement('iframe');
    frame.src = 'layout-demo.html';
    frame.title = '布局演示';
    frame.style.cssText = 'width:100%;height:calc(100vh - 112px);border:0;display:block;border-radius:8px;background:var(--surface-layout)';
    main.appendChild(frame);
    nav.querySelectorAll('a').forEach(function (a) { a.classList.remove('active'); });
    if (link) link.classList.add('active');
    window.scrollTo(0, 0);
  }

  nav.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('.nav-demo') : null;
    if (!link) return;
    e.preventDefault();
    showLayoutDemo(link);
  });
})();
