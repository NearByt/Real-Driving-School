# Real Driving School (RDS) - Official Portal & Valuation Hub

A professional, motion-graphics **White Theme Liquid Glass** website for **Real Driving School (RDS)** with full-screen background video/photo canvas, high-energy racing orange branding, workable notifications, Discord-style roles, separate Owner category, and zero-budget anti-hacking cloud security.

---

## 🎨 New Design & Architecture Highlights

### 1. Full-Screen Splash / Welcome Screen (No Boxed Look)
- **Full Screen Canvas**: Covers 100% of the screen (`100vw`, `100vh`) with sports car gameplay video or high-res photo in the background, overlaid with a frosted white blur liquid glass layer (`backdrop-filter: blur(24px)`).
- **Left Side Identity**:
  - Game Logo (clickable with full-screen photo lightbox viewer).
  - Game Name in a single **straight line** in vibrant **ORANGE**: `REAL DRIVING SCHOOL` (all "RDS Hub" subtext removed).
  - Clean, small about text describing the game.
  - Social buttons (Discord, Instagram, Google Play) and user's local timezone indicator.
- **Middle Down Continue Button**: A prominent glowing orange button with right arrow: `CONTINUE →` that smoothly opens the Main Web Hub.

### 2. Main Web Hub (Pinned Sticky Top Navigation)
- **Stays Still on Scroll**: The top navigation bar is pinned (`position: sticky; top: 0; z-index: 1000`) so it never moves when scrolling, with frosted liquid glass showing the page content gliding underneath.
- **Straight Line Title**: `REAL DRIVING SCHOOL` displayed prominently in orange.
- **Horizontally Scrollable Categories**: Smoothly swipe or scroll left/right on both mobile and desktop:
  - 🚗 Car Prices
  - 🛞 Tyre Codes
  - 🏆 Events (with Live Now, Upcoming, and Past)
  - 📜 Rules
  - 🗺️ Map Guide
  - 🚀 Updates
  - 👥 Multiplayer
  - 👑 **Owner Panel** (Separate dedicated category appearing when logged in as Owner)

### 3. Separate Category for Owner (`pennabadicharith@gmail.com`)
When logged in with the Owner account (`pennabadicharith@gmail.com` / `Cherry1111`), a dedicated **👑 Owner Panel** category appears in the top navigation bar with 5 specialized tabs:
1. 🎨 **Live UI & Background Controller**: Change background video URL, photo URL, Game Name, logo, about text, Discord link, and Instagram link live!
2. 👥 **Create & Manage Admins**: Add admins, set email, username, device login limits, and granular category permission checkboxes.
3. 🔑 **Database Key & Cloud Sync**: Configure free Google Firebase Firestore or REST database endpoints to sync changes, pictures, and videos to all users worldwide for $0!
4. 🏷️ **Discord-Style Roles**: Add custom roles and set hex colors.
5. 📜 **Categorized Audit Logs**: Dedicated filter tabs for All Logs, Login Logs, Content Changes, and System Logs with timestamps and user info.

### 4. In-Site Modal UI (No Browser Prompts!)
- Zero ugly browser `prompt()` dialogs! Everything opens in clean in-site modal dialogs.
- **Clickable Photos & Lightbox Viewer**: Clicking any car photo, event image, tyre compound, or map photo opens an interactive **Lightbox Viewer** with full-resolution zoom and an *"Open Full Image Link"* button.

### 5. Car Prices Calculator & Custom Stage
- Displays vehicles strictly in designated order (`#1`, `#2`, etc.).
- Clicking "Specs" opens an itemized technical data modal without summing up prices.
- **Custom Stage Input**: Users can enter any custom stage number (e.g. 7, 8, 10, 15) and the calculator computes the progressive valuation and speed boost automatically with the extrapolation formula!
- Add-on options: Rainbow Exhaust Smoke and Custom Livery (works package, lights, and ceramic removed as requested).
- In car creation form: Stage 7 is removed from being asked (Stage 1 to 6 asked, Stage 7+ is extrapolated).
- **Luxury Bill Receipt**: Clean invoice with subtotal, exact numbers, estimated market range (e.g., `100M - 120M`), and Print/Share buttons.

### 6. Events with Current Live Event (No "Set Alert" for Live Events)
- 3 Event Tabs: 🔴 **LIVE NOW (Current Events)**, ⏳ **Upcoming Events**, 📜 **Past Records**.
- For Live Events, the "Set Alert" button is removed and replaced with a **"Join Lobby Now"** button displaying the active room PIN!
- "Set Alert" is kept only for Upcoming Events.

### 7. Global Timezone Support & Privacy
- Automatically detects the visitor's local timezone (e.g. `UTC+5.5 (IST)` or `UTC-4 (EDT)`) and displays all event and update timestamps in their local time.
- In login modals, email placeholders are kept neutral (`example@domain.com`) to protect owner privacy.
- Includes **Sign in with Google** button for seamless driver authentication.
