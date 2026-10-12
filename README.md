# Real Driving School (RDS) - Official Portal & Valuation Hub

A professional, motion-graphics **White Theme Liquid Glass** website for **Real Driving School (RDS)** with full-screen background video/photo canvas, ambient dynamic speed lighting, high-energy racing orange branding, workable notifications, Discord-style roles, separate Owner category, and zero-budget anti-hacking cloud security powered by Google Firebase.

---

## 🚀 What's New in v1.2.120

### 1. Pre-Connected Real-Time Firebase Cloud Sync ($0 Budget)
- Pre-configured with your Firebase project:
  - **Project ID**: `rds-a95fc`
  - **Storage Bucket**: `rds-a95fc.firebasestorage.app`
  - **Realtime Firestore**: Every car added, tyre code created, event scheduled, or update posted synchronizes across all users' devices worldwide in real time!

### 2. Ambient Motion Graphics & Dynamic Background
- Dynamic ambient lighting layer with glowing neon speed trails, floating cyber-blobs, and racing particles that float smoothly across the screen.
- Can be toggled on/off in the new **Portal Settings** modal.

### 3. Mobile Detached Floating Island Category Dock
- **On Mobile Devices**: The category bar automatically becomes a sleek floating island dock positioned slightly above the bottom of the screen (detached from edges) with rounded capsule styling and frosted glassmorphism.
- **On Desktop / PC**: Category bar supports horizontal mouse-wheel scrolling (`wheel`) and click-and-drag panning.
- **Settings Toggle**: In the new Settings modal, players can choose between `Auto (Floating Bottom on Mobile, Top on PC)`, `Floating Bottom Dock (Always)`, or `Top Navigation Bar (Always)`.

### 4. Secret Staff Login (Easter Egg Access)
- The visible "Staff Login" button has been completely removed from public view.
- To access staff/owner authentication:
  1. Click the **Gear (Settings)** icon in the top header.
  2. Scroll to the very bottom of the Settings window to see: `Web Version: v1.2.120`.
  3. **Tap / Click on `v1.2.120` 10 times**.
  4. On the 10th tap, the Staff & Owner Login window will unlock and pop up!

### 5. In-Game Player ID Parser
- When setting up their profile, drivers are instructed to copy their ID string directly from inside **Real Driving School** (e.g. `「 ⚡| Hyper_DαʀкSтαʀ 」 FIc9Z16zj4VF6Jhqm0UOCUHYwTb2`).
- The portal automatically strips the account UID hash and displays **only the clean in-game name** (`「 ⚡| Hyper_DαʀкSтαʀ 」`) on their driver pill, receipts, and leaderboards!

### 6. Local Gallery & Files Upload Everywhere
- Every media input across the entire platform (cars, tyre codes, events, map guides, updates, multiplayer rooms, profile avatars, and custom background videos) now features a **"📁 Gallery / Files"** button allowing direct selection from phone gallery or PC files.
- Automatically uploads to Firebase Storage or converts to a permanent DataURL.

### 7. Active Logged-In Drivers Tracker (Owner Panel)
- Owner Panel now features an **"Active Drivers & Online Users"** sub-tab that displays live statistics:
  - Total count of drivers currently online.
  - Live table listing in-game display names, game account UIDs, roles, device fingerprints, and real-time status.

### 8. Custom Admin Passwords
- When creating or editing staff admins in the Owner Panel, the Owner can now set custom passwords for each admin email, and admins log in using their own passwords.
- Device login limits are strictly enforced per account.

### 9. Social & Store Links
- Splash screen top bar includes links for **Discord**, **Instagram**, **Google Play**, and **Apple App Store**.
- All 4 links can be edited in real time by the Owner in the **Live UI Controller** tab.

---

## 🛠️ Deployment to GitHub Pages

1. Drag and drop `index.html` into your GitHub repository root.
2. Go to **Settings** → **Pages** → Source: `Deploy from a branch` → Branch: `main` → `/root` → **Save**.
3. Your website is instantly live at `https://<your-username>.github.io/<repo-name>/`.
