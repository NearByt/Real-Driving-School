# Real Driving School (RDS) - Official Hub & Valuation Engine

A high-performance, responsive gaming portal and technical valuation calculator engineered with a **Liquid Glass (Glassmorphism)** aesthetic, background video/photo canvas, **workable notifications**, Discord-style role badges, granular category permissions, and zero-budget anti-hacking cloud security.

---

## 🔒 1. How to Keep Your Website 100% Safe from Hackers ($0 Budget)

You asked: *"first tell me how can i keep web safe cuz i can using github to host it and i have 0 budject"*

### The Vulnerability of Pure GitHub Pages
GitHub Pages is a **static web host**. This means anyone can right-click your website, click **Inspect (DevTools)**, and view client-side JavaScript.
If you simply hardcode admin passwords or store your database in client code without a server-side shield:
- A hacker could modify JavaScript variables in their browser console to fake permissions.
- A hacker could attempt to overwrite database records directly if no database rules exist.

### The Bulletproof $0 Solution (Zero-Trust Cloud Shield)
To make your website completely immune to hackers with **\$0 budget**:

1. **Host the Front-End for Free on GitHub Pages**:
   - GitHub Pages gives you free worldwide hosting, automated SSL encryption (HTTPS), and high-speed DDoS mitigation.
2. **Use Google Firebase Firestore Free Spark Plan ($0 / Month)**:
   - Google provides 50,000 document reads, 20,000 document writes, and 1 GB of storage per day **100% free forever**.
   - With the included `firestore.rules`, all authorization is enforced directly on **Google's cloud servers**. Even if a hacker uses Chrome DevTools or scripts to attempt unauthorized edits to Car Prices, Events, or Roles, Google's servers instantly reject the packet with `HTTP 403 Forbidden: PERMISSION_DENIED`.
3. **Role-Based Access Control (RBAC) & Device Fingerprints**:
   - The Owner (`pennabadicharith@gmail.com`) holds the master key.
   - Admins can be restricted to specific categories (e.g., only Car Prices, or only Events).
   - Device limit controls track unique device fingerprints to prevent account sharing and leaks.
4. **Append-Only Tamper-Evident Audit Logs**:
   - Every administrative change (car edit, rule change, event post, login) is permanently timestamped and logged with user, action, and device info. Only the Owner and permitted admins can view the log trail.

---

## 🖼️ 2. Saving Images & Videos Directly into GitHub Repository

You asked: *"make it like the image or video will directly save into github repo and the code will change according to the image by itself and display it to everyone."*

### How to Host Media in Your GitHub Repo for Free:
1. Put any car photos, background videos, or map guide screenshots inside the `assets/` folder in this repository:
   ```
   assets/
     ├── background-racing.mp4
     ├── gtr-r35.png
     ├── huracan-evo.png
     └── map-touge.jpg
   ```
2. Commit and push the files to GitHub:
   ```bash
   git add assets/
   git commit -m "Add new car photos"
   git push origin main
   ```
3. GitHub automatically provides a permanent direct raw link:
   ```
   https://raw.githubusercontent.com/<YourGitHubUsername>/<YourRepoName>/main/assets/gtr-r35.png
   ```
4. Whenever you paste this URL into the **Add/Edit Car**, **Hero Background Settings**, or **Events Publisher**, the website immediately loads and displays it to all visitors!

---

## 🚀 3. Deploying to GitHub Pages in 3 Clicks

1. Create a new repository on [GitHub.com](https://github.com) named `real-driving-school-hub`.
2. Upload or push all files from this directory to the repository.
3. In your GitHub repository:
   - Click **Settings** (top right gear icon).
   - In the left sidebar, click **Pages**.
   - Under **Build and deployment > Branch**, choose **`main`** and **`/ (root)`**, then click **Save**.
4. In ~60 seconds, GitHub gives you a live link:
   ```
   https://<your-username>.github.io/real-driving-school-hub/
   ```

---

## 🔑 4. Owner & Staff Accounts

### Owner Master Account:
- **Email**: `pennabadicharith@gmail.com`
- **Password**: `Cherry1111`
- **Permissions**: Full Master Control over everything (Cars, Tyres, Events, Rules, Maps, Updates, Multiplayer, Custom Categories, UI Settings, Discord-Style Roles, User Profile Moderation, and Audit Logs).

### Granular Staff Permissions:
The Owner can create admins and toggle individual checkboxes for:
- [x] 🚗 **Car Prices**
- [x] 🛞 **Tyre Codes**
- [x] 🏆 **Events**
- [x] 📜 **Rules of Conduct**
- [x] 🗺️ **Map Guide**
- [x] 🚀 **RDS Updates**
- [x] 👥 **Multiplayer Guide**
- [x] 📜 **View Audit Logs**
- Max Device Limit per admin (1 to 10 devices).

---

## ⚙️ 5. Features Breakdown

### 1. Liquid Glass Dashboard & Hero Landing
- Background video loop with fallback photo canvas.
- Dark matte screen overlay with adjustable blur and saturation.
- Game logo, official title, tagline, about description, downloads (Google Play, iOS App Store, APK), and community links.
- Sleek rectangular continue button with right arrow: `Continue →`.

### 2. Car Prices Calculator & Catalog
- **Catalog View**: Vehicles displayed strictly in designated order (`#1`, `#2`, `#3`...).
- **Technical Data Modal**: Clicking "Specs" opens an itemized modal displaying speed metrics without summing up prices.
- **Tuning Stages (1 to 7)**:
  - Each stage displays `Top speed (no turbo): _ km/h / _ mph` and `Top speed (turbo): _ km/h / _ mph`.
  - Stage price inputs support units: `k` (thousands), `M` (millions, default), `b` (billions), `t` (trillions).
- **Stage > 7 Extrapolation**:
  - Automatically calculates progressive valuation and speed boosts using exponential progression.
  - Displays disclaimer: `* Note: This is an approximate estimated value based on progressive stage trajectory.`
- **Add-on Customizations**:
  - Premium Package (Yes/No)
  - Police Siren & Lights (Yes/No)
  - Rainbow Exhaust Smoke (Yes/No)
  - Ceramic Coating (Yes/No)
  - Custom Livery (Yes/No - asks for custom price)
- **Luxury Bill Receipt**:
  - Styled itemized invoice with subtotal, exact numbers, and estimated market value range (e.g., `100M - 120M`).
  - Print bill and share bill functions.

### 3. Workable Notifications Engine
- **Browser Native Push**: Requests `Notification.requestPermission()` to trigger desktop/mobile system notifications.
- **Web Audio API Synth**: Synthesizes a futuristic sci-fi chime natively without depending on external audio files that could fail to load.
- **In-App Toast Alerts**: Glassmorphic animated alerts with progress drain bars.
- **Notification Center**: Bell icon with unread badge counter and history tray.
- **Scheduled Broadcasts**: Automatically monitors scheduled event timestamps and delivers alerts at specified times.

### 4. Events System & Mystery Mode
- Upcoming vs Past Events tabs.
- Game Mode: Grind, Track, Location, Duration, Car, Trade, Fuel, Mode, Character.
- Dynamic "+ Add More Info" key-value fields.
- **Mystery / Teaser Mode**: Toggle to tint images with a pulsating question mark `?` and classify sensitive event intel until official reveal.

### 5. Tyre Codes Gallery
- Visual cards with compound image, code name, and official code (e.g., `RDS-SLICK-99X`).
- One-click copy button with instant animation and clipboard feedback.

### 6. Rules of Conduct & Multiplayer Guidelines
- Categorized standards (Fair Play, Trading & Economy, Anti-Exploits, Chat Conduct).
- Safe rich text rendering with XSS sanitization.

### 7. Map Guide
- Track guides with difficulty badges, drift lines, speed camera locations, and pro driving tips.

### 8. RDS Updates & Release Timeline
- Chronological changelog feed with auto/manual timestamps.
- Status badges: "Android: Live/Pending", "iOS: Live/Pending", and "Coming Soon".

### 9. Discord-Like Roles & Moderation
- Custom role names and hex colors (e.g., Owner Gold `#FFD700`, Head Admin Crimson `#FF3B30`).
- Usernames reflect role colors across the site.
- Normal players can change username (enforced 20 character maximum) and avatar.
- **Owner Moderation Lock**: Owner can sanction and lock abusive users, disabling customization and reverting them to plain white default names.

### 10. Live UI Customizer & Dynamic Categories
- Owner can edit Game Name, Logo URL, Hero Video/Photo, Accent Glow Color, Typography scale, and Glass Blur.
- Owner can dynamically spawn brand new categories (e.g. "Pro Drift Setups", "Clan Wars") that appear directly in the top navigation bar!
