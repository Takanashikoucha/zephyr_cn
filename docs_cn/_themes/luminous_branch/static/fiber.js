/* 荧枝 · 纤维画布引擎
 * 确定性种子，可复现的发光纤维背景
 */
(function() {
  'use strict';

  // 确定性随机数生成器
  function makeRng(seed) {
    let s = seed;
    return function() {
      s = (s * 1103515245 + 12345) & 0x7fffffff;
      return s / 0x7fffffff;
    };
  }

  // 高斯分布（中心极限定理近似）
  function makeGauss(rnd) {
    return function() {
      return (rnd() + rnd() + rnd() + rnd() - 2) / 2;
    };
  }

  // 三色族
  const BLUE = [
    'rgba(150,215,255,1)', 'rgba(110,190,255,1)', 'rgba(185,232,255,1)',
    'rgba(80,165,250,1)', 'rgba(130,205,255,1)'
  ];
  const RED = [
    'rgba(255,70,100,1)', 'rgba(255,110,110,1)', 'rgba(235,45,75,1)',
    'rgba(255,140,130,1)', 'rgba(255,90,95,1)'
  ];
  const WHITE = [
    'rgba(235,250,255,1)', 'rgba(210,240,255,1)'
  ];

  // 族选择（加权交替，排除上一族防止大块单色）
  function makePickFam(rnd, redBias) {
    return function(prev) {
      const r = rnd();
      const blueThresh = 0.5 + (redBias || 0);
      const redThresh = 0.82 + (redBias || 0);
      if (prev !== 'B' && r < blueThresh) return 'B';
      if (prev !== 'R' && r >= blueThresh && r < redThresh) return 'R';
      if (prev !== 'B') return 'B';
      if (prev !== 'R') return 'R';
      return 'W';
    };
  }

  // 单根纤维（贝塞尔曲线）
  function fiber(ctx, x, y, a, len, color, width, alpha, gauss) {
    const dx = Math.cos(a), dy = Math.sin(a);
    const px = -dy, py = dx;
    const bow = gauss() * len * 0.25;
    const c1x = x + dx * len * 0.33 + px * bow * 0.4;
    const c1y = y + dy * len * 0.33 + px * bow * 0.4;
    const c2x = x + dx * len * 0.7 + px * bow;
    const c2y = y + dy * len * 0.7 + px * bow * 0.8;
    const ex = x + dx * len + px * bow * 1.2;
    const ey = y + dy * len + px * bow;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.bezierCurveTo(c1x, c1y, c2x, c2y, ex, ey);
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.globalAlpha = alpha;
    ctx.lineCap = 'round';
    ctx.stroke();
  }

  /**
   * 初始化纤维画布
   * @param {HTMLCanvasElement} canvasEl - 目标 canvas 元素
   * @param {object} opts - { seed: number, redBias: number }
   */
  window.initFiber = function(canvasEl, opts) {
    if (!canvasEl || !canvasEl.getContext) return;
    const ctx = canvasEl.getContext('2d');
    const seed = (opts && opts.seed) || 7;
    const redBias = (opts && opts.redBias) || 0;

    // 设置画布尺寸（跟随容器）
    const rect = canvasEl.getBoundingClientRect();
    const w = rect.width || canvasEl.width || 800;
    const h = rect.height || canvasEl.height || 400;
    canvasEl.width = w;
    canvasEl.height = h;

    const rnd = makeRng(seed);
    const gauss = makeGauss(rnd);
    const pickFam = makePickFam(rnd, redBias);

    // 铺设参数（荧枝指纹——除 seed 和红族权重外勿改）
    const step = 26;
    const overflow = 30;

    // 主纤维场
    let prev = '';
    for (let y = -overflow; y < h + overflow; y += step) {
      for (let x = -overflow; x < w + overflow; x += step) {
        const count = 1 + Math.floor(rnd() * 2); // 1-2 根
        for (let i = 0; i < count; i++) {
          const a = rnd() * Math.PI * 2;
          const len = 90 + rnd() * 150;
          const width = 4.5 + rnd() * 4.5;
          const alpha = 0.22 + rnd() * 0.16;
          const fam = pickFam(prev);
          prev = fam;
          const palette = fam === 'B' ? BLUE : fam === 'R' ? RED : WHITE;
          const color = palette[Math.floor(rnd() * palette.length)];
          fiber(ctx, x, y, a, len, color, width, alpha, gauss);
        }
      }
    }

    // 顶部火花纤维（120 根更亮的）
    for (let i = 0; i < 120; i++) {
      const x = rnd() * w;
      const y = rnd() * h * 0.5;
      const a = rnd() * Math.PI * 2;
      const len = 110 + rnd() * 140;
      const width = 2 + rnd() * 3;
      const alpha = 0.2 + rnd() * 0.14;
      const fam = pickFam(prev);
      prev = fam;
      const palette = fam === 'B' ? BLUE : fam === 'R' ? RED : WHITE;
      const color = palette[Math.floor(rnd() * palette.length)];
      fiber(ctx, x, y, a, len, color, width, alpha, gauss);
    }

    ctx.globalAlpha = 1;
  };
})();
