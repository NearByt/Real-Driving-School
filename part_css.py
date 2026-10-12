# part_css.py - Master CSS & Liquid Glass Theme Engine for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

CSS_CONTENT = r'''
  <!-- Google Fonts: Inter, Rajdhani & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">

  <!-- FontAwesome 6 Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous">

  <!-- Google Firebase SDK for $0 Global Multi-Device Real-Time Sync & Storage -->
  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-storage-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>

  <style>
    /* ==========================================================================
       AUTHENTIC LIQUID GLASS DESIGN SYSTEM (TRANSLUCENT & REFRACTIVE)
       Cards, Dock, Header, and Modals allow the background wallpaper/video
       to shine and move through them dynamically!
       ========================================================================== */
    :root, [data-theme="frost"] {
      /* Theme 1: Liquid Frost (Default Pure Translucent Frosted Glass) */
      --bg-base: #0b1120;
      --bg-surface: rgba(255, 255, 255, 0.28);
      --bg-surface-elevated: rgba(255, 255, 255, 0.42);
      --bg-glass-matte: rgba(255, 255, 255, 0.12);
      --card-bg: rgba(255, 255, 255, 0.32);

      --glass-blur: 24px;
      --glass-border: rgba(255, 255, 255, 0.65);
      --glass-border-subtle: rgba(255, 255, 255, 0.38);
      --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.14), inset 0 1px 1px 0 rgba(255, 255, 255, 0.7);
      --glass-shadow-lg: 0 16px 48px 0 rgba(0, 0, 0, 0.22), inset 0 1px 1px 0 rgba(255, 255, 255, 0.8);

      --text-main: #0f172a;
      --text-muted: #1e293b;
      --text-dim: #475569;

      /* ONLY GAME NAME & ACCENTS ARE ORANGE */
      --brand-orange: #ff6b00;
      --brand-orange-glow: rgba(255, 107, 0, 0.45);

      /* BUTTONS USE SLEEK MIDNIGHT SLATE & TRANSLUCENT GLASS */
      --btn-primary-bg: #0f172a;
      --btn-primary-hover: #1e293b;
      --btn-primary-text: #ffffff;

      --btn-secondary-bg: rgba(255, 255, 255, 0.45);
      --btn-secondary-hover: rgba(255, 255, 255, 0.75);
      --btn-secondary-text: #0f172a;
      --btn-secondary-border: rgba(255, 255, 255, 0.65);

      --accent-green: #15803d;
      --accent-blue: #0284c7;
      --accent-purple: #9333ea;
      --accent-red: #dc2626;

      --radius-sm: 10px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --radius-pill: 9999px;

      --font-main: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-heading: 'Rajdhani', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;

      --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    [data-theme="stealth"] {
      /* Theme 2: Midnight Stealth (Deep Obsidian Liquid Glass) */
      --bg-base: #030712;
      --bg-surface: rgba(15, 23, 42, 0.45);
      --bg-surface-elevated: rgba(30, 41, 59, 0.6);
      --bg-glass-matte: rgba(3, 7, 18, 0.35);
      --card-bg: rgba(15, 23, 42, 0.5);

      --glass-border: rgba(255, 255, 255, 0.22);
      --glass-border-subtle: rgba(255, 255, 255, 0.12);
      --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.55), inset 0 1px 1px 0 rgba(255, 255, 255, 0.25);
      --glass-shadow-lg: 0 16px 48px 0 rgba(0, 0, 0, 0.75), inset 0 1px 1px 0 rgba(255, 255, 255, 0.35);

      --text-main: #f8fafc;
      --text-muted: #cbd5e1;
      --text-dim: #94a3b8;

      --brand-orange: #ff6b00;
      --brand-orange-glow: rgba(255, 107, 0, 0.55);

      --btn-primary-bg: #1e293b;
      --btn-primary-hover: #334155;
      --btn-primary-text: #ffffff;

      --btn-secondary-bg: rgba(255, 255, 255, 0.15);
      --btn-secondary-hover: rgba(255, 255, 255, 0.28);
      --btn-secondary-text: #f8fafc;
      --btn-secondary-border: rgba(255, 255, 255, 0.25);
    }

    [data-theme="velocity"] {
      /* Theme 3: Cyber Velocity (Neon Cyan & Indigo Liquid Glass) */
      --bg-base: #050b1a;
      --bg-surface: rgba(14, 22, 45, 0.5);
      --bg-surface-elevated: rgba(20, 35, 70, 0.65);
      --bg-glass-matte: rgba(5, 11, 26, 0.3);
      --card-bg: rgba(14, 22, 45, 0.52);

      --glass-border: rgba(56, 189, 248, 0.45);
      --glass-border-subtle: rgba(56, 189, 248, 0.25);
      --glass-shadow: 0 8px 32px 0 rgba(2, 6, 23, 0.6), inset 0 1px 1px 0 rgba(56, 189, 248, 0.4);

      --text-main: #f0f9ff;
      --text-muted: #bae6fd;
      --text-dim: #7dd3fc;

      --brand-orange: #ff6b00;
      --brand-orange-glow: rgba(255, 107, 0, 0.55);

      --btn-primary-bg: #0369a1;
      --btn-primary-hover: #0284c7;
      --btn-primary-text: #ffffff;

      --btn-secondary-bg: rgba(56, 189, 248, 0.18);
      --btn-secondary-hover: rgba(56, 189, 248, 0.3);
      --btn-secondary-text: #f0f9ff;
      --btn-secondary-border: rgba(56, 189, 248, 0.4);
    }

    [data-theme="carbon"] {
      /* Theme 4: Carbon GT (Smoked Race Glass) */
      --bg-base: #0a0a0a;
      --bg-surface: rgba(24, 24, 27, 0.55);
      --bg-surface-elevated: rgba(39, 39, 42, 0.7);
      --bg-glass-matte: rgba(10, 10, 10, 0.35);
      --card-bg: rgba(24, 24, 27, 0.58);

      --glass-border: rgba(255, 255, 255, 0.25);
      --glass-border-subtle: rgba(255, 255, 255, 0.14);
      --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7), inset 0 1px 1px 0 rgba(255, 255, 255, 0.25);

      --text-main: #fafafa;
      --text-muted: #d4d4d8;
      --text-dim: #a1a1aa;

      --brand-orange: #ff6b00;
      --brand-orange-glow: rgba(255, 107, 0, 0.55);

      --btn-primary-bg: #27272a;
      --btn-primary-hover: #3f3f46;
      --btn-primary-text: #ffffff;

      --btn-secondary-bg: rgba(255, 255, 255, 0.14);
      --btn-secondary-hover: rgba(255, 255, 255, 0.25);
      --btn-secondary-text: #fafafa;
      --btn-secondary-border: rgba(255, 255, 255, 0.22);
    }

    /* Global Reset */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    html, body {
      font-family: var(--font-main);
      color: var(--text-main);
      background-color: var(--bg-base);
      min-height: 100vh;
      overflow-x: hidden;
      scroll-behavior: smooth;
    }

    /* Ambient Fullscreen Background Layer */
    #bg-media-container {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -3;
      overflow: hidden;
      background: #000;
    }

    .bg-video-element, .bg-image-element {
      position: absolute;
      top: 50%;
      left: 50%;
      min-width: 100%;
      min-height: 100%;
      width: auto;
      height: auto;
      transform: translate(-50%, -50%);
      object-fit: cover;
    }

    /* Animated Canvas Particle Layer */
    #bg-motion-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -2;
      pointer-events: none;
      transition: opacity 0.4s ease;
    }
    #bg-motion-canvas.motion-disabled { display: none; }

    /* Frost Matte Optical Blur Layer (Soft Luminous Veil) */
    .bg-white-matte-layer {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -1;
      background: var(--bg-glass-matte);
      backdrop-filter: blur(14px) saturate(160%);
      -webkit-backdrop-filter: blur(14px) saturate(160%);
      pointer-events: none;
    }

    /* Reusable Liquid Glass Cards */
    .liquid-glass {
      background: var(--card-bg);
      backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-md);
      box-shadow: var(--glass-shadow);
      transition: var(--transition);
    }
    .liquid-glass:hover {
      border-color: rgba(255, 107, 0, 0.55);
      box-shadow: var(--glass-shadow-lg);
    }

    /* Button System */
    .btn-brand-primary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      padding: 0.65rem 1.25rem;
      background: var(--btn-primary-bg);
      color: var(--btn-primary-text);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: var(--radius-sm);
      font-size: 0.88rem;
      font-weight: 600;
      font-family: var(--font-main);
      cursor: pointer;
      transition: var(--transition);
      user-select: none;
      white-space: nowrap;
    }
    .btn-brand-primary:hover {
      background: var(--btn-primary-hover);
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .btn-brand-primary:active { transform: translateY(0); }

    .btn-brand-secondary {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      padding: 0.65rem 1.25rem;
      background: var(--btn-secondary-bg);
      color: var(--btn-secondary-text);
      border: 1px solid var(--btn-secondary-border);
      border-radius: var(--radius-sm);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      font-size: 0.88rem;
      font-weight: 600;
      font-family: var(--font-main);
      cursor: pointer;
      transition: var(--transition);
      user-select: none;
      white-space: nowrap;
    }
    .btn-brand-secondary:hover {
      background: var(--btn-secondary-hover);
      transform: translateY(-1px);
    }

    .btn-brand-danger {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.5rem 0.95rem;
      background: rgba(220, 38, 38, 0.15);
      color: var(--accent-red);
      border: 1px solid rgba(220, 38, 38, 0.35);
      border-radius: var(--radius-sm);
      backdrop-filter: blur(12px);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }
    .btn-brand-danger:hover {
      background: var(--accent-red);
      color: #fff;
    }

    /* ==========================================================================
       SCREEN 1: FULL SCREEN SPLASH LANDING (CLEAN, NO BOX LOOK)
       ========================================================================== */
    #splash-screen {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 5000;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 3rem 4rem;
      transition: opacity 0.4s ease, transform 0.4s ease;
    }
    #splash-screen.hidden-splash {
      opacity: 0;
      transform: scale(1.02);
      pointer-events: none;
      visibility: hidden;
    }

    .splash-social-row {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
    .splash-social-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.5rem 1rem;
      background: rgba(255, 255, 255, 0.35);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-pill);
      color: var(--text-main);
      font-size: 0.82rem;
      font-weight: 700;
      text-decoration: none;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      box-shadow: 0 4px 15px rgba(0,0,0,0.08);
      transition: var(--transition);
    }
    .splash-social-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
      background: rgba(255, 255, 255, 0.65);
    }

    .splash-left-block {
      max-width: 780px;
      margin: auto 0;
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .splash-logo-row {
      display: flex;
      align-items: center;
      gap: 1.25rem;
    }

    .splash-game-logo {
      width: 76px;
      height: 76px;
      border-radius: 18px;
      object-fit: cover;
      box-shadow: 0 10px 25px rgba(255, 107, 0, 0.4);
      border: 2px solid var(--brand-orange);
      user-select: none;
    }

    /* STRICT REQUIREMENT: Game name in straight line and ORANGE */
    .splash-game-name {
      font-family: var(--font-heading);
      font-size: 3.4rem;
      font-weight: 800;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--brand-orange);
      white-space: nowrap;
      line-height: 1;
      text-shadow: 0 4px 20px var(--brand-orange-glow);
    }

    .splash-about-small {
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--text-muted);
      max-width: 620px;
      font-weight: 500;
    }

    .splash-continue-container {
      display: flex;
      justify-content: center;
      align-items: center;
      padding-bottom: 1.5rem;
    }

    .btn-splash-continue {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.85rem;
      padding: 1.05rem 3.5rem;
      background: linear-gradient(135deg, var(--brand-orange), #ff8533);
      color: #fff;
      font-family: var(--font-heading);
      font-size: 1.35rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 2px;
      border: none;
      border-radius: var(--radius-pill);
      cursor: pointer;
      box-shadow: 0 10px 30px rgba(255, 107, 0, 0.5);
      transition: var(--transition);
      user-select: none;
    }
    .btn-splash-continue:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 16px 45px rgba(255, 107, 0, 0.75);
    }
    .btn-splash-continue .arrow-icon {
      font-size: 1.3rem;
      transition: transform 0.25s ease;
    }
    .btn-splash-continue:hover .arrow-icon {
      transform: translateX(6px);
    }

    /* ==========================================================================
       SCREEN 2: MAIN WEB HUB (STICKY TOP UI THAT STAYS STILL)
       ========================================================================== */
    #main-hub-screen {
      display: none;
      min-height: 100vh;
      opacity: 0;
      transition: opacity 0.35s ease;
    }
    #main-hub-screen.active-hub {
      display: block;
      opacity: 1;
    }

    /* Top Sticky Header - Liquid Glass that stays still on scroll */
    .hub-sticky-header {
      position: sticky;
      top: 0;
      width: 100%;
      z-index: 1000;
      background: var(--bg-surface);
      backdrop-filter: blur(28px) saturate(200%);
      -webkit-backdrop-filter: blur(28px) saturate(200%);
      border-bottom: 1px solid var(--glass-border-subtle);
      box-shadow: var(--glass-shadow);
      padding: 0.65rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }

    .hub-brand-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      cursor: pointer;
      flex-shrink: 0;
    }
    .hub-brand-logo {
      width: 38px;
      height: 38px;
      border-radius: 10px;
      object-fit: cover;
      border: 2px solid var(--brand-orange);
    }
    /* Strictly Game Name in Orange */
    .hub-brand-title {
      font-family: var(--font-heading);
      font-size: 1.45rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--brand-orange);
      white-space: nowrap;
      line-height: 1;
    }

    .hub-actions-group {
      display: flex;
      align-items: center;
      gap: 0.65rem;
      flex-shrink: 0;
    }

    .hub-icon-btn {
      width: 38px;
      height: 38px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--bg-surface-elevated);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-sm);
      color: var(--text-main);
      cursor: pointer;
      font-size: 0.95rem;
      transition: var(--transition);
      position: relative;
    }
    .hub-icon-btn:hover {
      background: rgba(255, 255, 255, 0.7);
      transform: translateY(-1px);
    }

    .hub-badge-dot {
      position: absolute;
      top: 5px;
      right: 5px;
      background: var(--brand-orange);
      color: #fff;
      font-size: 0.65rem;
      font-weight: 800;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .cloud-sync-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.35rem 0.75rem;
      background: rgba(22, 163, 74, 0.2);
      border: 1px solid rgba(22, 163, 74, 0.4);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: var(--radius-pill);
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--accent-green);
    }
    .cloud-sync-indicator {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--accent-green);
      box-shadow: 0 0 8px var(--accent-green);
    }

    /* Driver Profile Header Pill */
    .hub-user-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.85rem 0.35rem 0.4rem;
      background: var(--bg-surface-elevated);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-pill);
      cursor: pointer;
      transition: var(--transition);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    .hub-user-pill:hover {
      transform: translateY(-1px);
      border-color: var(--brand-orange);
    }
    .user-pill-img {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      object-fit: cover;
    }
    .user-pill-info {
      display: flex;
      flex-direction: column;
      line-height: 1.15;
    }
    .user-pill-name {
      font-size: 0.82rem;
      font-weight: 700;
      max-width: 110px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .user-pill-role {
      font-size: 0.68rem;
      color: var(--text-dim);
    }

    /* ==========================================================================
       CATEGORY NAVIGATION DOCK WITH VISIBLE SCROLL ARROWS
       ========================================================================== */
    .hub-dock-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      width: 100%;
      max-width: 980px;
      margin: 0.75rem auto;
      padding: 0 1rem;
    }

    .nav-dock-scroll-arrow {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: var(--bg-surface-elevated);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--glass-border);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10002;
      transition: var(--transition);
      font-size: 0.8rem;
    }
    .nav-dock-scroll-arrow.arrow-left { left: 0px; }
    .nav-dock-scroll-arrow.arrow-right { right: 0px; }
    .nav-dock-scroll-arrow:hover {
      background: #fff;
      transform: translateY(-50%) scale(1.1);
      border-color: var(--brand-orange);
      color: var(--brand-orange);
    }

    .hub-category-dock {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      overflow-x: auto;
      scrollbar-width: none;
      padding: 0.4rem 0.75rem;
      background: var(--bg-surface);
      backdrop-filter: blur(28px) saturate(200%);
      -webkit-backdrop-filter: blur(28px) saturate(200%);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-pill);
      box-shadow: var(--glass-shadow);
      user-select: none;
      width: 100%;
      transition: var(--transition);
    }
    .hub-category-dock::-webkit-scrollbar { display: none; }

    .hub-nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.5rem 0.95rem;
      background: transparent;
      border: 1px solid transparent;
      border-radius: var(--radius-pill);
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 700;
      cursor: pointer;
      transition: var(--transition);
      white-space: nowrap;
    }
    .hub-nav-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.3);
    }
    .hub-nav-btn.active {
      background: var(--btn-primary-bg);
      color: var(--btn-primary-text);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }

    /* Bottom Dock Mode (For Desktop if chosen) */
    body.nav-pos-bottom .hub-dock-wrapper {
      position: fixed !important;
      bottom: 18px !important;
      left: 14px !important;
      right: 14px !important;
      max-width: 720px !important;
      margin: 0 auto !important;
      z-index: 9999 !important;
    }
    body.nav-pos-bottom .hub-content-container {
      padding-bottom: 95px !important;
    }

    /* Content View Container */
    .hub-content-container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 1.5rem 1.5rem 4rem 1.5rem;
    }

    .view-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .view-title-main {
      font-family: var(--font-heading);
      font-size: 2.1rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1px;
      line-height: 1.1;
    }
    .view-subtitle-main {
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-top: 0.25rem;
      font-weight: 500;
    }

    /* Catalog Grids (PC: 3 or 4 columns) */
    .cars-grid-catalog,
    .tyres-grid-container,
    .events-grid-container,
    .maps-grid-container,
    .updates-grid-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 1.25rem;
    }

    /* Vehicle Display Card - Liquid Glass */
    .car-display-card {
      background: var(--card-bg);
      backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: var(--glass-shadow);
      transition: var(--transition);
    }
    .car-display-card:hover {
      transform: translateY(-4px);
      box-shadow: var(--glass-shadow-lg);
      border-color: rgba(255, 107, 0, 0.5);
    }

    .car-photo-box {
      width: 100%;
      height: 180px;
      position: relative;
      overflow: hidden;
      background: #000;
      cursor: pointer;
    }
    .car-photo-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.4s ease;
    }
    .car-photo-box:hover .car-photo-img {
      transform: scale(1.05);
    }
    .car-order-pill {
      position: absolute;
      top: 10px;
      left: 10px;
      padding: 0.25rem 0.6rem;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      color: #fff;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 0.85rem;
      border-radius: var(--radius-sm);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .car-card-body {
      padding: 1.15rem;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .car-title-heading {
      font-size: 1.15rem;
      font-weight: 800;
      margin-bottom: 0.35rem;
      color: var(--text-main);
    }
    .car-quick-specs {
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--glass-border-subtle);
      border-radius: var(--radius-sm);
      padding: 0.65rem;
      margin: 0.75rem 0;
      display: flex;
      flex-direction: column;
      gap: 0.3rem;
      font-size: 0.82rem;
    }

    /* Calculator Two-Column Layout */
    .calculator-two-col {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 1.5rem;
      margin-top: 2rem;
    }

    /* Tuning Stage Chips */
    .stage-chips-wrap {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin: 0.5rem 0;
    }
    .stage-choice-chip {
      padding: 0.45rem 0.95rem;
      background: rgba(255, 255, 255, 0.35);
      backdrop-filter: blur(12px);
      border: 1px solid var(--glass-border-subtle);
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: var(--transition);
      user-select: none;
    }
    .stage-choice-chip:hover {
      background: rgba(255, 255, 255, 0.65);
      color: var(--text-main);
    }
    .stage-choice-chip.active {
      background: var(--btn-primary-bg);
      color: #fff;
      border-color: var(--btn-primary-bg);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Luxury Bill / Valuation Breakdown */
    .luxury-receipt-container {
      background: var(--card-bg);
      backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(190%);
      border-radius: var(--radius-md);
      border: 1px solid var(--glass-border);
      padding: 1.75rem;
      box-shadow: var(--glass-shadow-lg);
      position: relative;
    }
    .receipt-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 1rem;
      border-bottom: 2px dashed var(--glass-border-subtle);
      margin-bottom: 1.25rem;
    }
    .receipt-item-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.45rem 0;
      font-size: 0.88rem;
    }
    .receipt-total-box {
      margin-top: 1.25rem;
      padding-top: 1rem;
      border-top: 2px solid var(--glass-border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }
    .receipt-total-range {
      font-family: var(--font-heading);
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--brand-orange);
    }

    /* Form Fields */
    .form-group-item {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      margin-bottom: 1rem;
    }
    .form-field-label {
      font-size: 0.82rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
    }
    .input-box-field, .select-box-field, .textarea-box-field {
      width: 100%;
      padding: 0.75rem 1rem;
      background: rgba(255, 255, 255, 0.4);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--glass-border);
      border-radius: var(--radius-sm);
      color: var(--text-main);
      font-family: var(--font-main);
      font-size: 0.92rem;
      transition: var(--transition);
      outline: none;
    }
    .input-box-field:focus, .select-box-field:focus, .textarea-box-field:focus {
      border-color: var(--brand-orange);
      background: rgba(255, 255, 255, 0.65);
      box-shadow: 0 0 0 3px rgba(255, 107, 0, 0.2);
    }

    /* Media Feedback & Status Thumbnail */
    .media-selected-status-badge {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-top: 0.45rem;
      padding: 0.4rem 0.75rem;
      background: rgba(22, 163, 74, 0.12);
      border: 1px solid rgba(22, 163, 74, 0.35);
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      color: var(--accent-green);
      font-weight: 700;
    }
    .media-selected-thumb {
      width: 44px;
      height: 30px;
      object-fit: cover;
      border-radius: 4px;
      border: 1px solid var(--accent-green);
    }

    /* Modals - Liquid Glass Layers */
    .app-modal-layer {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 12000;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.25rem;
    }
    .app-modal-layer.active {
      display: flex;
    }
    .app-modal-window {
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(32px) saturate(200%);
      -webkit-backdrop-filter: blur(32px) saturate(200%);
      border-radius: var(--radius-lg);
      border: 1px solid var(--glass-border);
      box-shadow: var(--glass-shadow-lg);
      width: 100%;
      max-width: 680px;
      max-height: 90vh;
      overflow-y: auto;
      padding: 2rem;
      position: relative;
    }
    .modal-headline-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--glass-border-subtle);
    }
    .modal-headline-title {
      font-family: var(--font-heading);
      font-size: 1.5rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-main);
    }
    .modal-close-cross {
      background: transparent;
      border: none;
      font-size: 1.5rem;
      color: var(--text-dim);
      cursor: pointer;
      line-height: 1;
      transition: var(--transition);
    }
    .modal-close-cross:hover { color: var(--accent-red); }

    /* Updates Channel Tabs */
    .update-channel-tabs {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      border-bottom: 1px solid var(--glass-border-subtle);
      padding-bottom: 0.5rem;
    }
    .update-tab-btn {
      padding: 0.55rem 1.25rem;
      background: rgba(255, 255, 255, 0.35);
      border: 1px solid var(--glass-border-subtle);
      border-radius: var(--radius-pill);
      font-size: 0.9rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: var(--transition);
    }
    .update-tab-btn.active {
      background: var(--btn-primary-bg);
      color: #fff;
    }

    /* Subtabs in Owner Panel */
    .admin-subtab-btn {
      padding: 0.5rem 1rem;
      background: rgba(255, 255, 255, 0.35);
      border: 1px solid var(--glass-border-subtle);
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      transition: var(--transition);
      white-space: nowrap;
    }
    .admin-subtab-btn.active {
      background: var(--btn-primary-bg);
      color: #fff;
      border-color: var(--btn-primary-bg);
    }

    /* Secret Version Click Pill */
    .version-click-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 1rem;
      background: rgba(255, 255, 255, 0.4);
      border: 1px solid var(--glass-border-subtle);
      border-radius: var(--radius-pill);
      font-size: 0.78rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
    }
    .version-click-pill:active { background: rgba(0, 0, 0, 0.1); }

    /* ==========================================================================
       MOBILE RESPONSIVE OVERRIDES (MOBILE 2-COLUMNS & DETACHED FLOATING DOCK)
       ========================================================================== */
    @media (max-width: 768px) {
      #splash-screen {
        padding: 2rem 1.25rem;
      }
      .splash-game-name {
        font-size: 2.2rem;
        white-space: normal;
      }
      .splash-logo-row {
        gap: 0.75rem;
      }
      .splash-game-logo {
        width: 58px;
        height: 58px;
      }
      .btn-splash-continue {
        width: 100%;
        padding: 0.95rem 1.5rem;
        font-size: 1.15rem;
      }

      /* Compact single horizontal header row */
      .hub-sticky-header {
        padding: 0.5rem 0.75rem !important;
        gap: 0.4rem !important;
      }
      .hub-brand-group {
        gap: 0.45rem !important;
        max-width: 50% !important;
      }
      .hub-brand-logo {
        width: 32px !important;
        height: 32px !important;
      }
      .hub-brand-title {
        font-size: 1.05rem !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
      }
      .hub-actions-group {
        gap: 0.35rem !important;
      }
      .hub-icon-btn {
        width: 34px !important;
        height: 34px !important;
        font-size: 0.85rem !important;
      }
      .cloud-sync-pill {
        display: none !important;
      }
      .hub-user-pill {
        padding: 0.25rem 0.5rem 0.25rem 0.25rem !important;
        max-width: 110px !important;
      }
      .user-pill-img {
        width: 24px !important;
        height: 24px !important;
      }
      .user-pill-name {
        font-size: 0.72rem !important;
        max-width: 60px !important;
      }

      /* DETACHED FLOATING BOTTOM ISLAND DOCK ON MOBILE */
      .hub-dock-wrapper {
        position: fixed !important;
        bottom: 14px !important;
        left: 10px !important;
        right: 10px !important;
        width: auto !important;
        max-width: 560px !important;
        margin: 0 auto !important;
        z-index: 9999 !important;
        padding: 0 !important;
      }
      .nav-dock-scroll-arrow {
        display: none !important; /* Hide arrows on touch mobile where swipe works */
      }
      .hub-category-dock {
        background: var(--bg-surface-elevated) !important;
        backdrop-filter: blur(28px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(200%) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: var(--radius-pill) !important;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.25) !important;
        padding: 0.35rem 0.6rem !important;
      }

      /* Mobile 2-by-2 Grid (At least 2 items side by side) */
      .cars-grid-catalog,
      .tyres-grid-container,
      .events-grid-container,
      .maps-grid-container,
      .updates-grid-container {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.65rem !important;
      }
      .car-photo-box {
        height: 110px !important;
      }
      .car-card-body {
        padding: 0.65rem !important;
      }
      .car-title-heading {
        font-size: 0.95rem !important;
        margin-bottom: 0.2rem !important;
      }
      .car-quick-specs {
        padding: 0.4rem !important;
        font-size: 0.72rem !important;
        margin: 0.4rem 0 !important;
      }
      .btn-brand-primary, .btn-brand-secondary {
        padding: 0.45rem 0.65rem !important;
        font-size: 0.76rem !important;
      }

      .calculator-two-col {
        grid-template-columns: 1fr !important;
        gap: 1rem !important;
      }

      /* Content padding for bottom dock */
      .hub-content-container {
        padding-bottom: 95px !important;
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
      }
    }
  </style>
'''
