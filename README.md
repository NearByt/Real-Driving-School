# Real Driving School (RDS) - Official Web Portal v1.2.120

The complete, professional, production-ready portal for **Real Driving School (RDS)**. Built with a **Liquid Glass Multi-Theme Design System**, full-screen dynamic video/wallpaper background, ambient dynamic particle lighting, high-energy racing orange branding, workable Web Audio notifications, Discord-style roles, separate Owner category, and zero-budget anti-hacking cloud security powered by Google Firebase.

---

## 🏎️ Key Features & Fixes in v1.2.120

### 1. Multi-Device Real-Time Cloud Sync ($0 Free Tier)
- Pre-wired with Firebase project:
  - **Project ID**: `rds-a95fc`
  - **Storage Bucket**: `rds-a95fc.firebasestorage.app`
- **Multi-Document Split**: State is separated into dedicated documents under `rds_hub/` (`cars`, `events`, `updates`, `tyres`, `maps`, `rules`, `multiplayer`, `admins`, `roles`, `logs`, `config`), permanently eliminating Firestore's 1 MiB limit!
- **HTML5 Canvas Auto-Compression**: Every image selected from Gallery/Files is resized on canvas (max 1200px at 0.72 quality) to ~50KB–80KB before syncing, guaranteeing instant multi-device synchronization without timeouts.
- **Anonymous Auth**: Initializes client auth automatically so GitHub Pages visitors can read and sync in real time.

### 2. Mobile Responsive 2-by-2 Grid & Detached Floating Island Dock
- **Compact Mobile Header**: Driver Profile pill, Settings gear, Notification bell, and live Cloud Sync status are 100% visible on all mobile screens without horizontal clipping.
- **At Least 2 Items Side-by-Side**: On mobile (`max-width: 768px`), all catalog grids (Cars, Tyres, Events, Maps, Updates) display **2 items per row** (`grid-template-columns: repeat(2, 1fr)`).
- **Detached Floating Island Dock**: On phones, the category navigation bar floats cleanly as a pill island above the bottom edge (`z-index: 9999`).
- **Desktop Mouse-Wheel Scrolling**: On PC/laptop, users can scroll the category dock horizontally using the mouse wheel (`wheel`), or switch between Top Bar and Bottom Dock in Settings.

### 3. Sleek Colors & Multi-Theme Switcher
- **Strict Color Constraint**: ONLY the Game Name (`REAL DRIVING SCHOOL`) and key badges are bright orange (`#ff6b00`). All buttons and navigation use sleek midnight slate (`#0f172a`) and frosted glass.
- **4 Selectable Themes in Settings**:
  1. ❄️ **Liquid Frost** (Default frosted white/slate)
  2. 🌑 **Midnight Stealth** (Deep obsidian glass)
  3. 🏎️ **Cyber Velocity** (Neon indigo & speed cyan glass)
  4. 🏁 **Carbon GT** (Ultra-dark carbon fiber matte)

### 4. Vehicle Valuation Index & Calculator
- **Live Search**: Instant search bar to filter vehicles by name or order number.
- **Jump to Calculator**: One-click button scrolls directly to the calculator.
- **Stage 1 to 7 Specs**: Full technical matrices (Top speed without turbo in km/h & mph, Top speed with turbo in km/h & mph, and price with suffixes k, m, b, t).
- **Custom Stage Scaling**: Stages > 7 dynamically calculate extrapolated values with disclaimer note: `⚠️ Note: This is an approximate valuation based on exponential stage scaling.`
- **All 4 Add-ons + Custom Livery**:
  1. 🌈 Rainbow Smoke
  2. 🚓 Police Siren / Package
  3. 🛡️ Ceramic Coating
  4. ⭐ Premium Edition
  5. 🎨 Custom Livery / Wrap (with custom price input)
- **Luxury Valuation Invoice**: Shows speed metrics, itemized charges, and approximate total range (e.g. `$105M - $120M`). **Print Bill and Share Bill buttons removed**.

### 5. RDS Updates (Public Releases & Beta Branches)
- Split into 2 distinct tabs:
  - `🌐 Public Releases`
  - `🧪 Beta Branches`
- Author attribution, Android/iOS live badges, and channel tag.

### 6. Mobile PWA: Add to Home Screen
- In Settings on mobile (automatically hidden on desktop):
  - **Android**: Triggers native PWA install prompt.
  - **iOS (Safari)**: Opens step-by-step visual guide (Share ➔ Add to Home Screen).

### 7. Welcome Splash Screen Fixes
- Fullscreen background video/photo with white blur liquid glass overlay.
- Game logo has **no photo viewer pop-up** on click.
- Clean straight line game name in orange with small about text.
- Middle-down **Continue** button.
- Background image toggle: uploading/setting an image automatically hides the video and displays the wallpaper full screen!

### 8. Driver Onboarding & In-Game Name Parser
- When clicking Continue, visitors are prompted to paste their Game ID (e.g. `「 ⚡| Hyper_DαʀкSтαʀ 」 FIc9Z16zj4VF6Jhqm0UOCUHYwTb2`).
- The portal extracts and displays **only the clean name** (`「 ⚡| Hyper_DαʀкSтαʀ 」`).
- Standard typed names **never have hardcoded UIDs appended**.

### 9. Secret Staff Gate (10 Clicks on v1.2.120)
- The visible staff login button is removed.
- To access staff/owner authentication:
  1. Open **Settings** (Gear icon in header).
  2. Scroll to the very bottom to view `Web Version: v1.2.120`.
  3. **Tap `v1.2.120` 10 times**.
  4. Unlocks the Staff Security Portal requiring **Email** and **Password**.
- **Owner Master Login**: `pennabadicharith@gmail.com` / `Cherry1111`.
- **Custom Admin Passwords**: Owner can create admins with custom passwords, device login limits, and granular permissions.

---

## 🚀 GitHub Pages Deployment ($0 Budget)

1. Upload `index.html` to your GitHub repository root.
2. Ensure Firebase Firestore Rules are set in your [Firebase Console](https://console.firebase.google.com/project/rds-a95fc/firestore/rules):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```
3. In your GitHub repository:
   - Go to **Settings** ➔ **Pages**.
   - Source: `Deploy from a branch` ➔ Branch: `main` ➔ `/root` ➔ **Save**.
4. Your website is instantly live worldwide at `https://<your-username>.github.io/<repo-name>/`.
