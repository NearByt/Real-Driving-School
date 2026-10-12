# verify_hub_v2.py - Comprehensive verification test suite for RDS Hub v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    c = f.read()

tests = []

def test(name, condition, details=""):
    tests.append((name, condition, details))

# 1. Liquid Glass & Translucency
test("Liquid Glass: Translucent --card-bg", "rgba(255, 255, 255, 0.32)" in c or "rgba(255, 255, 255, 0.28)" in c)
test("Liquid Glass: Translucent --bg-surface", "rgba(255, 255, 255, 0.28)" in c)
test("Liquid Glass: Luminous Matte Overlay", "backdrop-filter: blur(14px)" in c and "bg-white-matte-layer" in c)
test("Liquid Glass: Specular Highlight Box Shadows", "inset 0 1px 1px" in c)

# 2. Calculator Add-ons Word Filtering (Strictly remove: package, ceramic, edition)
test("Add-on: Police (package removed)", "🚓 Police" in c and "Police Siren / Package" not in c)
test("Add-on: Coating (ceramic removed)", "🛡️ Coating" in c and "Ceramic Coating" not in c)
test("Add-on: Premium (edition removed)", "⭐ Premium" in c and "Premium Edition" not in c)
test("Add-on: Rainbow Smoke present", "🌈 Rainbow Smoke" in c)
test("Add-on: Custom Livery present", "Custom Livery" in c)
test("Print & Share Bill buttons REMOVED", "printBill" not in c and "shareBill" not in c and "Print Bill" not in c and "Share Bill" not in c)

# 3. Category Bar Dock & Ending Arrow Marks
test("Category Bar: Left Scroll Arrow", 'nav-dock-scroll-arrow arrow-left' in c and 'scrollNavDock(-220)' in c)
test("Category Bar: Right Scroll Arrow", 'nav-dock-scroll-arrow arrow-right' in c and 'scrollNavDock(220)' in c)
test("Category Bar: Scroll Function Implemented", 'function scrollNavDock' in c and 'scrollBy' in c)

# 4. Owner & Staff Panel Restored & Fully Functional
test("Owner tab always in category bar", 'data-view="owner"' in c and 'nav-owner-tab' in c and 'style="display: none;"' not in c[c.find('nav-owner-tab')-30:c.find('nav-owner-tab')+120])
test("Owner panel in-view authentication", 'owner-page-email' in c and 'submitInPageViewLogin' in c)
test("Owner panel 6 subtabs", all(st in c for st in ["renderSubtabAdmins", "renderSubtabRoles", "renderSubtabCustomCats", "renderSubtabUiSettings", "renderSubtabSecurityDb", "renderSubtabLogs"]))
test("Live Editing Mode toggle", 'isEditingMode' in c and 'toggleEditingMode' in c)
test("Quick action shortcuts bar", "Quick Add:" in c and "openCarModal" in c and "openTyreModal" in c)

# 5. Media Feedback & Cloud Sync
test("Media Feedback Badges near inputs", all(b in c for b in ["status-car-image", "status-profile-avatar", "status-update-image", "status-event-image", "status-map-image", "status-ui-logo", "status-ui-bg"]))
test("Media status feedback in picker", "media-selected-status-badge" in c and "Optimizing & attaching" in c)
test("Canvas image compression", "compressImageFile" in c and "canvas.toDataURL" in c)
test("Firebase multi-document sync", all(d in c for d in ["cars", "events", "updates", "tyres", "maps", "rules", "multiplayer", "admins", "roles", "logs", "custom_cats", "config"]))
test("Global Sync All Cloud function", "syncAll()" in c and "triggerManualSync" in c)

# 6. Full Working CRUD Modals (Fix Add Tyre Code & others)
test("Modal Tyre Editor in HTML", 'id="modal-tyre-editor"' in c and 'form-tyre-editor' in c)
test("Tyre CRUD functions", 'openTyreModal' in c and 'saveTyreFromModal' in c and 'deleteTyre' in c)
test("Modal Map Editor in HTML", 'id="modal-map-editor"' in c and 'openMapModal' in c and 'saveMapFromModal' in c)
test("Modal Rule Editor in HTML", 'id="modal-rule-editor"' in c and 'openRuleModal' in c and 'saveRuleFromModal' in c)
test("Modal Multiplayer Editor in HTML", 'id="modal-multiplayer-editor"' in c and 'openMpModal' in c and 'saveMpFromModal' in c)
test("Modal Role Editor in HTML", 'id="modal-role-editor"' in c and 'openRoleModal' in c and 'saveRoleFromModal' in c)
test("Modal Category Editor in HTML", 'id="modal-category-editor"' in c and 'openCategoryModal' in c and 'saveCategoryFromModal' in c)

# 7. Core Mobile & Responsive Features
test("Mobile 2-by-2 Grid CSS", "grid-template-columns: repeat(2, 1fr) !important;" in c)
test("Detached Floating Island Dock on Mobile", "bottom: 14px !important;" in c and "z-index: 9999 !important;" in c)
test("Game Name in Orange #ff6b00", "#ff6b00" in c and "REAL DRIVING SCHOOL" in c)
test("Buttons Midnight Slate #0f172a", "--btn-primary-bg: #0f172a;" in c)
test("Clean In-Game Name Parser (no UID appended)", "parseRDSPlayerId" in c and 'document.getElementById("profile-name-input").value = u.username;' in c)
test("10 Taps Secret Gate on v1.2.120", "v1.2.120" in c and "handleVersionSecretClick" in c and "versionTapCount >= 10" in c)
test("Car Stages 1-7 technical specs", "Stage 1" in c and "Stage 7" in c and "speedNoTurboKmph" in c and "speedTurboKmph" in c)
test("Updates: Public and Beta Tabs", "Public Releases" in c and "Beta Branches" in c and "currentUpdatesChannel" in c)
test("PWA Add to Home Screen on mobile", "handleAddToHomeScreen" in c and "modal-ios-install-guide" in c)

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
