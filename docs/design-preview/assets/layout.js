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
    ['app-layout', '布局'],
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
      ['scene-entry', '新建/编辑表单', 'blank'],
      ['scene-display', '复杂数据展示', 'blank']
    ]],
    ['rules', '对与错'],
    ['customize', '定制']
  ];
  var current = document.body.dataset.page || '';
  var html = '<p class="brand">PKUSE 设计规范</p>';
  pages.forEach(function (p) {
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
        var target = c[2] === 'blank' ? ' target="_blank"' : '';
        html += '<a class="nav-child' + active + '" href="' + c[0] + '.html"' + target + '>' + c[1] + '</a>';
      });
      return;
    }
    var active = p[0] === current ? ' class="active"' : '';
    html += '<a href="' + p[0] + '.html"' + active + '>' + p[1] + '</a>';
  });
  nav.innerHTML = html;

  // ===== 局部刷新：点击菜单只替换右侧内容区，左侧导航不重载 =====
  // file:// 协议下浏览器禁止 fetch 本地文件，保持原生跳转（双击 index.html 离线浏览不受影响）
  if (location.protocol === 'file:') return;

  var swapping = false;

  function setActive(href) {
    nav.querySelectorAll('a').forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === href);
    });
  }

  function ensureVendor(doc) {
    var need = doc.querySelector('script[src*="vendor/protable"]');
    var have = document.querySelector('script[src*="vendor/protable"], script[data-pk-vendor]');
    if (!need || (have && window.__pkRender)) return Promise.resolve();
    var s = document.createElement('script');
    s.src = need.getAttribute('src');
    s.dataset.pkVendor = '1';
    return new Promise(function (resolve) {
      s.onload = s.onerror = function () { resolve(); };
      document.body.appendChild(s);
    });
  }

  function swapPage(href, push) {
    if (swapping) return;
    swapping = true;
    fetch(href).then(function (res) {
      if (!res.ok) throw new Error('HTTP ' + res.status);
      return res.text();
    }).then(function (text) {
      var doc = new DOMParser().parseFromString(text, 'text/html');
      // 1) .shell 骨架整体保留（导航元素不重建、滚动位置自然保留），只替换它里面除导航外的内容
      var shell = document.querySelector('.shell');
      var newShell = doc.querySelector('.shell');
      if (!shell || !newShell) throw new Error('shell missing');
      Array.prototype.slice.call(shell.children).forEach(function (child) {
        if (child.id !== 'site-nav') child.remove();
      });
      Array.prototype.slice.call(newShell.children).forEach(function (child) {
        if (child.id === 'site-nav') return;
        shell.appendChild(document.adoptNode(child));
      });
      // 2) body 顶层的其他动态节点（如 提示 toast）一并替换
      Array.prototype.slice.call(document.body.children).forEach(function (child) {
        if (child.tagName === 'SCRIPT' || child.classList.contains('shell')) return;
        child.remove();
      });
      Array.prototype.slice.call(doc.body.children).forEach(function (child) {
        if (child.tagName === 'SCRIPT' || child.classList.contains('shell')) return;
        document.body.appendChild(document.adoptNode(child));
      });
      // 3) 重执行新页面携带的内联脚本（如 新建/编辑表单 的表单交互）
      doc.body.querySelectorAll('script:not([src])').forEach(function (old) {
        var s = document.createElement('script');
        s.textContent = old.textContent;
        document.body.appendChild(s);
      });
      document.title = doc.title;
      setActive(href);
      window.scrollTo(0, 0);
      return ensureVendor(doc).then(function () {
        if (window.__pkRender) window.__pkRender();
      });
    }).then(function () {
      swapping = false;
      if (push !== false) history.pushState({}, '', href);
    }).catch(function () {
      swapping = false;
      // 任何一步失败（离线、404 等）回退为原生跳转
      location.href = href;
    });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href$=".html"]');
    if (!a || a.target === '_blank' || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    swapPage(a.getAttribute('href'));
  });

  window.addEventListener('popstate', function () {
    var file = location.pathname.split('/').pop() || 'principles.html';
    swapPage(file, false);
  });
})();
