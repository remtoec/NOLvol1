# -*- coding: utf-8 -*-
"""Generate a self-contained, mobile-optimized Traditional-Chinese reader (index.html)
from NOL.txt. Strips the leading "N\\t" line-number prefix from each paragraph and
embeds the text directly into the HTML so the result is fully portable/offline."""

import html
import re
from pathlib import Path

SRC = Path(__file__).with_name("NOL.txt")
OUT = Path(__file__).with_name("index.html")

line_re = re.compile(r"^\s*(\d+)\t(.*)$")

paras = []
for raw in SRC.read_text(encoding="utf-8").splitlines():
    if not raw.strip():
        continue
    m = line_re.match(raw)
    if m:
        n, body = m.group(1), m.group(2)
    else:
        # Fallback: no number prefix -> append to previous paragraph if any
        n, body = (str(len(paras) + 1), raw.strip())
    body = html.escape(body.strip())
    paras.append((int(n), body))

paras.sort(key=lambda x: x[0])
last_n = paras[-1][0] if paras else 0

paras_html = "\n".join(
    f'<p class="para" id="p{n}" data-n="{n}">'
    f'<button class="pnum" type="button" data-n="{n}" '
    f'title="複製此段連結" aria-label="複製第 {n} 段連結">{n}</button>'
    f'<span class="ptext">{body}</span></p>'
    for n, body in paras
)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<title>愛的本質 · 第一卷　第一章 — Irving Singer</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Body face: LXGW WenKai TC (霞鶩文楷) — warm hand-brushed Kai, loaded async & subset, non-blocking -->
<link rel="preload" as="style" href="https://cdn.jsdelivr.net/npm/@fontsource/lxgw-wenkai-tc@5/400.css" onload="this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/lxgw-wenkai-tc@5/400.css"></noscript>
<!-- Masthead title only: Noto Serif TC (Ming authority) -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@600;700&display=swap" rel="stylesheet">
<style>
:root{
  --fs: 20px;
  --ease-out:cubic-bezier(.23,1,.32,1);
  --bg:#f7f4ec; --panel:#fffdf8; --ink:#26221c; --ink-soft:#6f685c;
  --rule:#e3dccd; --accent:#9a3b2e; --accent-soft:#d8c7a6; --flash:#fbe9c9;
  --bar:#9a3b2e; --chip:#ead9bf; --sel:#f4dfa6;
}
body.theme-light{ --bg:#f6f1e7; --panel:#fffdf8; --ink:#2b2620; --ink-soft:#6f685c; --rule:#e3dccd; --accent:#9a3b2e; --accent-soft:#d8c7a6; --flash:#fbe9c9; --bar:#9a3b2e; --chip:#ead9bf; --sel:#f4dfa6; }
body.theme-sepia{ --bg:#ece0c8; --panel:#f5ead2; --ink:#3a2f1d; --ink-soft:#6b5a3a; --rule:#d8c39a; --accent:#8a4a22; --accent-soft:#cdb286; --flash:#f0dcae; --bar:#8a4a22; --chip:#e0c79a; --sel:#e7cd92; }
body.theme-dark{ --bg:#1b1814; --panel:#22201a; --ink:#d8d0c0; --ink-soft:#8f8878; --rule:#343026; --accent:#e0916f; --accent-soft:#5a4d39; --flash:#3a3220; --bar:#e0916f; --chip:#3a3024; --sel:#4a3f2c; }

::selection{ background:var(--sel); }
::-moz-selection{ background:var(--sel); }

/* metric-matched fallback so the swap from system Songti -> LXGW WenKai TC doesn't reflow the column */
@font-face{
  font-family:"CJK Fallback";
  src:local("Songti TC"),local("PingFang TC"),local("Microsoft JhengHei"),local("PMingLiU");
  size-adjust:100%; ascent-override:88%; descent-override:12%; line-gap-override:0%;
}

*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; }
body{
  background:var(--bg); color:var(--ink);
  font-family:"LXGW WenKai TC","CJK Fallback","Noto Serif TC","Source Han Serif TC","Songti TC","Songti SC","PMingLiU","MingLiU",serif;
  -webkit-text-size-adjust:100%; text-rendering:optimizeLegibility;
  transition:background .25s ease,color .25s ease;
}

/* ---- progress bar ---- */
#progress{
  position:fixed; top:0; left:0; height:3px; width:0;
  background:var(--bar); z-index:50; transition:width .08s linear;
}

/* ---- toolbar ---- */
#bar{
  position:sticky; top:0; z-index:40;
  display:flex; align-items:center; justify-content:center; gap:5px; flex-wrap:wrap;
  padding:9px max(6px,env(safe-area-inset-left)) 9px max(6px,env(safe-area-inset-right));
  background:color-mix(in srgb,var(--panel) 85%,transparent);
  -webkit-backdrop-filter:saturate(1.3) blur(10px);
  backdrop-filter:saturate(1.3) blur(10px);
  border-bottom:1px solid var(--rule);
}
/* grouped "pill" containers */
.group,.seg-toggle{
  display:inline-flex; align-items:center;
  background:var(--panel); border:1px solid var(--rule);
  border-radius:12px; padding:3px;
  box-shadow:0 1px 1px rgba(0,0,0,.04);
}
.seg{
  appearance:none; -webkit-appearance:none; border:0; background:transparent; color:var(--ink);
  height:36px; min-width:36px; padding:0 7px; border-radius:9px;
  font-family:inherit; font-size:15px; line-height:1; cursor:pointer;
  display:inline-flex; align-items:center; justify-content:center; gap:5px;
  -webkit-tap-highlight-color:transparent;
  transition:transform 140ms var(--ease-out), background-color 160ms ease, color 160ms ease;
}
.seg:active{ transform:scale(.94); }
@media (hover:hover) and (pointer:fine){
  .seg:hover{ background:var(--chip); }
}
.theme-seg{ min-width:36px; padding:0; }
.theme-seg .ticon{ font-size:17px; line-height:1; }
.seg .sub{ font-size:.82em; }

/* sliding layout toggle 直 / 橫 */
.seg-toggle{ position:relative; }
.seg-toggle .seg{ position:relative; z-index:1; width:38px; min-width:38px; padding:0; color:var(--ink-soft); }
.seg-toggle .thumb{
  position:absolute; top:3px; left:3px; width:38px; height:36px; border-radius:9px;
  background:var(--chip); z-index:0;
  transition:transform 240ms var(--ease-out);
}
body.vertical    #layoutToggle .thumb{ transform:translateX(0); }
body:not(.vertical) #layoutToggle .thumb{ transform:translateX(38px); }
body.vertical    #layoutToggle .seg[data-layout="v"]{ color:var(--accent); font-weight:700; }
body:not(.vertical) #layoutToggle .seg[data-layout="h"]{ color:var(--accent); font-weight:700; }

/* jump-to-paragraph */
.group.jump{ gap:3px; padding-inline:6px 3px; }
.jump .jlabel{ font-size:13px; color:var(--ink-soft); }
.jump input{
  width:2.4em; height:30px; text-align:center; font-family:inherit; font-size:15px;
  border:0; border-radius:7px; background:var(--bg); color:var(--ink);
  -webkit-appearance:none; appearance:none;
}
.jump input::-webkit-outer-spin-button,.jump input::-webkit-inner-spin-button{ -webkit-appearance:none; margin:0; }
.jump input[type=number]{ -moz-appearance:textfield; }
.jump .go{ min-width:34px; width:34px; padding:0; font-size:18px; color:var(--accent); }

/* ---- masthead ---- */
header.mast{
  text-align:center; padding:26px 18px 8px;
}
header.mast .zh{ font-size:1.5em; font-weight:700; letter-spacing:.04em;
  font-family:"Noto Serif TC","Source Han Serif TC","Songti TC",serif; }
header.mast .en{ font-size:.82em; color:var(--ink-soft); margin-top:6px; font-style:italic;
  font-family:Georgia,"Times New Roman",serif; }
header.mast .rule{ width:42px; height:2px; background:var(--accent); margin:14px auto 0; }

/* ---- reading area ---- */
#reader{ padding:8px 0 28vh; }
.content{
  max-width:36rem; margin:0 auto;
  padding:0 max(20px,env(safe-area-inset-right)) 0 max(20px,env(safe-area-inset-left));
}
.para{
  position:relative; font-size:var(--fs); line-height:1.9;
  margin:0 0 1.7em; text-align:justify; letter-spacing:.02em;
  border-radius:8px; transition:background .6s ease;
  scroll-margin-top:64px; scroll-margin-bottom:24vh;
}
body.vertical .para{ scroll-margin-top:0; scroll-margin-right:24px; }
.para .ptext{ text-indent:2em; display:block;
  -webkit-user-select:text; user-select:text; }
.pnum{
  appearance:none; border:0; background:transparent; color:var(--accent);
  font-size:.62em; font-weight:600; opacity:.85; font-family:Georgia,serif;
  vertical-align:top; margin-inline-end:.1em; padding:.45em .5em; border-radius:6px;
  cursor:pointer; line-height:1; user-select:none; -webkit-user-select:none;
  -webkit-tap-highlight-color:transparent;
  transition:background .15s ease,opacity .15s ease,transform 140ms var(--ease-out);
}
.pnum:active{ transform:scale(.9); }
.pnum::after{ content:"🔗"; font-size:.82em; margin-inline-start:.15em;
  opacity:0; transition:opacity .15s ease; }
@media (hover:hover) and (pointer:fine){
  .pnum:hover{ background:var(--accent-soft); opacity:1; }
  .pnum:hover::after{ opacity:.7; }
}
.para.flash{ background:var(--flash); }

/* ---- toast ---- */
#toast{
  position:fixed; left:50%; bottom:calc(22px + env(safe-area-inset-bottom));
  transform:translateX(-50%) translateY(10px);
  background:var(--ink); color:var(--bg);
  padding:9px 16px; border-radius:999px; font-size:14px; line-height:1;
  box-shadow:0 6px 20px rgba(0,0,0,.25); z-index:60;
  opacity:0; pointer-events:none; transition:opacity .2s ease,transform .2s ease;
  max-width:80vw; text-align:center;
}
#toast.show{ opacity:1; transform:translateX(-50%) translateY(0); }

/* ---- copy-selected-text pill ---- */
.copysel{
  position:fixed; left:50%; bottom:calc(24px + env(safe-area-inset-bottom));
  transform:translateX(-50%) translateY(10px) scale(.96);
  background:var(--accent); color:#fff; border:0;
  padding:11px 18px; border-radius:999px; font-family:inherit; font-size:14px; line-height:1;
  box-shadow:0 8px 24px rgba(0,0,0,.28); z-index:61; cursor:pointer;
  opacity:0; pointer-events:none; -webkit-tap-highlight-color:transparent;
  display:inline-flex; align-items:center; gap:6px;
  transition:opacity 180ms var(--ease-out),transform 180ms var(--ease-out);
}
.copysel.show{ opacity:1; transform:translateX(-50%) translateY(0) scale(1); pointer-events:auto; }
.copysel:active{ transform:translateX(-50%) translateY(0) scale(.96); }

/* ---- menu button + auto-hiding toolbar ---- */
.menu-seg{ min-width:36px; font-size:17px; }
#bar{ transition:transform 260ms var(--ease-out); will-change:transform; }
#bar.hidden{ transform:translateY(-100%); }

/* ---- position readout (第 N 段 / 共 N 段) ---- */
#posind{
  position:fixed; right:max(10px,env(safe-area-inset-right));
  bottom:calc(16px + env(safe-area-inset-bottom)); z-index:45;
  padding:5px 11px; border-radius:999px; font-size:12px; line-height:1; pointer-events:none;
  background:color-mix(in srgb,var(--panel) 88%,transparent); color:var(--ink-soft);
  border:1px solid var(--rule); -webkit-backdrop-filter:blur(6px); backdrop-filter:blur(6px);
  opacity:0; transform:translateY(6px); transition:opacity .25s ease,transform .25s ease;
}
#posind.show{ opacity:1; transform:translateY(0); }

/* ---- TOC / settings drawer ---- */
#scrim{ position:fixed; inset:0; z-index:70; background:rgba(0,0,0,.4);
  opacity:0; transition:opacity .26s ease; }
#scrim.show{ opacity:1; }
#drawer{
  position:fixed; top:0; right:0; z-index:71; height:100%;
  width:min(86vw,360px); display:flex; flex-direction:column;
  background:var(--panel); color:var(--ink);
  border-left:1px solid var(--rule); box-shadow:-12px 0 40px rgba(0,0,0,.28);
  transform:translateX(100%); transition:transform 300ms var(--ease-out);
}
#drawer.open{ transform:translateX(0); }
.drawer-head{
  display:flex; align-items:flex-start; justify-content:space-between; gap:10px;
  padding:calc(16px + env(safe-area-inset-top)) 16px 12px; border-bottom:1px solid var(--rule);
}
.drawer-title{ font-size:1.2em; font-weight:700;
  font-family:"Noto Serif TC","Source Han Serif TC",serif; }
.drawer-meta{ font-size:12px; color:var(--ink-soft); margin-top:5px; }
.drawer-close{ flex:0 0 auto; border:1px solid var(--rule); background:var(--bg); color:var(--ink-soft); }
.drawer-row{
  display:flex; align-items:center; justify-content:space-between;
  padding:12px 16px; border-bottom:1px solid var(--rule);
}
.set-label{ font-size:14px; color:var(--ink-soft); }
#fontToggle .seg[data-font="kai"]{ font-family:"LXGW WenKai TC","CJK Fallback",serif; }
#fontToggle .seg[data-font="song"]{ font-family:"Noto Serif TC","Songti TC",serif; }
body:not(.font-song) #fontToggle .thumb{ transform:translateX(0); }
body.font-song      #fontToggle .thumb{ transform:translateX(38px); }
body:not(.font-song) #fontToggle .seg[data-font="kai"]{ color:var(--accent); font-weight:700; }
body.font-song      #fontToggle .seg[data-font="song"]{ color:var(--accent); font-weight:700; }
.toc{ flex:1 1 auto; overflow-y:auto; -webkit-overflow-scrolling:touch;
  padding:4px 0 calc(18px + env(safe-area-inset-bottom)); }
.toc-item{
  display:flex; align-items:baseline; gap:10px; width:100%;
  appearance:none; border:0; background:transparent; color:var(--ink); text-align:left;
  padding:11px 16px; cursor:pointer; font-family:inherit; -webkit-tap-highlight-color:transparent;
}
.toc-item:active{ background:var(--chip); }
.toc-item .toc-n{ flex:0 0 auto; min-width:1.8em; color:var(--accent); font-weight:600;
  font-size:.9em; font-family:Georgia,serif; }
.toc-item .toc-snip{ flex:1 1 auto; min-width:0; font-size:.95em; line-height:1.5;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.toc-item.current{ background:color-mix(in srgb,var(--accent) 12%,transparent); }
.toc-item.current .toc-snip{ font-weight:700; }
@media (hover:hover) and (pointer:fine){ .toc-item:hover{ background:var(--chip); } }

/* font switch: 明體 (Noto Serif) body for the reading area only */
body.font-song #reader{
  font-family:"Noto Serif TC","Source Han Serif TC","Songti TC","Songti SC","PMingLiU","MingLiU",serif;
}

/* ---- reduced motion ---- */
@media (prefers-reduced-motion:reduce){
  *{ scroll-behavior:auto !important; }
  .seg,.pnum,.seg-toggle .thumb,#toast,.copysel,.para,body,#drawer,#scrim,#posind,#bar{
    transition-duration:1ms !important;
  }
  .seg:active,.pnum:active{ transform:none; }
}

/* ---- vertical 直排 ---- */
/* In vertical mode the page itself does not scroll; the body is a flex column
   (toolbar + masthead pinned) and only .content scrolls horizontally. */
body.vertical{
  display:flex; flex-direction:column;
  height:100vh; height:100dvh; overflow:hidden;
}
body.vertical #reader{
  writing-mode:vertical-rl; text-orientation:upright;
  flex:1 1 auto; min-height:0; padding:6px 0;
  display:flex;
}
body.vertical .content{
  max-width:none; width:100%; height:100%; margin:0;
  padding:10px max(18px,env(safe-area-inset-right)) 10px max(18px,env(safe-area-inset-left));
  overflow-x:auto; overflow-y:hidden; -webkit-overflow-scrolling:touch;
}
body.vertical .para{
  line-height:2.05; text-align:justify; margin:0 1.6em 0 0;
  letter-spacing:.02em;
}
body.vertical .para .ptext{ text-indent:2em; }
body.vertical .pnum{ writing-mode:horizontal-tb; text-orientation:mixed;
  display:inline-block; vertical-align:top; }
/* hide masthead in 直排 to maximize reading space */
body.vertical header.mast{ display:none; }
/* Latin runs read better rotated in vertical flow */
body.vertical .para{ text-orientation:mixed; }

/* numerals stay upright/combined where short */
.para :is(.ptext){ }

#hint{ text-align:center; color:var(--ink-soft); font-size:12px; padding:0 0 18px; }
body:not(.vertical) #hint.vonly{ display:none; }
body.vertical #hint.honly{ display:none; }
</style>
</head>
<body class="theme-light">
<div id="progress"></div>

<div id="bar">
  <div class="group">
    <button class="seg theme-seg" id="themeBtn" title="切換主題" aria-label="切換主題">
      <span class="ticon" id="themeIcon">☀</span>
    </button>
  </div>
  <div class="group" role="group" aria-label="字級">
    <button class="seg" id="fsDown" title="縮小字級" aria-label="縮小字級">A<span class="sub">−</span></button>
    <button class="seg" id="fsUp" title="放大字級" aria-label="放大字級">A<span class="sub">＋</span></button>
  </div>
  <div class="seg-toggle" id="layoutToggle" role="group" aria-label="排版方向">
    <span class="thumb" aria-hidden="true"></span>
    <button class="seg" data-layout="v" title="直排" aria-label="直排">直</button>
    <button class="seg" data-layout="h" title="橫排" aria-label="橫排">橫</button>
  </div>
  <div class="group jump" role="group" aria-label="跳到段落">
    <input id="jumpInput" type="number" min="1" max="__MAXN__" inputmode="numeric" placeholder="段#" aria-label="段落編號">
    <button class="seg go" id="jumpBtn" title="前往" aria-label="前往段落">→</button>
  </div>
  <div class="group">
    <button class="seg menu-seg" id="menuBtn" title="目錄與設定" aria-label="開啟目錄與設定" aria-expanded="false">☰</button>
  </div>
</div>

<header class="mast">
  <div class="zh">愛的本質 · 第一卷　第一章</div>
  <div class="en">Irving Singer — The Nature of Love, Vol. 1, Ch. 1</div>
  <div class="rule"></div>
</header>

<main id="reader">
  <div class="content">
__PARAS__
  </div>
</main>
<div id="hint" class="vonly">← 由右至左閱讀，左右滑動翻頁 →</div>
<div id="toast" role="status" aria-live="polite"></div>
<button id="copySel" class="copysel" type="button">⧉ 複製所選文字</button>
<div id="posind" aria-hidden="true"></div>

<div id="scrim" hidden></div>
<aside id="drawer" aria-hidden="true" aria-label="目錄與設定">
  <div class="drawer-head">
    <div>
      <div class="drawer-title">目錄</div>
      <div class="drawer-meta" id="drawerMeta"></div>
    </div>
    <button class="seg drawer-close" id="drawerClose" title="關閉" aria-label="關閉目錄">✕</button>
  </div>
  <div class="drawer-row">
    <span class="set-label">字體</span>
    <div class="seg-toggle" id="fontToggle" role="group" aria-label="字體">
      <span class="thumb" aria-hidden="true"></span>
      <button class="seg" data-font="kai" title="楷體 · 霞鶩文楷" aria-label="楷體">楷</button>
      <button class="seg" data-font="song" title="明體 · 思源宋體" aria-label="明體">明</button>
    </div>
  </div>
  <nav class="toc" id="toc" aria-label="段落目錄"></nav>
</aside>

<script>
(function(){
  var MAXN = __MAXN__;
  var body = document.body, root = document.documentElement;
  var reader = document.getElementById('reader');
  var content = document.querySelector('.content');
  var progress = document.getElementById('progress');
  var bar = document.getElementById('bar');
  var THEMES = ['light','sepia','dark'];
  var THEME_LBL = {light:'明亮', sepia:'米黃', dark:'夜間'};
  var THEME_ICON = {light:'☀', sepia:'◐', dark:'☾'};

  function save(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }
  function load(k,d){ try{ var v=localStorage.getItem(k); return v===null?d:v; }catch(e){ return d; } }

  // ---- theme ----
  var themeBtn = document.getElementById('themeBtn');
  var themeIcon = document.getElementById('themeIcon');
  function applyTheme(t, persist){
    THEMES.forEach(function(x){ body.classList.remove('theme-'+x); });
    body.classList.add('theme-'+t);
    themeIcon.textContent = THEME_ICON[t];
    themeBtn.setAttribute('aria-label', '主題：' + THEME_LBL[t] + '（點按切換）');
    if(persist!==false) save('nol_theme', t);
  }
  var storedTheme = load('nol_theme', null);
  var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  var theme = storedTheme || (prefersDark ? 'dark' : 'light');
  if(THEMES.indexOf(theme)<0) theme='light';
  applyTheme(theme, false); // don't lock-in the auto choice on load
  // follow OS theme changes live, until the reader explicitly picks a theme
  if(!storedTheme && window.matchMedia){
    try{
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e){
        if(load('nol_theme', null)===null){ theme = e.matches ? 'dark' : 'light'; applyTheme(theme, false); }
      });
    }catch(e){}
  }
  themeBtn.addEventListener('click', function(){
    theme = THEMES[(THEMES.indexOf(theme)+1)%THEMES.length];
    applyTheme(theme, true); // explicit choice — persist it
    showToast(THEME_LBL[theme] + '模式');
  });

  // ---- font size ----
  var fs = parseFloat(load('nol_fs','20'));
  if(isNaN(fs)) fs=20;
  function applyFs(){ fs=Math.max(15,Math.min(30,fs)); root.style.setProperty('--fs', fs+'px'); save('nol_fs',String(fs)); }
  applyFs();
  document.getElementById('fsUp').addEventListener('click', function(){ fs+=1.5; applyFs(); updateProgress(); });
  document.getElementById('fsDown').addEventListener('click', function(){ fs-=1.5; applyFs(); updateProgress(); });

  // ---- layout ----
  function applyLayout(vertical){
    body.classList.toggle('vertical', vertical);
    save('nol_vertical', vertical?'1':'0');
    // reset relevant scrolls so progress reads correctly
    requestAnimationFrame(updateProgress);
  }
  var vertical = load('nol_vertical','0')==='1';
  applyLayout(vertical);
  document.querySelectorAll('#layoutToggle .seg').forEach(function(seg){
    seg.addEventListener('click', function(){
      var wantVertical = seg.getAttribute('data-layout')==='v';
      if(wantVertical === body.classList.contains('vertical')) return; // already there
      var target = currentParagraph();
      applyLayout(wantVertical);
      showBar();
      if(target) requestAnimationFrame(function(){ scrollToPara(target,false); });
    });
  });

  // ---- progress ----
  function updateProgress(){
    var frac=0;
    if(body.classList.contains('vertical')){
      var max = content.scrollWidth - content.clientWidth;
      // vertical-rl scrolls right-to-left: scrollLeft is <=0 (or 0..-max) per engine.
      var sl = content.scrollLeft;
      var traveled = Math.abs(sl);
      frac = max>0 ? traveled/max : 0;
    } else {
      var dmax = (document.documentElement.scrollHeight - window.innerHeight);
      frac = dmax>0 ? window.scrollY/dmax : 0;
    }
    frac = Math.max(0,Math.min(1,frac));
    progress.style.width = (frac*100).toFixed(2)+'%';
  }
  window.addEventListener('scroll', updateProgress, {passive:true});
  content.addEventListener('scroll', updateProgress, {passive:true});
  window.addEventListener('resize', updateProgress);

  // ---- find current paragraph (for keeping place on layout switch) ----
  function currentParagraph(){
    var ps = document.querySelectorAll('.para');
    var vw = window.innerWidth, vh = window.innerHeight;
    for(var i=0;i<ps.length;i++){
      var r = ps[i].getBoundingClientRect();
      if(body.classList.contains('vertical')){
        if(r.right >= 0 && r.left <= vw) return ps[i];
      } else {
        if(r.bottom >= 0 && r.top <= vh) return ps[i];
      }
    }
    return ps[0];
  }

  // ---- jump / scroll-to ----
  function scrollToPara(el, smooth){
    if(!el) return;
    el.scrollIntoView({behavior: smooth?'smooth':'auto', block:'center', inline:'center'});
    requestAnimationFrame(updateProgress);
  }
  function flash(el){
    if(!el) return;
    el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
    setTimeout(function(){ el.classList.remove('flash'); }, 1400);
  }
  function jumpTo(n){
    n = parseInt(n,10);
    if(isNaN(n) || n<1 || n>MAXN) return;
    var el = document.getElementById('p'+n);
    if(el){
      if(history.replaceState) history.replaceState(null,'','#p'+n); else location.hash='p'+n;
      scrollToPara(el,true); flash(el);
    }
  }
  document.getElementById('jumpBtn').addEventListener('click', function(){ jumpTo(document.getElementById('jumpInput').value); });
  document.getElementById('jumpInput').addEventListener('keydown', function(e){ if(e.key==='Enter'){ jumpTo(this.value); } });

  // ---- copy link to a paragraph ----
  var toast = document.getElementById('toast'), toastTimer=null;
  function showToast(msg){
    toast.textContent = msg; toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function(){ toast.classList.remove('show'); }, 1800);
  }
  function linkFor(n){ return location.href.split('#')[0] + '#p' + n; }
  function copyText(text){
    if(navigator.clipboard && navigator.clipboard.writeText){
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function(resolve,reject){
      try{
        var ta=document.createElement('textarea');
        ta.value=text; ta.setAttribute('readonly','');
        ta.style.position='fixed'; ta.style.top='-1000px';
        document.body.appendChild(ta); ta.select();
        var ok=document.execCommand('copy'); document.body.removeChild(ta);
        ok?resolve():reject();
      }catch(e){ reject(e); }
    });
  }
  document.querySelectorAll('.pnum').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault(); e.stopPropagation();
      var n = btn.getAttribute('data-n');
      var url = linkFor(n);
      if(history.replaceState) history.replaceState(null,'','#p'+n);
      copyText(url).then(function(){
        showToast('已複製第 ' + n + ' 段連結');
      }).catch(function(){
        showToast('連結：' + url);
      });
      var el=document.getElementById('p'+n); if(el) flash(el);
    });
  });

  // ---- copy selected passage text (coexists with per-paragraph link copy) ----
  var copySelBtn = document.getElementById('copySel');
  var selTimer=null, lastSel='';
  function selectionInReader(){
    var sel = window.getSelection ? window.getSelection() : null;
    if(!sel || sel.isCollapsed || !sel.rangeCount) return '';
    var node = sel.anchorNode;
    if(node && reader.contains(node)) return sel.toString().replace(/\s+$/,'').replace(/^\s+/,'');
    return '';
  }
  function refreshCopySel(){
    lastSel = selectionInReader();
    copySelBtn.classList.toggle('show', lastSel.length>0);
  }
  document.addEventListener('selectionchange', function(){
    clearTimeout(selTimer); selTimer=setTimeout(refreshCopySel, 120);
  });
  // keep the selection alive when the pill is pressed
  copySelBtn.addEventListener('mousedown', function(e){ e.preventDefault(); });
  copySelBtn.addEventListener('click', function(){
    var t = lastSel || selectionInReader();
    if(!t){ copySelBtn.classList.remove('show'); return; }
    copyText(t).then(function(){ showToast('已複製所選文字'); })
               .catch(function(){ showToast('複製失敗，請長按選取後使用系統選單'); });
    copySelBtn.classList.remove('show');
    var sel = window.getSelection && window.getSelection();
    if(sel && sel.removeAllRanges) sel.removeAllRanges();
  });

  // ---- resume reading position across sessions ----
  function savePos(){
    var el = currentParagraph();
    if(el && el.dataset && el.dataset.n) save('nol_pos', el.dataset.n);
  }
  function restorePos(){
    var n = parseInt(load('nol_pos',''),10);
    if(isNaN(n) || n<2 || n>MAXN) return false;       // p1 is already the top
    var el = document.getElementById('p'+n);
    if(!el) return false;
    scrollToPara(el,false);
    showToast('已回到第 ' + n + ' 段');
    return true;
  }
  var posTimer=null;
  function queueSavePos(){ clearTimeout(posTimer); posTimer=setTimeout(savePos,400); }
  window.addEventListener('scroll', queueSavePos, {passive:true});
  content.addEventListener('scroll', queueSavePos, {passive:true});
  window.addEventListener('pagehide', savePos);
  document.addEventListener('visibilitychange', function(){ if(document.visibilityState==='hidden') savePos(); });

  // ---- body font: 楷 (LXGW WenKai) / 明 (Noto Serif), lazy-load Song weights ----
  var notoBodyLoaded = false;
  function ensureNotoBody(){
    if(notoBodyLoaded) return; notoBodyLoaded = true;
    var l = document.createElement('link'); l.rel='stylesheet';
    l.href='https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;600;700&display=swap';
    document.head.appendChild(l);
  }
  function applyFont(f, persist){
    var song = (f==='song');
    body.classList.toggle('font-song', song);
    if(song) ensureNotoBody();
    if(persist!==false) save('nol_font', song?'song':'kai');
  }
  applyFont(load('nol_font','kai'), false);
  document.querySelectorAll('#fontToggle .seg').forEach(function(seg){
    seg.addEventListener('click', function(){ applyFont(seg.getAttribute('data-font'), true); });
  });

  // ---- TOC / settings drawer ----
  var menuBtn = document.getElementById('menuBtn');
  var drawer  = document.getElementById('drawer');
  var scrim   = document.getElementById('scrim');
  var toc     = document.getElementById('toc');
  var allParas = document.querySelectorAll('.para');

  // reading-time estimate (~350 Chinese chars/min) + total count
  var totalChars = 0;
  allParas.forEach(function(p){ var t=p.querySelector('.ptext'); if(t) totalChars += t.textContent.length; });
  document.getElementById('drawerMeta').textContent =
    '共 ' + MAXN + ' 段 · 約 ' + Math.max(1, Math.round(totalChars/350)) + ' 分鐘';

  // build the table of contents (snippets read from the DOM — no duplicated text in HTML)
  allParas.forEach(function(p){
    var n = p.dataset.n;
    var t = ((p.querySelector('.ptext')||{}).textContent || '').replace(/^\s+/,'');
    var item = document.createElement('button');
    item.type='button'; item.className='toc-item'; item.setAttribute('data-n', n);
    var sn=document.createElement('span'); sn.className='toc-n';   sn.textContent=n;
    var ss=document.createElement('span'); ss.className='toc-snip'; ss.textContent=t.slice(0,24);
    item.appendChild(sn); item.appendChild(ss);
    item.addEventListener('click', function(){ closeDrawer(); jumpTo(n); });
    toc.appendChild(item);
  });
  function markCurrentToc(){
    var cur = currentParagraph(); var cn = cur && cur.dataset ? cur.dataset.n : null, active=null;
    toc.querySelectorAll('.toc-item').forEach(function(it){
      var on = it.getAttribute('data-n')===cn; it.classList.toggle('current', on); if(on) active=it;
    });
    if(active) active.scrollIntoView({block:'center'});
  }
  function openDrawer(){
    scrim.hidden=false; markCurrentToc();
    requestAnimationFrame(function(){ scrim.classList.add('show'); drawer.classList.add('open'); });
    drawer.setAttribute('aria-hidden','false'); menuBtn.setAttribute('aria-expanded','true');
    showBar();
  }
  function closeDrawer(){
    scrim.classList.remove('show'); drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden','true'); menuBtn.setAttribute('aria-expanded','false');
    setTimeout(function(){ if(!drawer.classList.contains('open')) scrim.hidden=true; }, 320);
  }
  menuBtn.addEventListener('click', function(){ drawer.classList.contains('open') ? closeDrawer() : openDrawer(); });
  scrim.addEventListener('click', closeDrawer);
  document.getElementById('drawerClose').addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape' && drawer.classList.contains('open')) closeDrawer(); });

  // ---- position readout (appears while scrolling, fades when idle) ----
  var posind = document.getElementById('posind');
  var posTick=false, posIdle=null;
  function showPosInd(){
    var el = currentParagraph(); if(!el || !el.dataset) return;
    posind.textContent = '第 ' + el.dataset.n + ' 段 / 共 ' + MAXN + ' 段';
    posind.classList.add('show');
    clearTimeout(posIdle); posIdle = setTimeout(function(){ posind.classList.remove('show'); }, 1500);
  }
  function queuePosInd(){ if(posTick) return; posTick=true;
    requestAnimationFrame(function(){ posTick=false; showPosInd(); }); }

  // ---- auto-hiding toolbar (horizontal mode only; disabled for reduced-motion) ----
  var prefersReduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lastY = window.scrollY||0;
  function showBar(){ bar.classList.remove('hidden'); }
  function hideBar(){ if(!drawer.classList.contains('open')) bar.classList.add('hidden'); }
  function onScrollDir(){
    if(prefersReduce || body.classList.contains('vertical')){ showBar(); return; }
    var y = window.scrollY||0;
    if(y < 90){ showBar(); }
    else if(y - lastY > 8){ hideBar(); }
    else if(lastY - y > 8){ showBar(); }
    lastY = y;
  }
  function onScrollExtras(){ onScrollDir(); queuePosInd(); }
  window.addEventListener('scroll', onScrollExtras, {passive:true});
  content.addEventListener('scroll', onScrollExtras, {passive:true});

  // ---- deep link on load ----
  function gotoHash(smooth){
    var m = /^#p(\d+)$/.exec(location.hash||'');
    if(m){
      var el = document.getElementById('p'+m[1]);
      if(el){ scrollToPara(el,smooth); flash(el); return true; }
    }
    return false;
  }
  window.addEventListener('hashchange', function(){ gotoHash(true); });

  // initial paint — deep link wins, else resume saved position, else top
  requestAnimationFrame(function(){
    if(!gotoHash(false)){ if(!restorePos()) updateProgress(); }
    lastY = window.scrollY||0;  // sync so the resume scroll doesn't trigger auto-hide
    showBar();
  });
})();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__PARAS__", paras_html)
       .replace("__MAXN__", str(last_n)))
OUT.write_text(out, encoding="utf-8")
print(f"Wrote {OUT.name}: {len(paras)} paragraphs (1..{last_n}), {len(out)} bytes")
