(function () {
  var nav = document.getElementById('site-nav');
  if (!nav) return;
  var pages = [
    ['overview', '概述'],
    ['values', '价值观'],
    ['colors', '色彩'],
    ['type', '字体'],
    ['layout', '布局'],
    ['elevation', '层级与深度'],
    ['shapes', '形状'],
    ['components', '组件'],
    ['scenes', '场景', [
      ['scene-entry', '数据录入'],
      ['scene-simple', '简易数据展示'],
      ['scene-display', '复杂数据展示']
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
        var active = c[0] === current ? ' class="active"' : '';
        html += '<a class="nav-child" href="' + c[0] + '.html"' + active + '>' + c[1] + '</a>';
      });
      return;
    }
    var active = p[0] === current ? ' class="active"' : '';
    html += '<a href="' + p[0] + '.html"' + active + '>' + p[1] + '</a>';
  });
  nav.innerHTML = html;
})();
