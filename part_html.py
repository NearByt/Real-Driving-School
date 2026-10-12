# part_html.py - Master HTML Structure & Modals for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

HTML_CONTENT = r'''
</head>
<body>
  <!-- Ambient Fullscreen Background Media -->
  <div id="bg-media-container">
    <video id="bg-video-main" class="bg-video-element" autoplay muted loop playsinline>
      <source id="bg-video-src" src="https://assets.mixkit.co/videos/preview/mixkit-sports-car-driving-at-night-41584-large.mp4" type="video/mp4">
    </video>
    <img id="bg-image-fallback" class="bg-image-element" src="" alt="RDS Background" style="display: none;">
  </div>
  <canvas id="bg-motion-canvas"></canvas>
  <div class="bg-white-matte-layer"></div>

  <!-- ========================================================================
       SCREEN 1: FULL SCREEN SPLASH LANDING (NO BOX LOOK)
       ======================================================================== -->
  <section id="splash-screen">
    <!-- Top Bar with Social Links (No UTC Timezone) -->
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
      <div class="splash-social-row" id="splash-social-row-container">
        <a href="https://discord.gg/realdrivingschool" target="_blank" class="splash-social-btn" id="link-splash-discord">
          <i class="fa-brands fa-discord" style="color: #5865f2;"></i> Discord
        </a>
        <a href="https://instagram.com/realdrivingschool" target="_blank" class="splash-social-btn" id="link-splash-instagram">
          <i class="fa-brands fa-instagram" style="color: #e1306c;"></i> Instagram
        </a>
        <a href="https://play.google.com/store/apps/details?id=com.qizz.rds" target="_blank" class="splash-social-btn" id="link-splash-googleplay">
          <i class="fa-brands fa-google-play" style="color: #16a34a;"></i> Google Play
        </a>
        <a href="https://apps.apple.com/app/real-driving-school/id1498327827" target="_blank" class="splash-social-btn" id="link-splash-appstore">
          <i class="fa-brands fa-apple" style="color: #0f172a;"></i> App Store
        </a>
      </div>
    </div>

    <!-- Big Left Content: Logo + Game Name in Straight Line & Orange + Small About Text -->
    <div class="splash-left-block">
      <div class="splash-logo-row">
        <img src="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=200&q=80" alt="Game Logo" class="splash-game-logo" id="splash-main-logo">
        <!-- Game Name in Straight Line & Orange -->
        <h1 class="splash-game-name" id="splash-main-title">REAL DRIVING SCHOOL</h1>
      </div>

      <p class="splash-about-small" id="splash-main-about">
        Experience the next generation of realistic driving simulation in Real Driving School. Ultra-realistic clutch physics, dynamic weather, custom liveries, multiplayer lobbies, and an expansive open world.
      </p>
    </div>

    <!-- Middle Down Continue Button -->
    <div class="splash-continue-container">
      <button class="btn-splash-continue" onclick="proceedToHub()">
        Continue <span class="arrow-icon"><i class="fa-solid fa-arrow-right"></i></span>
      </button>
    </div>
  </section>

  <!-- ========================================================================
       SCREEN 2: MAIN WEB HUB (STICKY TOP UI THAT STAYS STILL)
       ======================================================================== -->
  <div id="main-hub-screen">
    <!-- Top Sticky Header -->
    <header class="hub-sticky-header">
      <!-- Game Logo + Game Name in Straight Line & Orange -->
      <div class="hub-brand-group" onclick="returnToSplash()" title="Return to Welcome Screen">
        <img src="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=128&q=80" alt="RDS Logo" class="hub-brand-logo" id="header-brand-logo">
        <div class="hub-brand-title" id="header-brand-title">REAL DRIVING SCHOOL</div>
      </div>

      <!-- Header Controls & Actions -->
      <div class="hub-actions-group">
        <!-- Live Cloud Sync Badge -->
        <div class="cloud-sync-pill" id="header-sync-pill" title="Real-time multi-device sync active">
          <span class="cloud-sync-indicator"></span>
          <span id="sync-pill-text">Cloud Synced</span>
        </div>

        <!-- Audio Synthesizer Toggle -->
        <button class="hub-icon-btn" id="btn-sound-toggle" onclick="toggleAudio()" title="Sound Feedback">
          <i class="fa-solid fa-volume-high" id="icon-sound-state"></i>
        </button>

        <!-- Notification Bell with Count Badge -->
        <button class="hub-icon-btn" onclick="openAppModal('modal-notifications-list')" title="Notifications">
          <i class="fa-solid fa-bell"></i>
          <span class="hub-badge-dot" id="header-bell-badge" style="display: none;">0</span>
        </button>

        <!-- Settings Gear (Always Visible) -->
        <button class="hub-icon-btn" onclick="openAppModal('modal-app-settings')" title="Portal Settings">
          <i class="fa-solid fa-gear"></i>
        </button>

        <!-- Driver Profile Pill (Always Visible) -->
        <div class="hub-user-pill" onclick="openDriverProfileModal()" title="Driver Profile">
          <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80" alt="Avatar" class="user-pill-img" id="user-pill-avatar-img">
          <div class="user-pill-info">
            <span class="user-pill-name" id="user-pill-name-span">Driver</span>
            <span class="user-pill-role" id="user-pill-role-span">Driver</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Horizontally Scrollable Category Bar (Detached Island Dock on Mobile) -->
    <nav class="hub-category-dock nav-dock-top" id="hub-main-category-dock">
      <button class="hub-nav-btn active" data-view="car-prices" onclick="switchHubView('car-prices')"><i class="fa-solid fa-car"></i> Car Prices</button>
      <button class="hub-nav-btn" data-view="tyre-codes" onclick="switchHubView('tyre-codes')"><i class="fa-solid fa-circle-notch"></i> Tyre Codes</button>
      <button class="hub-nav-btn" data-view="events" onclick="switchHubView('events')"><i class="fa-solid fa-trophy"></i> Events</button>
      <button class="hub-nav-btn" data-view="updates" onclick="switchHubView('updates')"><i class="fa-solid fa-rocket"></i> RDS Updates</button>
      <button class="hub-nav-btn" data-view="maps" onclick="switchHubView('maps')"><i class="fa-solid fa-map-location-dot"></i> Maps & Secrets</button>
      <button class="hub-nav-btn" data-view="multiplayer" onclick="switchHubView('multiplayer')"><i class="fa-solid fa-users"></i> Multiplayer & Clans</button>
      <button class="hub-nav-btn" data-view="rules" onclick="switchHubView('rules')"><i class="fa-solid fa-scale-balanced"></i> Rules</button>
      <button class="hub-nav-btn" data-view="grinders" onclick="switchHubView('grinders')"><i class="fa-solid fa-chart-line"></i> Active Grinders</button>
      <button class="hub-nav-btn" data-view="owner" id="nav-owner-tab" onclick="switchHubView('owner')" style="display: none;"><i class="fa-solid fa-crown"></i> Owner & Staff</button>
    </nav>

    <!-- Main View Content Area -->
    <main class="hub-content-container" id="hub-main-content">
      <!-- Dynamic Views Rendered via JS -->
    </main>
  </div>

  <!-- ========================================================================
       MODALS SYSTEM
       ======================================================================== -->

  <!-- 1. Driver Onboarding Modal (Prompted on Continue) -->
  <div class="app-modal-layer" id="modal-driver-onboarding">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-id-card"></i> Welcome to RDS Portal</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-driver-onboarding')">&times;</button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        <div style="background: rgba(255, 107, 0, 0.08); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid rgba(255, 107, 0, 0.25); font-size: 0.88rem; line-height: 1.5;">
          Copy your ID from inside <strong>Real Driving School</strong> and paste below (e.g. <code>「 ⚡| Hyper_DαʀкSтαʀ 」 FIc9Z16zj4VF6Jhqm0UOCUHYwTb2</code>). The portal extracts and displays only your clean name!
        </div>

        <div class="form-group-item">
          <label class="form-field-label">Game ID or Driver Name</label>
          <input type="text" class="input-box-field" id="onboarding-input-id" placeholder="Paste game ID or enter username" oninput="handleOnboardingInput(this.value)">
          <div id="onboarding-detected-box" style="margin-top: 0.45rem; padding: 0.5rem 0.75rem; background: rgba(22, 163, 74, 0.1); border-radius: var(--radius-sm); border: 1px solid rgba(22, 163, 74, 0.25); display: none;">
            <div style="font-size: 0.75rem; color: var(--accent-green); font-weight: 700;">DETECTED IN-GAME NAME:</div>
            <div style="font-size: 0.95rem; font-weight: 800; color: var(--text-main);" id="onboarding-extracted-name"></div>
          </div>
        </div>

        <button type="button" class="btn-brand-primary" style="padding: 0.85rem; font-size: 1rem; justify-content: center;" onclick="confirmOnboarding()">
          Enter Portal <i class="fa-solid fa-arrow-right"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- 2. Staff & Owner Login Modal (Unlocked via 10 Taps on v1.2.120) -->
  <div class="app-modal-layer" id="modal-staff-login">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-shield-halved"></i> Staff Security Portal</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-staff-login')">&times;</button>
      </div>
      <form id="form-staff-login" onsubmit="event.preventDefault(); submitStaffLogin();">
        <div class="form-group-item">
          <label class="form-field-label">Staff / Owner Email</label>
          <input type="email" class="input-box-field" id="staff-email-input" placeholder="admin@realdrivingschool.com" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Password</label>
          <input type="password" class="input-box-field" id="staff-pass-input" placeholder="Enter security passphrase" required>
        </div>
        <div id="staff-login-error" style="color: var(--accent-red); font-size: 0.82rem; margin-bottom: 0.75rem; display: none;"></div>
        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.8rem;">
          <i class="fa-solid fa-lock-open"></i> Authenticate & Enter
        </button>
      </form>
    </div>
  </div>

  <!-- 3. App Settings Modal -->
  <div class="app-modal-layer" id="modal-app-settings">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-sliders"></i> Portal Settings & Info</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-app-settings')">&times;</button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 1.25rem;">
        <!-- Theme Switcher -->
        <div class="form-group-item">
          <label class="form-field-label"><i class="fa-solid fa-palette"></i> Theme & Visual Style</label>
          <select class="select-box-field" id="setting-theme-select" onchange="changeAppTheme(this.value)">
            <option value="frost">❄️ Liquid Frost (Default Frosted Slate)</option>
            <option value="stealth">🌑 Midnight Stealth (Deep Obsidian Glass)</option>
            <option value="velocity">🏎️ Cyber Velocity (Neon Indigo / Speed Cyan)</option>
            <option value="carbon">🏁 Carbon GT (Ultra-Dark Carbon Fiber)</option>
          </select>
        </div>

        <!-- Navigation Bar Position Option -->
        <div class="form-group-item">
          <label class="form-field-label"><i class="fa-solid fa-compass"></i> Category Navigation Bar Position</label>
          <select class="select-box-field" id="setting-nav-position" onchange="changeNavPosition(this.value)">
            <option value="auto">Auto (Floating Bottom on Mobile, Top on PC)</option>
            <option value="bottom">Floating Bottom Dock (Detached Island)</option>
            <option value="top">Top Navigation Bar</option>
          </select>
          <small style="color: var(--text-dim); font-size: 0.75rem; margin-top: 0.25rem; display: block;">
            Customize category bar location. Bottom dock stays detached above screen edge.
          </small>
        </div>

        <!-- Add to Home Screen (PWA - Mobile Only) -->
        <div class="form-group-item" id="pwa-install-container" style="display: none;">
          <label class="form-field-label"><i class="fa-solid fa-mobile-screen"></i> Install App on Device</label>
          <button type="button" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.75rem;" onclick="handleAddToHomeScreen()">
            <i class="fa-solid fa-download"></i> Add RDS Portal to Home Screen
          </button>
          <small style="color: var(--text-dim); font-size: 0.75rem; margin-top: 0.25rem; display: block;">
            Use Real Driving School Portal full screen just like a native mobile app.
          </small>
        </div>

        <!-- Ambient Motion Effects Option -->
        <div class="form-group-item">
          <label class="form-field-label"><i class="fa-solid fa-wand-magic-sparkles"></i> Background Motion Effects</label>
          <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
            <div>
              <div style="font-weight: 600; font-size: 0.88rem;">Ambient Dynamic Lighting</div>
              <div style="font-size: 0.75rem; color: var(--text-dim);">Floating glowing speed particles & trails</div>
            </div>
            <input type="checkbox" id="setting-motion-toggle" checked onchange="toggleBackgroundMotions(this.checked)" style="transform: scale(1.3);">
          </div>
        </div>

        <!-- Sound Effects Option -->
        <div class="form-group-item">
          <label class="form-field-label"><i class="fa-solid fa-volume-high"></i> Audio Synthesizer & Chimes</label>
          <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.75rem 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
            <div>
              <div style="font-weight: 600; font-size: 0.88rem;">Sound Alerts & Feedback</div>
              <div style="font-size: 0.75rem; color: var(--text-dim);">In-browser Web Audio chimes</div>
            </div>
            <input type="checkbox" id="setting-sound-toggle" checked onchange="toggleSound(this.checked)" style="transform: scale(1.3);">
          </div>
        </div>

        <!-- Account Session Info -->
        <div style="background: var(--bg-base); padding: 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 0.85rem; font-weight: 700;" id="settings-user-display">Driver</div>
              <div style="font-size: 0.75rem; color: var(--text-dim);" id="settings-role-display">Role: Driver</div>
            </div>
            <button type="button" class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.78rem;" onclick="closeAppModal('modal-app-settings'); openDriverProfileModal();">
              Edit Profile
            </button>
          </div>
          <div id="settings-logout-row" style="display: none; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid rgba(0,0,0,0.06);">
            <button type="button" class="btn-brand-danger" style="width: 100%; justify-content: center; padding: 0.45rem; font-size: 0.8rem;" onclick="AUTH.logout(); closeAppModal('modal-app-settings');">
              <i class="fa-solid fa-right-from-bracket"></i> Sign Out
            </button>
          </div>
        </div>

        <!-- Secret Staff Gate: Tap v1.2.120 for 10 times to unlock Staff Login -->
        <div class="settings-about-footer" style="margin-top: 1rem; padding-top: 1.25rem; border-top: 1px solid var(--glass-border-subtle); text-align: center;">
          <p style="font-size: 0.82rem; font-weight: 600; color: var(--text-muted); margin-bottom: 0.35rem;">Real Driving School Community Hub</p>
          <p style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.85rem;">Official vehicle valuation index, tuning speed calculators, and multiplayer clan guide.</p>
          
          <div class="version-click-pill" id="web-version-pill" onclick="handleVersionSecretClick()" title="Tap 10 times for staff gate">
            <i class="fa-solid fa-code-branch"></i> Web Version: v1.2.120
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 4. iOS Safari PWA Install Instructions Modal -->
  <div class="app-modal-layer" id="modal-ios-install-guide">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-brands fa-apple"></i> Install on iPhone / iPad</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-ios-install-guide')">&times;</button>
      </div>
      <div style="display: flex; flex-direction: column; gap: 1rem; font-size: 0.92rem; line-height: 1.6;">
        <p>To install <strong>Real Driving School Portal</strong> on your iOS device:</p>
        <div style="background: var(--bg-base); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
          <div style="margin-bottom: 0.75rem;"><strong>1.</strong> Tap the <strong>Share</strong> icon <i class="fa-solid fa-arrow-up-from-bracket" style="color: var(--accent-blue);"></i> at the bottom of Safari.</div>
          <div style="margin-bottom: 0.75rem;"><strong>2.</strong> Scroll down and select <strong>'Add to Home Screen'</strong> <i class="fa-regular fa-square-plus"></i>.</div>
          <div><strong>3.</strong> Tap <strong>'Add'</strong> in the top-right corner.</div>
        </div>
        <p style="color: var(--text-muted); font-size: 0.82rem;">The RDS Portal icon will now appear on your iPhone home screen for instant fullscreen app experience!</p>
        <button type="button" class="btn-brand-primary" style="justify-content: center;" onclick="closeAppModal('modal-ios-install-guide')">Got It</button>
      </div>
    </div>
  </div>

  <!-- 5. Driver Profile Modal -->
  <div class="app-modal-layer" id="modal-driver-profile">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-user-gear"></i> Driver Profile</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-driver-profile')">&times;</button>
      </div>
      <form id="form-driver-profile" onsubmit="event.preventDefault(); saveDriverProfile();">
        <div class="form-group-item">
          <label class="form-field-label">Game ID or Username</label>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.35rem;">
            Paste your full RDS ID (e.g. <code>「 ⚡| Hyper_DαʀкSтαʀ 」 FIc9Z16zj4VF6Jhqm0UOCUHYwTb2</code>). The portal displays only your clean name!
          </div>
          <input type="text" class="input-box-field" id="profile-name-input" placeholder="Paste game ID or enter username" oninput="handlePlayerIdInput(this.value)" required>
          <div id="profile-detected-box" style="margin-top: 0.45rem; padding: 0.5rem 0.75rem; background: rgba(22, 163, 74, 0.1); border-radius: var(--radius-sm); border: 1px solid rgba(22, 163, 74, 0.25); display: none;">
            <div style="font-size: 0.75rem; color: var(--accent-green); font-weight: 700;">DETECTED IN-GAME NAME:</div>
            <div style="font-size: 0.95rem; font-weight: 800; color: var(--text-main);" id="profile-extracted-display"></div>
          </div>
        </div>

        <div class="form-group-item">
          <label class="form-field-label">Avatar Photo</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="profile-avatar-input" placeholder="https://..." required>
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('profile-avatar-input', 'preview-profile-avatar')" title="Choose from Gallery or Files">
              <i class="fa-solid fa-folder-open"></i> Gallery
            </button>
          </div>
          <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.75rem;">
            <img id="preview-profile-avatar" src="" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; display: none; border: 2px solid var(--brand-orange);">
            <span style="font-size: 0.75rem; color: var(--text-dim);">Supported: JPG, PNG, WEBP (Auto-compressed)</span>
          </div>
        </div>

        <div class="form-group-item">
          <label class="form-field-label">Current Role</label>
          <div style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);" id="profile-role-display">Driver</div>
        </div>

        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.8rem; margin-top: 0.5rem;">
          <i class="fa-solid fa-floppy-disk"></i> Save Driver Profile
        </button>
      </form>
    </div>
  </div>

  <!-- 6. Fullscreen Photo Viewer Modal -->
  <div class="app-modal-layer" id="modal-photo-viewer" onclick="closePhotoViewer()">
    <div style="position: relative; max-width: 90vw; max-height: 90vh;" onclick="event.stopPropagation()">
      <button class="modal-close-cross" style="position: absolute; top: -40px; right: 0; color: #fff; font-size: 2rem;" onclick="closePhotoViewer()">&times;</button>
      <img id="photo-viewer-image" src="" style="max-width: 90vw; max-height: 85vh; border-radius: 12px; object-fit: contain; box-shadow: 0 20px 50px rgba(0,0,0,0.7);">
      <div id="photo-viewer-caption" style="color: #fff; text-align: center; margin-top: 0.75rem; font-size: 0.95rem; font-weight: 600;"></div>
    </div>
  </div>

  <!-- 7. Add/Edit Car Modal (Complete with Add-ons & Stage 1-7 Specs) -->
  <div class="app-modal-layer" id="modal-car-editor">
    <div class="app-modal-window" style="max-width: 840px;">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title" id="car-editor-modal-title">Vehicle Management</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-car-editor')">&times;</button>
      </div>
      <form id="form-car-editor" onsubmit="event.preventDefault(); saveCarFromModal();">
        <input type="hidden" id="car-edit-id">

        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1rem;">
          <div class="form-group-item">
            <label class="form-field-label">Car Name</label>
            <input type="text" class="input-box-field" id="car-name-input" placeholder="e.g. Bugatti Chiron Pur Sport" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">Catalog Order #</label>
            <input type="number" class="input-box-field" id="car-order-input" placeholder="1" required>
          </div>
        </div>

        <div class="form-group-item">
          <label class="form-field-label">Car Image</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="car-image-input" placeholder="https://..." required>
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('car-image-input', 'preview-car-editor-img')" title="Choose from Gallery or Files">
              <i class="fa-solid fa-folder-open"></i> Gallery
            </button>
          </div>
          <img id="preview-car-editor-img" src="" style="width: 100%; max-height: 140px; border-radius: 8px; object-fit: cover; margin-top: 0.5rem; display: none;">
        </div>

        <!-- Add-on Charges Required -->
        <h4 style="font-family: var(--font-heading); color: var(--brand-orange); margin: 1.25rem 0 0.5rem 0; text-transform: uppercase;">
          <i class="fa-solid fa-tags"></i> Add-on Pricing (Default Millions, support k, m, b, t)
        </h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">
          <div class="form-group-item">
            <label class="form-field-label">⭐ Premium Charge</label>
            <input type="text" class="input-box-field" id="car-premium-price-input" placeholder="e.g. 5M" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">🛡️ Coating Charge</label>
            <input type="text" class="input-box-field" id="car-coating-price-input" placeholder="e.g. 8M" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">🚓 Police Charge</label>
            <input type="text" class="input-box-field" id="car-police-price-input" placeholder="e.g. 15M" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">🌈 Rainbow Smoke Charge</label>
            <input type="text" class="input-box-field" id="car-rainbow-price-input" placeholder="e.g. 12M" required>
          </div>
        </div>

        <!-- Stage 1 to 7 Individual Specifications Inputs -->
        <h4 style="font-family: var(--font-heading); color: var(--brand-orange); margin: 1.5rem 0 0.5rem 0; text-transform: uppercase;">
          <i class="fa-solid fa-gauge-high"></i> Stage 1 to 7 Individual Tuning Specs & Prices
        </h4>
        <p style="font-size: 0.78rem; color: var(--text-dim); margin-bottom: 0.75rem;">
          Enter speeds in km/h and mph, with & without turbo, and stage valuation price (supports suffixes k, m, b, t).
        </p>

        <div style="display: flex; flex-direction: column; gap: 0.85rem;" id="car-stages-inputs-container">
          <!-- Dynamically populated or rendered 7 stage rows -->
        </div>

        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.85rem; margin-top: 1.25rem;">
          <i class="fa-solid fa-floppy-disk"></i> Save Vehicle into Official Index
        </button>
      </form>
    </div>
  </div>

  <!-- 8. Technical Specs Sheet Viewer Modal -->
  <div class="app-modal-layer" id="modal-car-specs-viewer">
    <div class="app-modal-window" style="max-width: 780px;">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title" id="specs-viewer-car-name">Vehicle Specifications Sheet</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-car-specs-viewer')">&times;</button>
      </div>
      <div id="specs-viewer-body"></div>
    </div>
  </div>

  <!-- 9. Update Editor Modal -->
  <div class="app-modal-layer" id="modal-update-editor">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title">Publish RDS Update</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-update-editor')">&times;</button>
      </div>
      <form id="form-update-editor" onsubmit="event.preventDefault(); saveUpdateFromModal();">
        <input type="hidden" id="update-edit-id">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
          <div class="form-group-item">
            <label class="form-field-label">Version</label>
            <input type="text" class="input-box-field" id="update-version-input" placeholder="v1.2.120" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">Release Channel</label>
            <select class="select-box-field" id="update-channel-select">
              <option value="public">🌐 Public Update</option>
              <option value="beta">🧪 Beta Update</option>
            </select>
          </div>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Title / Headline</label>
          <input type="text" class="input-box-field" id="update-title-input" placeholder="Patch Notes & Feature Rollout" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Cover Image (Optional)</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="update-image-input" placeholder="https://...">
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('update-image-input')">
              <i class="fa-solid fa-folder-open"></i> Gallery
            </button>
          </div>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Release Notes (One per line)</label>
          <textarea class="textarea-box-field" id="update-notes-input" rows="4" placeholder="- Added Bugatti Chiron Pur Sport&#10;- Fixed clutch slipping in multiplayer&#10;- Improved dynamic night lighting" required></textarea>
        </div>
        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
          <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem;">
            <input type="checkbox" id="update-android-check" checked> Android Live
          </label>
          <label style="display: flex; align-items: center; gap: 0.4rem; font-size: 0.85rem;">
            <input type="checkbox" id="update-ios-check" checked> iOS Live
          </label>
        </div>
        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.8rem;">
          <i class="fa-solid fa-paper-plane"></i> Publish Update
        </button>
      </form>
    </div>
  </div>

  <!-- 10. Event Editor Modal -->
  <div class="app-modal-layer" id="modal-event-editor">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title">Manage Event</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-event-editor')">&times;</button>
      </div>
      <form id="form-event-editor" onsubmit="event.preventDefault(); saveEventFromModal();">
        <input type="hidden" id="event-edit-id">
        <div class="form-group-item">
          <label class="form-field-label">Event Title</label>
          <input type="text" class="input-box-field" id="event-title-input" placeholder="Tokyo Midnight Drag Championship" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Event Banner Image</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="event-image-input" placeholder="https://..." required>
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('event-image-input')">
              <i class="fa-solid fa-folder-open"></i> Gallery
            </button>
          </div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
          <div class="form-group-item">
            <label class="form-field-label">Start Date & Time</label>
            <input type="datetime-local" class="input-box-field" id="event-start-input" required>
          </div>
          <div class="form-group-item">
            <label class="form-field-label">End Date & Time</label>
            <input type="datetime-local" class="input-box-field" id="event-end-input" required>
          </div>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Prizes & Details</label>
          <input type="text" class="input-box-field" id="event-prize-input" placeholder="1st: $500M in-game cash + Exclusive Livery" required>
        </div>
        <div class="form-group-item">
          <label style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.88rem;">
            <input type="checkbox" id="event-is-live-check"> Mark as Currently Live Event
          </label>
        </div>
        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.8rem;">
          <i class="fa-solid fa-calendar-check"></i> Save Event
        </button>
      </form>
    </div>
  </div>

  <!-- 11. Admin Creation & Management Modal -->
  <div class="app-modal-layer" id="modal-admin-editor">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title">Create / Edit Staff Administrator</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-admin-editor')">&times;</button>
      </div>
      <form id="form-admin-editor" onsubmit="event.preventDefault(); saveAdminFromModal();">
        <input type="hidden" id="admin-edit-id">
        <div class="form-group-item">
          <label class="form-field-label">Admin Name</label>
          <input type="text" class="input-box-field" id="admin-name-input" placeholder="e.g. ApexLegend" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Admin Email</label>
          <input type="email" class="input-box-field" id="admin-email-input" placeholder="apex@realdrivingschool.com" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Custom Password</label>
          <input type="password" class="input-box-field" id="admin-pass-input" placeholder="Enter security passphrase" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Device Login Limit</label>
          <select class="select-box-field" id="admin-device-limit-select">
            <option value="1">1 Device (High Security)</option>
            <option value="2" selected>2 Devices (Standard)</option>
            <option value="3">3 Devices</option>
            <option value="5">5 Devices</option>
          </select>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Permissions Assigned</label>
          <div style="display: grid; grid-template-columns: 1fr; gap: 0.45rem; background: var(--bg-base); padding: 0.75rem; border-radius: var(--radius-sm);">
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-cars" checked> Manage Vehicles & Calculator</label>
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-events" checked> Manage Events</label>
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-updates" checked> Publish Updates (Public & Beta)</label>
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-tyres" checked> Manage Tyre Codes</label>
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-maps" checked> Manage Map Guides</label>
            <label style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem;"><input type="checkbox" id="perm-rules" checked> Manage Conduct Rules</label>
          </div>
        </div>
        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.8rem;">
          <i class="fa-solid fa-user-shield"></i> Save Administrator
        </button>
      </form>
    </div>
  </div>

  <!-- 12. UI Customization Modal (For Owner) -->
  <div class="app-modal-layer" id="modal-ui-editor">
    <div class="app-modal-window" style="max-width: 720px;">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-paintbrush"></i> Portal UI & Branding Customizer</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-ui-editor')">&times;</button>
      </div>
      <form id="form-ui-editor" onsubmit="event.preventDefault(); saveUiCustomization();">
        <div class="form-group-item">
          <label class="form-field-label">Portal Game Name</label>
          <input type="text" class="input-box-field" id="ui-game-name-input" placeholder="REAL DRIVING SCHOOL" required>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Portal Logo Image</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="ui-logo-input" placeholder="https://..." required>
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('ui-logo-input')">
              <i class="fa-solid fa-folder-open"></i> Gallery
            </button>
          </div>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">About the Game Summary</label>
          <textarea class="textarea-box-field" id="ui-about-input" rows="3" required></textarea>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Background Media Type</label>
          <select class="select-box-field" id="ui-bg-type-select" onchange="toggleUiBgTypeInputs(this.value)">
            <option value="video">Full Screen Video (.mp4)</option>
            <option value="image">Full Screen Photo / Wallpaper</option>
          </select>
        </div>
        <div class="form-group-item">
          <label class="form-field-label">Background Media Source</label>
          <div style="display: flex; gap: 0.5rem;">
            <input type="url" class="input-box-field" id="ui-bg-media-input" placeholder="https://..." required>
            <button type="button" class="btn-brand-secondary" onclick="openLocalFilePicker('ui-bg-media-input', null, document.getElementById('ui-bg-type-select').value === 'video')">
              <i class="fa-solid fa-folder-open"></i> Gallery / Files
            </button>
          </div>
        </div>
        <h4 style="font-family: var(--font-heading); color: var(--brand-orange); margin: 1rem 0 0.5rem 0;">Social & Download Links</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
          <div class="form-group-item">
            <label class="form-field-label"><i class="fa-brands fa-discord"></i> Discord Invite</label>
            <input type="url" class="input-box-field" id="ui-discord-input">
          </div>
          <div class="form-group-item">
            <label class="form-field-label"><i class="fa-brands fa-instagram"></i> Instagram Link</label>
            <input type="url" class="input-box-field" id="ui-instagram-input">
          </div>
          <div class="form-group-item">
            <label class="form-field-label"><i class="fa-brands fa-google-play"></i> Google Play Link</label>
            <input type="url" class="input-box-field" id="ui-googleplay-input">
          </div>
          <div class="form-group-item">
            <label class="form-field-label"><i class="fa-brands fa-apple"></i> App Store Link</label>
            <input type="url" class="input-box-field" id="ui-appstore-input">
          </div>
        </div>
        <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.85rem; margin-top: 1rem;">
          <i class="fa-solid fa-cloud-arrow-up"></i> Save & Broadcast to Everyone
        </button>
      </form>
    </div>
  </div>

  <!-- 13. Notifications History Modal -->
  <div class="app-modal-layer" id="modal-notifications-list">
    <div class="app-modal-window">
      <div class="modal-headline-row">
        <h3 class="modal-headline-title"><i class="fa-solid fa-bell"></i> Live Notifications</h3>
        <button class="modal-close-cross" onclick="closeAppModal('modal-notifications-list')">&times;</button>
      </div>
      <div id="notifications-modal-list" style="display: flex; flex-direction: column; gap: 0.75rem;">
        <!-- Filled dynamically -->
      </div>
    </div>
  </div>
'''
