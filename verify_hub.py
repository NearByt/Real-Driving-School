# verify_hub.py - Comprehensive Verification Test Suite for Real Driving School Portal
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    c = f.read()

tests = []

def test(name, condition, details=""):
    tests.append((name, condition, details))

# 1. Colors & Branding
test("Game Name in Orange", "#ff6b00" in c and "REAL DRIVING SCHOOL" in c)
test("Button Primary uses Midnight Slate", "--btn-primary-bg: #0f172a;" in c)
test("Theme Switcher (4 themes)", all(t in c for t in ["frost", "stealth", "velocity", "carbon"]))

# 2. Splash Screen Fixes
test("Splash Logo has NO photo viewer onclick", '<img src="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=200&q=80" alt="Game Logo" class="splash-game-logo" id="splash-main-logo">' in c)
test("UTC Timezone removed", "UTC+5.5" not in c and "Asia/Calcutta" not in c)
test("Continue button present", 'btn-splash-continue' in c and 'proceedToHub()' in c)
test("Background video/image proper toggle", 'videoEl.style.display = "none"' in c and 'imageEl.style.display = "block"' in c)

# 3. Mobile Header & 2-by-2 Grid
test("Mobile 2-by-2 Grid CSS", "grid-template-columns: repeat(2, 1fr) !important;" in c)
test("Detached Floating Bottom Island Dock on Mobile", "bottom: 14px !important;" in c and "z-index: 9999 !important;" in c)
test("Cloud Sync Badge in Header", 'id="header-sync-pill"' in c)
test("Driver Profile Pill in Header", 'class="hub-user-pill"' in c and 'openDriverProfileModal()' in c)
test("Settings Gear in Header", 'openAppModal(\'modal-app-settings\')' in c)

# 4. Navigation Bar PC features
test("Mouse wheel horizontal scroll", 'catBar.addEventListener("wheel"' in c and 'catBar.scrollLeft += e.deltaY' in c)
test("Nav position switcher in Settings", 'setting-nav-position' in c and 'changeNavPosition' in c)

# 5. Cloud Multi-Device Sync ($0 Free Tier)
test("Firebase config rds-a95fc", 'AIzaSyBlRiz74eFt5zWOIowVEOgxQEAHuLfM3e0' in c and 'rds-a95fc' in c)
test("Multi-document split under rds_hub", all(d in c for d in ["cars", "events", "updates", "tyres", "maps", "rules", "admins", "logs", "config"]))
test("Canvas image compression", "compressImageFile" in c and "canvas.toDataURL" in c)
test("Anonymous auth call", "signInAnonymously" in c)

# 6. Car Prices & Calculator
test("Real-time car search input", "filterCarCatalog" in c and "🔍 Search car by name" in c)
test("Jump to Calculator button", "jumpToCalculator" in c)
test("Stages 1 to 7 individual specs in editor", all(f"st-${{s}}" in c or f"STAGE ${{s}}" in c for s in [1, 2, 3, 4, 5, 6, 7]))
test("Custom stage > 7 extrapolation with disclaimer", "is an approximate valuation based on exponential stage scaling" in c)
test("4 Add-ons: Rainbow, Police, Coating, Premium", all(a in c for a in ["Rainbow Smoke", "Police Siren", "Ceramic Coating", "Premium Edition"]))
test("Custom Livery with custom price", "Custom Livery" in c and "calcCustomLiveryPrice" in c)
test("Print Bill and Share Bill buttons REMOVED", "printBill" not in c and "Print Bill" not in c and "shareBill" not in c and "Share Bill" not in c)
test("Approx valuation range in numbers", "Valuation Range" in c and "minTotal" in c and "maxTotal" in c)

# 7. RDS Updates: Public & Beta Tabs
test("2 distinct tabs: Public & Beta Updates", "Public Releases" in c and "Beta Branches" in c and "currentUpdatesChannel" in c)
test("Update release channel selector in modal", "update-channel-select" in c and "🌐 Public Update" in c and "🧪 Beta Update" in c)

# 8. Mobile PWA Add to Home Screen
test("Add to Home Screen in Settings for mobile", "pwa-install-container" in c and "handleAddToHomeScreen" in c)
test("iOS Safari install guide modal", "modal-ios-install-guide" in c and "Add to Home Screen" in c)

# 9. Driver Onboarding & Clean Username
test("Driver onboarding modal on Continue", "modal-driver-onboarding" in c and "confirmOnboarding" in c)
test("RDS Player ID parsing strips UID", "parseRDSPlayerId" in c and "cleanName" in c and "gameUid" in c)
test("Does NOT append UID to input value", 'document.getElementById("profile-name-input").value = u.username;' in c)

# 10. Staff Login Security
test("10 taps secret gate on v1.2.120", "v1.2.120" in c and "handleVersionSecretClick" in c and "versionTapCount >= 10" in c)
test("Staff modal strictly requires email & password", "modal-staff-login" in c and "staff-email-input" in c and "staff-pass-input" in c)
test("Owner Master credentials intact", "pennabadicharith@gmail.com" in c and "Cherry1111" in c)
test("Admin custom passwords support", "adm.password" in c and "admin-pass-input" in c)

# 11. Background Motion & Online Users
test("Canvas dynamic particles motion", "bg-motion-canvas" in c and "MotionEngine" in c)
test("Active Grinders shows clean username", "renderGrinders" in c and "Active Grinders & Online Drivers" in c)

# 12. Preserved features
test("Tyre codes with one-click copy", "copyTyreCode" in c and "navigator.clipboard.writeText" in c)
test("Secret locations and map guides", "renderMaps" in c and "Secret Locations" in c)
test("Multiplayer guides and clan etiquette", "renderMultiplayer" in c and "Clan Etiquette" in c)
test("Rules of conduct", "renderRules" in c and "Rules of Conduct" in c)
test("Audit logs", "renderOwnerPanel" in c and "auditLogs" in c)

print("=" * 60)
print("TEST RESULTS:")
print("=" * 60)
passed = 0
failed = 0
for name, ok, details in tests:
    status = "PASS" if ok else "FAIL"
    if ok: passed += 1
    else: failed += 1
    print(f"[{status}] {name}")
    if not ok and details:
        print(f"       Details: {details}")

print("=" * 60)
print(f"Summary: {passed} PASSED, {failed} FAILED out of {len(tests)} tests.")
print("=" * 60)

if failed > 0:
    sys.exit(1)
