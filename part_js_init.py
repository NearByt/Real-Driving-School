# part_js_init.py - Modals, CRUD Handlers & Bootstrap for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

JS_INIT_CONTENT = r'''
    /* ==========================================================================
       MODALS, NOTIFICATIONS & TOAST NOTIFICATIONS
       ========================================================================== */
    function openAppModal(id) {
      const el = document.getElementById(id);
      if (el) el.classList.add("active");
    }

    function closeAppModal(id) {
      const el = document.getElementById(id);
      if (el) el.classList.remove("active");
    }

    function openPhotoViewer(url, title = "") {
      const modal = document.getElementById("modal-photo-viewer");
      const img = document.getElementById("photo-viewer-image");
      const cap = document.getElementById("photo-viewer-caption");
      if (modal && img) {
        img.src = url;
        if (cap) cap.textContent = title;
        modal.classList.add("active");
      }
    }

    function closePhotoViewer() {
      const modal = document.getElementById("modal-photo-viewer");
      if (modal) modal.classList.remove("active");
    }

    function showToast(msg, type = "info") {
      let toast = document.getElementById("app-floating-toast");
      if (!toast) {
        toast = document.createElement("div");
        toast.id = "app-floating-toast";
        toast.style.cssText = `
          position: fixed;
          bottom: 24px;
          right: 24px;
          z-index: 99999;
          background: #0f172a;
          color: #fff;
          padding: 0.75rem 1.25rem;
          border-radius: 9999px;
          font-size: 0.85rem;
          font-weight: 600;
          box-shadow: 0 10px 30px rgba(0,0,0,0.3);
          border: 1px solid rgba(255,255,255,0.2);
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: transform 0.3s ease, opacity 0.3s ease;
          pointer-events: none;
        `;
        document.body.appendChild(toast);
      }
      toast.textContent = msg;
      toast.style.opacity = "1";
      toast.style.transform = "translateY(0)";
      clearTimeout(toast._timer);
      toast._timer = setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(15px)";
      }, 3200);
    }

    function showSyncPill(text = "Cloud Synced") {
      const pill = document.getElementById("header-sync-pill");
      const pillText = document.getElementById("sync-pill-text");
      if (pillText) pillText.textContent = text;
      if (pill) {
        pill.style.display = "inline-flex";
        pill.style.borderColor = "rgba(22, 163, 74, 0.5)";
      }
    }

    /* ==========================================================================
       SPLASH SCREEN & ONBOARDING SYSTEM
       ========================================================================== */
    function proceedToHub() {
      const isOnboarded = localStorage.getItem("RDS_ONBOARDED") === "true";
      if (!isOnboarded) {
        openAppModal("modal-driver-onboarding");
      } else {
        enterHubDirectly();
      }
    }

    function handleOnboardingInput(val) {
      const parsed = parseRDSPlayerId(val);
      const box = document.getElementById("onboarding-detected-box");
      const nameEl = document.getElementById("onboarding-extracted-name");
      if (parsed.cleanName && parsed.cleanName !== "StreetRacer") {
        if (box) box.style.display = "block";
        if (nameEl) nameEl.textContent = parsed.cleanName;
      } else {
        if (box) box.style.display = "none";
      }
    }

    function confirmOnboarding() {
      const inputVal = (document.getElementById("onboarding-input-id").value || "").trim();
      const parsed = parseRDSPlayerId(inputVal);
      AUTH.user.username = parsed.cleanName || "StreetRacer";
      AUTH.user.gameUid = parsed.gameUid || "";
      AUTH.save();
      localStorage.setItem("RDS_ONBOARDED", "true");
      closeAppModal("modal-driver-onboarding");
      enterHubDirectly();
      showToast(`Welcome to RDS Portal, ${AUTH.user.username}!`);
    }

    function enterHubDirectly() {
      document.getElementById("splash-screen").classList.add("hidden-splash");
      document.getElementById("main-hub-screen").classList.add("active-hub");
      AUDIO.init();
      AUDIO.play(659, 0.3);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function returnToSplash() {
      document.getElementById("splash-screen").classList.remove("hidden-splash");
      document.getElementById("main-hub-screen").classList.remove("active-hub");
    }

    function handlePlayerIdInput(val) {
      const parsed = parseRDSPlayerId(val);
      const box = document.getElementById("profile-detected-box");
      const nameEl = document.getElementById("profile-extracted-display");
      if (parsed.gameUid) {
        if (box) box.style.display = "block";
        if (nameEl) nameEl.textContent = parsed.cleanName;
      } else {
        if (box) box.style.display = "none";
      }
    }

    function openDriverProfileModal() {
      const u = AUTH.user;
      // NEVER APPEND HARDCODED UID TO INPUT
      document.getElementById("profile-name-input").value = u.username;
      document.getElementById("profile-avatar-input").value = u.avatar;
      document.getElementById("profile-role-display").textContent = u.roleName;
      handlePlayerIdInput(u.username);
      openAppModal("modal-driver-profile");
    }

    function saveDriverProfile() {
      const rawInput = document.getElementById("profile-name-input").value.trim();
      const parsed = parseRDSPlayerId(rawInput);
      AUTH.user.username = parsed.cleanName || "StreetRacer";
      AUTH.user.gameUid = parsed.gameUid || "";
      AUTH.user.avatar = document.getElementById("profile-avatar-input").value.trim() || AUTH.user.avatar;
      AUTH.save();
      closeAppModal("modal-driver-profile");
      updateHeaderUserUI();
      renderHubView();
      showToast("Driver profile saved!");
    }

    function updateHeaderUserUI() {
      const u = AUTH.user;
      const avatar = document.getElementById("user-pill-avatar-img");
      const name = document.getElementById("user-pill-name-span");
      const role = document.getElementById("user-pill-role-span");
      const settingsUser = document.getElementById("settings-user-display");
      const settingsRole = document.getElementById("settings-role-display");
      const settingsLogout = document.getElementById("settings-logout-row");

      if (avatar) avatar.src = u.avatar;
      if (name) name.textContent = u.username;
      if (role) role.textContent = u.roleName;

      if (settingsUser) settingsUser.textContent = u.username;
      if (settingsRole) settingsRole.textContent = `Role: ${u.roleName}`;
      if (settingsLogout) settingsLogout.style.display = u.isLoggedIn ? "block" : "none";
    }

    /* ==========================================================================
       SETTINGS: THEMES, NAV POSITION, PWA, 10-TAP SECRET STAFF GATE
       ========================================================================== */
    function changeAppTheme(theme) {
      localStorage.setItem("RDS_APP_THEME", theme);
      document.documentElement.setAttribute("data-theme", theme);
      const sel = document.getElementById("setting-theme-select");
      if (sel) sel.value = theme;
      showToast(`Theme switched to ${theme.toUpperCase()}`);
    }

    function changeNavPosition(pos) {
      localStorage.setItem("RDS_NAV_POS", pos);
      applyNavPosition();
    }

    function applyNavPosition() {
      const pos = localStorage.getItem("RDS_NAV_POS") || "auto";
      document.body.classList.remove("nav-pos-bottom", "nav-pos-top");

      if (pos === "bottom") {
        document.body.classList.add("nav-pos-bottom");
      } else if (pos === "top") {
        document.body.classList.add("nav-pos-top");
      }
      const sel = document.getElementById("setting-nav-position");
      if (sel) sel.value = pos;
    }

    function toggleBackgroundMotions(enabled) {
      localStorage.setItem("RDS_MOTION_ENABLED", enabled ? "true" : "false");
      MOTION.enabled = enabled;
      if (enabled) MOTION.start();
      else MOTION.stop();
    }

    function toggleSound(enabled) {
      localStorage.setItem("RDS_SOUND_ENABLED", enabled ? "true" : "false");
      AUDIO.enabled = enabled;
      updateSoundIcon();
    }

    function toggleAudio() {
      const newState = !AUDIO.enabled;
      toggleSound(newState);
      showToast(newState ? "Sound feedback enabled" : "Sound feedback muted");
    }

    function updateSoundIcon() {
      const icon = document.getElementById("icon-sound-state");
      if (icon) {
        icon.className = AUDIO.enabled ? "fa-solid fa-volume-high" : "fa-solid fa-volume-xmark";
      }
      const chk = document.getElementById("setting-sound-toggle");
      if (chk) chk.checked = AUDIO.enabled;
    }

    // PWA Install Handling
    let deferredInstallPrompt = null;
    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredInstallPrompt = e;
      const pwaContainer = document.getElementById("pwa-install-container");
      if (pwaContainer && /Android|iPhone|iPad|iPod|webOS/i.test(navigator.userAgent)) {
        pwaContainer.style.display = "block";
      }
    });

    function handleAddToHomeScreen() {
      const isIos = /iPhone|iPad|iPod/i.test(navigator.userAgent);
      if (isIos) {
        closeAppModal("modal-app-settings");
        openAppModal("modal-ios-install-guide");
        return;
      }

      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        deferredInstallPrompt.userChoice.then(choice => {
          if (choice.outcome === "accepted") {
            showToast("RDS Portal successfully installed!");
          }
          deferredInstallPrompt = null;
        });
      } else {
        showToast("To add to home screen, tap browser options [⋮] and choose 'Install App' or 'Add to Home Screen'.");
      }
    }

    // Secret 10-tap Gate for Staff Login
    let versionTapCount = 0;
    let versionTapTimer = null;

    function handleVersionSecretClick() {
      versionTapCount++;
      clearTimeout(versionTapTimer);
      versionTapTimer = setTimeout(() => {
        versionTapCount = 0;
      }, 3500);

      if (versionTapCount >= 6 && versionTapCount < 10) {
        showToast(`🔒 ${10 - versionTapCount} more taps to unlock Staff Security Gate...`);
      } else if (versionTapCount >= 10) {
        versionTapCount = 0;
        AUDIO.play(987.77, 0.4);
        closeAppModal("modal-app-settings");
        openAppModal("modal-staff-login");
        showToast("🔓 Staff Security Gate Unlocked!");
      }
    }

    function submitStaffLogin() {
      const email = document.getElementById("staff-email-input").value;
      const pass = document.getElementById("staff-pass-input").value;
      const res = AUTH.login(email, pass);
      const errBox = document.getElementById("staff-login-error");

      if (res.success) {
        if (errBox) errBox.style.display = "none";
        closeAppModal("modal-staff-login");
        AUDIO.play(880, 0.5);
        showToast(res.message);
        renderHubView();
        updateHeaderUserUI();
      } else {
        if (errBox) {
          errBox.textContent = res.message;
          errBox.style.display = "block";
        }
        AUDIO.play(300, 0.3);
      }
    }

    /* ==========================================================================
       VEHICLE MANAGEMENT & MODAL OPERATIONS (STAGES 1 TO 7)
       ========================================================================== */
    function openCarModal(carId = null) {
      const car = carId ? STORE.state.cars.find(c => c.id === carId) : null;
      document.getElementById("car-editor-modal-title").textContent = car ? "Edit Vehicle Specs" : "Add New Vehicle";
      document.getElementById("car-edit-id").value = car ? car.id : "";
      document.getElementById("car-name-input").value = car ? car.name : "";
      document.getElementById("car-order-input").value = car ? car.order || 1 : (STORE.state.cars.length + 1);
      document.getElementById("car-image-input").value = car ? car.image : "";

      const statusBox = document.getElementById("status-car-image");
      if (statusBox) {
        if (car && car.image) {
          statusBox.innerHTML = `
            <div class="media-selected-status-badge">
              <i class="fa-solid fa-circle-check"></i> Current Photo Attached:
              <img src="${car.image}" class="media-selected-thumb" alt="Preview">
            </div>
          `;
        } else {
          statusBox.innerHTML = "";
        }
      }

      document.getElementById("car-premium-price-input").value = car ? car.premiumPrice || "10M" : "10M";
      document.getElementById("car-coating-price-input").value = car ? car.coatingPrice || "8M" : "8M";
      document.getElementById("car-police-price-input").value = car ? car.policePrice || "20M" : "20M";
      document.getElementById("car-rainbow-price-input").value = car ? car.rainbowPrice || "15M" : "15M";

      // Populate Stages 1 to 7 Inputs Container
      const stagesContainer = document.getElementById("car-stages-inputs-container");
      if (stagesContainer) {
        stagesContainer.innerHTML = [1, 2, 3, 4, 5, 6, 7].map(s => {
          const st = (car && car.stages && car.stages[s - 1]) ? car.stages[s - 1] : {
            stage: s,
            price: (20 + s * 15) + "M",
            speedNoTurboKmph: 280 + s * 20,
            speedNoTurboMph: Math.round((280 + s * 20) * 0.621371),
            speedTurboKmph: 310 + s * 22,
            speedTurboMph: Math.round((310 + s * 22) * 0.621371)
          };

          return `
            <div style="background: rgba(255,255,255,0.3); border: 1px solid var(--glass-border-subtle); border-radius: var(--radius-sm); padding: 0.75rem;">
              <div style="font-weight: 800; font-size: 0.88rem; color: var(--brand-orange); margin-bottom: 0.5rem;">
                STAGE ${s}
              </div>
              <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">
                <div>
                  <label class="form-field-label" style="font-size: 0.72rem;">Price (k, m, b, t)</label>
                  <input type="text" class="input-box-field" id="st-${s}-price" value="${st.price || (25 * s) + 'M'}" style="padding: 0.4rem 0.6rem; font-size: 0.8rem;">
                </div>
                <div>
                  <label class="form-field-label" style="font-size: 0.72rem;">No Turbo: _kmph / _mph</label>
                  <div style="display: flex; gap: 0.3rem;">
                    <input type="number" class="input-box-field" id="st-${s}-nt-km" value="${st.speedNoTurboKmph || 300}" placeholder="km/h" style="padding: 0.4rem 0.5rem; font-size: 0.8rem;">
                    <input type="number" class="input-box-field" id="st-${s}-nt-mp" value="${st.speedNoTurboMph || 186}" placeholder="mph" style="padding: 0.4rem 0.5rem; font-size: 0.8rem;">
                  </div>
                </div>
                <div>
                  <label class="form-field-label" style="font-size: 0.72rem;">With Turbo: _kmph / _mph</label>
                  <div style="display: flex; gap: 0.3rem;">
                    <input type="number" class="input-box-field" id="st-${s}-tb-km" value="${st.speedTurboKmph || 340}" placeholder="km/h" style="padding: 0.4rem 0.5rem; font-size: 0.8rem;">
                    <input type="number" class="input-box-field" id="st-${s}-tb-mp" value="${st.speedTurboMph || 211}" placeholder="mph" style="padding: 0.4rem 0.5rem; font-size: 0.8rem;">
                  </div>
                </div>
              </div>
            </div>
          `;
        }).join("");
      }

      openAppModal("modal-car-editor");
    }

    function saveCarFromModal() {
      const editId = document.getElementById("car-edit-id").value;
      const name = document.getElementById("car-name-input").value.trim();
      const order = parseInt(document.getElementById("car-order-input").value, 10) || 1;
      const image = document.getElementById("car-image-input").value.trim();
      const premiumPrice = document.getElementById("car-premium-price-input").value.trim() || "10M";
      const coatingPrice = document.getElementById("car-coating-price-input").value.trim() || "8M";
      const policePrice = document.getElementById("car-police-price-input").value.trim() || "20M";
      const rainbowPrice = document.getElementById("car-rainbow-price-input").value.trim() || "15M";

      // Read Stages 1 to 7
      const stages = [1, 2, 3, 4, 5, 6, 7].map(s => {
        const pr = (document.getElementById(`st-${s}-price`).value || (25 * s) + "M").trim();
        const ntKm = parseInt(document.getElementById(`st-${s}-nt-km`).value, 10) || 300;
        const ntMp = parseInt(document.getElementById(`st-${s}-nt-mp`).value, 10) || Math.round(ntKm * 0.621371);
        const tbKm = parseInt(document.getElementById(`st-${s}-tb-km`).value, 10) || 340;
        const tbMp = parseInt(document.getElementById(`st-${s}-tb-mp`).value, 10) || Math.round(tbKm * 0.621371);
        return {
          stage: s,
          price: pr,
          speedNoTurboKmph: ntKm,
          speedNoTurboMph: ntMp,
          speedTurboKmph: tbKm,
          speedTurboMph: tbMp
        };
      });

      if (editId) {
        const existing = STORE.state.cars.find(c => c.id === editId);
        if (existing) {
          Object.assign(existing, { name, order, image, premiumPrice, coatingPrice, policePrice, rainbowPrice, stages });
        }
        STORE.addLog("cars", AUTH.user.username, "Edit Vehicle", `Updated specifications for ${name}.`);
      } else {
        const newCar = {
          id: "car_" + Date.now(),
          name,
          order,
          image,
          description: "High-performance Real Driving School vehicle build.",
          basePrice: stages[0].price || "30M",
          premiumPrice,
          coatingPrice,
          policePrice,
          rainbowPrice,
          stages
        };
        STORE.state.cars.push(newCar);
        STORE.addLog("cars", AUTH.user.username, "Add Vehicle", `Added ${name} to official index.`);
      }

      STORE.syncCollection("cars");
      closeAppModal("modal-car-editor");
      renderHubView();
      showToast(`Vehicle ${name} saved successfully!`);
    }

    function deleteCar(id) {
      if (!confirm("Are you sure you want to delete this vehicle from the official index?")) return;
      const c = STORE.state.cars.find(x => x.id === id);
      STORE.state.cars = STORE.state.cars.filter(x => x.id !== id);
      STORE.addLog("cars", AUTH.user.username, "Delete Vehicle", `Removed ${c ? c.name : id} from catalog.`);
      STORE.syncCollection("cars");
      renderHubView();
      showToast("Vehicle removed from index.");
    }

    function viewCarTechnicalData(carId) {
      const c = STORE.state.cars.find(x => x.id === carId);
      if (!c) return;

      document.getElementById("specs-viewer-car-name").textContent = `${c.name} - Technical Data`;
      const body = document.getElementById("specs-viewer-body");
      if (body) {
        body.innerHTML = `
          <div style="display: flex; gap: 1rem; margin-bottom: 1.25rem; flex-wrap: wrap;">
            <img src="${c.image}" style="width: 220px; height: 130px; object-fit: cover; border-radius: 8px;">
            <div style="flex: 1;">
              <h4 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 0.25rem;">${c.name}</h4>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">${c.description || ''}</p>
              <div style="font-size: 0.82rem;"><strong>Catalog Order:</strong> #${c.order || 1}</div>
            </div>
          </div>

          <h5 style="font-family: var(--font-heading); color: var(--brand-orange); text-transform: uppercase; margin-bottom: 0.5rem;">
            Stage 1 to 7 Performance Matrix
          </h5>
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; text-align: left;">
              <thead>
                <tr style="background: rgba(255,255,255,0.4); border-bottom: 2px solid var(--glass-border-subtle);">
                  <th style="padding: 0.5rem;">Stage</th>
                  <th style="padding: 0.5rem;">Valuation</th>
                  <th style="padding: 0.5rem;">Top Speed (No Turbo)</th>
                  <th style="padding: 0.5rem;">Top Speed (With Turbo)</th>
                </tr>
              </thead>
              <tbody>
                ${(c.stages || []).map(st => `
                  <tr style="border-bottom: 1px solid var(--glass-border-subtle);">
                    <td style="padding: 0.5rem; font-weight: 700;">Stage ${st.stage}</td>
                    <td style="padding: 0.5rem; color: var(--brand-orange); font-weight: 700;">${st.price}</td>
                    <td style="padding: 0.5rem;">${st.speedNoTurboKmph} km/h (${st.speedNoTurboMph} mph)</td>
                    <td style="padding: 0.5rem; font-weight: 700; color: var(--accent-green);">${st.speedTurboKmph} km/h (${st.speedTurboMph} mph)</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        `;
      }
      openAppModal("modal-car-specs-viewer");
    }

    /* ==========================================================================
       TYRE CODES, MAPS, RULES, MULTIPLAYER, ROLES, CATEGORIES CRUD
       ========================================================================== */
    function openTyreModal(tyreId = null) {
      const t = tyreId ? (STORE.state.tyres || []).find(x => x.id === tyreId) : null;
      document.getElementById("tyre-edit-id").value = t ? t.id : "";
      document.getElementById("tyre-name-input").value = t ? t.name : "";
      document.getElementById("tyre-category-input").value = t ? t.category : "Track & Circuit";
      document.getElementById("tyre-code-input").value = t ? t.code : "RDS-GRIP-99X";
      document.getElementById("tyre-friction-input").value = t ? t.frictionIndex : "0.98 Lateral G";
      document.getElementById("tyre-surface-input").value = t ? t.surface : "Asphalt & Dry Track";
      document.getElementById("tyre-description-input").value = t ? t.description : "";
      openAppModal("modal-tyre-editor");
    }

    function saveTyreFromModal() {
      const editId = document.getElementById("tyre-edit-id").value;
      const name = document.getElementById("tyre-name-input").value.trim();
      const category = document.getElementById("tyre-category-input").value.trim();
      const code = document.getElementById("tyre-code-input").value.trim();
      const frictionIndex = document.getElementById("tyre-friction-input").value.trim();
      const surface = document.getElementById("tyre-surface-input").value.trim();
      const description = document.getElementById("tyre-description-input").value.trim();

      if (!STORE.state.tyres) STORE.state.tyres = [];

      if (editId) {
        const existing = STORE.state.tyres.find(x => x.id === editId);
        if (existing) Object.assign(existing, { name, category, code, frictionIndex, surface, description });
        STORE.addLog("tyres", AUTH.user.username, "Edit Tyre", `Updated tyre code ${code}.`);
      } else {
        STORE.state.tyres.push({
          id: "tyre_" + Date.now(),
          name, category, code, frictionIndex, surface, description
        });
        STORE.addLog("tyres", AUTH.user.username, "Add Tyre", `Created tyre compound ${name} (${code}).`);
      }

      STORE.syncCollection("tyres");
      closeAppModal("modal-tyre-editor");
      renderHubView();
      showToast("Tyre code saved successfully!");
    }

    function deleteTyre(id) {
      if (!confirm("Delete this tyre code?")) return;
      STORE.state.tyres = (STORE.state.tyres || []).filter(x => x.id !== id);
      STORE.syncCollection("tyres");
      renderHubView();
      showToast("Tyre code deleted.");
    }

    function openMapModal(mapId = null) {
      const m = mapId ? (STORE.state.maps || []).find(x => x.id === mapId) : null;
      document.getElementById("map-edit-id").value = m ? m.id : "";
      document.getElementById("map-title-input").value = m ? m.title : "";
      document.getElementById("map-tag-input").value = m ? m.tag : "Drift Zone";
      document.getElementById("map-image-input").value = m ? m.image : "";
      document.getElementById("map-description-input").value = m ? m.description : "";
      openAppModal("modal-map-editor");
    }

    function saveMapFromModal() {
      const editId = document.getElementById("map-edit-id").value;
      const title = document.getElementById("map-title-input").value.trim();
      const tag = document.getElementById("map-tag-input").value.trim();
      const image = document.getElementById("map-image-input").value.trim();
      const description = document.getElementById("map-description-input").value.trim();

      if (!STORE.state.maps) STORE.state.maps = [];
      if (editId) {
        const existing = STORE.state.maps.find(x => x.id === editId);
        if (existing) Object.assign(existing, { title, tag, image, description });
      } else {
        STORE.state.maps.push({ id: "map_" + Date.now(), title, tag, image, description });
      }

      STORE.syncCollection("maps");
      closeAppModal("modal-map-editor");
      renderHubView();
      showToast("Map location saved!");
    }

    function deleteMap(id) {
      if (!confirm("Delete this map location?")) return;
      STORE.state.maps = (STORE.state.maps || []).filter(x => x.id !== id);
      STORE.syncCollection("maps");
      renderHubView();
      showToast("Location removed.");
    }

    function openRuleModal(ruleId = null) {
      const r = ruleId ? (STORE.state.rules || []).find(x => x.id === ruleId) : null;
      document.getElementById("rule-edit-id").value = r ? r.id : "";
      document.getElementById("rule-title-input").value = r ? r.title : "";
      document.getElementById("rule-content-input").value = r ? r.content : "";
      openAppModal("modal-rule-editor");
    }

    function saveRuleFromModal() {
      const editId = document.getElementById("rule-edit-id").value;
      const title = document.getElementById("rule-title-input").value.trim();
      const content = document.getElementById("rule-content-input").value.trim();

      if (!STORE.state.rules) STORE.state.rules = [];
      if (editId) {
        const existing = STORE.state.rules.find(x => x.id === editId);
        if (existing) Object.assign(existing, { title, content });
      } else {
        STORE.state.rules.push({ id: "rule_" + Date.now(), title, content });
      }

      STORE.syncCollection("rules");
      closeAppModal("modal-rule-editor");
      renderHubView();
      showToast("Conduct rule saved!");
    }

    function deleteRule(id) {
      if (!confirm("Delete this rule?")) return;
      STORE.state.rules = (STORE.state.rules || []).filter(x => x.id !== id);
      STORE.syncCollection("rules");
      renderHubView();
      showToast("Rule removed.");
    }

    function openMpModal(mpId = null) {
      const m = mpId ? (STORE.state.multiplayerGuides || []).find(x => x.id === mpId) : null;
      document.getElementById("mp-edit-id").value = m ? m.id : "";
      document.getElementById("mp-title-input").value = m ? m.title : "";
      document.getElementById("mp-content-input").value = m ? m.content : "";
      openAppModal("modal-multiplayer-editor");
    }

    function saveMpFromModal() {
      const editId = document.getElementById("mp-edit-id").value;
      const title = document.getElementById("mp-title-input").value.trim();
      const content = document.getElementById("mp-content-input").value.trim();

      if (!STORE.state.multiplayerGuides) STORE.state.multiplayerGuides = [];
      if (editId) {
        const existing = STORE.state.multiplayerGuides.find(x => x.id === editId);
        if (existing) Object.assign(existing, { title, content });
      } else {
        STORE.state.multiplayerGuides.push({ id: "mp_" + Date.now(), title, content });
      }

      STORE.syncCollection("multiplayer");
      closeAppModal("modal-multiplayer-editor");
      renderHubView();
      showToast("Clan guide saved!");
    }

    function deleteMp(id) {
      if (!confirm("Delete this multiplayer guide?")) return;
      STORE.state.multiplayerGuides = (STORE.state.multiplayerGuides || []).filter(x => x.id !== id);
      STORE.syncCollection("multiplayer");
      renderHubView();
      showToast("Guide removed.");
    }

    function openRoleModal(roleId = null) {
      const r = roleId ? (STORE.state.roles || []).find(x => x.id === roleId) : null;
      document.getElementById("role-edit-id").value = r ? r.id : "";
      document.getElementById("role-name-input").value = r ? r.name : "";
      document.getElementById("role-color-input").value = r ? r.color : "#ff6b00";
      openAppModal("modal-role-editor");
    }

    function saveRoleFromModal() {
      const editId = document.getElementById("role-edit-id").value;
      const name = document.getElementById("role-name-input").value.trim();
      const color = document.getElementById("role-color-input").value;
      const perms = [];
      if (document.getElementById("role-perm-cars").checked) perms.push("cars");
      if (document.getElementById("role-perm-events").checked) perms.push("events");
      if (document.getElementById("role-perm-updates").checked) perms.push("updates");
      if (document.getElementById("role-perm-tyres").checked) perms.push("tyres");

      if (!STORE.state.roles) STORE.state.roles = [];
      if (editId) {
        const existing = STORE.state.roles.find(x => x.id === editId);
        if (existing) Object.assign(existing, { name, color, perms });
      } else {
        STORE.state.roles.push({ id: "role_" + Date.now(), name, color, perms });
      }

      STORE.syncCollection("roles");
      closeAppModal("modal-role-editor");
      renderHubView();
      showToast("Role saved!");
    }

    function deleteRole(id) {
      if (!confirm("Delete this role?")) return;
      STORE.state.roles = (STORE.state.roles || []).filter(x => x.id !== id);
      STORE.syncCollection("roles");
      renderHubView();
      showToast("Role deleted.");
    }

    function openCategoryModal(catId = null) {
      const c = catId ? (STORE.state.customCategories || []).find(x => x.id === catId) : null;
      document.getElementById("category-edit-id").value = c ? c.id : "";
      document.getElementById("category-title-input").value = c ? c.title : "";
      document.getElementById("category-icon-input").value = c ? c.icon : "fa-solid fa-star";
      document.getElementById("category-content-input").value = c ? c.content : "";
      openAppModal("modal-category-editor");
    }

    function saveCategoryFromModal() {
      const editId = document.getElementById("category-edit-id").value;
      const title = document.getElementById("category-title-input").value.trim();
      const icon = document.getElementById("category-icon-input").value.trim() || "fa-solid fa-star";
      const content = document.getElementById("category-content-input").value.trim();

      if (!STORE.state.customCategories) STORE.state.customCategories = [];
      if (editId) {
        const existing = STORE.state.customCategories.find(x => x.id === editId);
        if (existing) Object.assign(existing, { title, icon, content });
      } else {
        const newCat = { id: "cat_" + Date.now(), title, icon, content };
        STORE.state.customCategories.push(newCat);
      }

      STORE.syncCollection("custom_cats");
      rebuildCustomCategoryNav();
      closeAppModal("modal-category-editor");
      renderHubView();
      showToast("Category added to portal navigation!");
    }

    function deleteCategory(id) {
      if (!confirm("Delete this category?")) return;
      STORE.state.customCategories = (STORE.state.customCategories || []).filter(x => x.id !== id);
      STORE.syncCollection("custom_cats");
      rebuildCustomCategoryNav();
      renderHubView();
      showToast("Category deleted.");
    }

    function rebuildCustomCategoryNav() {
      const dock = document.getElementById("hub-main-category-dock");
      if (!dock) return;

      // Remove existing custom buttons
      dock.querySelectorAll(".custom-nav-btn").forEach(b => b.remove());

      const cats = STORE.state.customCategories || [];
      const ownerBtn = document.getElementById("nav-owner-tab");

      cats.forEach(c => {
        const btn = document.createElement("button");
        btn.className = "hub-nav-btn custom-nav-btn";
        btn.setAttribute("data-view", `custom_${c.id}`);
        btn.innerHTML = `<i class="${c.icon || 'fa-solid fa-star'}"></i> ${c.title}`;
        btn.onclick = () => switchHubView(`custom_${c.id}`);
        if (ownerBtn) dock.insertBefore(btn, ownerBtn);
        else dock.appendChild(btn);
      });
    }

    /* ==========================================================================
       UPDATES, EVENTS, ADMINS & UI BRANDING OPERATIONS
       ========================================================================== */
    function saveUpdateFromModal() {
      const version = document.getElementById("update-version-input").value.trim();
      const channel = document.getElementById("update-channel-select").value;
      const title = document.getElementById("update-title-input").value.trim();
      const image = document.getElementById("update-image-input").value.trim();
      const notesRaw = document.getElementById("update-notes-input").value.trim();
      const notes = notesRaw.split("\n").map(s => s.trim().replace(/^[-*•]\s*/, "")).filter(Boolean);
      const publishedAndroid = document.getElementById("update-android-check").checked;
      const publishedIos = document.getElementById("update-ios-check").checked;

      const newUpd = {
        id: "upd_" + Date.now(),
        version,
        channel,
        title,
        image,
        notes,
        publishedAndroid,
        publishedIos,
        author: AUTH.user.username,
        timestamp: new Date().toISOString()
      };

      if (!STORE.state.updates) STORE.state.updates = [];
      STORE.state.updates.unshift(newUpd);
      STORE.addLog("updates", AUTH.user.username, "Publish Update", `Announced ${version} (${channel}).`);
      STORE.syncCollection("updates");

      closeAppModal("modal-update-editor");
      renderHubView();
      showToast(`Update ${version} published to everyone!`);
    }

    function deleteUpdate(id) {
      if (!confirm("Delete this update announcement?")) return;
      STORE.state.updates = STORE.state.updates.filter(u => u.id !== id);
      STORE.syncCollection("updates");
      renderHubView();
      showToast("Update removed.");
    }

    function saveEventFromModal() {
      const title = document.getElementById("event-title-input").value.trim();
      const image = document.getElementById("event-image-input").value.trim();
      const startTime = document.getElementById("event-start-input").value;
      const endTime = document.getElementById("event-end-input").value;
      const prizes = document.getElementById("event-prize-input").value.trim();
      const isLive = document.getElementById("event-is-live-check").checked;

      const newEv = {
        id: "ev_" + Date.now(),
        title,
        image,
        startTime,
        endTime,
        prizes,
        isLive,
        location: "RDS Open World Arena",
        description: "Official competitive event organized by RDS staff."
      };

      if (!STORE.state.events) STORE.state.events = [];
      STORE.state.events.unshift(newEv);
      STORE.addLog("events", AUTH.user.username, "Create Event", `Created event ${title}.`);
      STORE.syncCollection("events");

      closeAppModal("modal-event-editor");
      renderHubView();
      showToast("Event published!");
    }

    function deleteEvent(id) {
      if (!confirm("Delete this event?")) return;
      STORE.state.events = STORE.state.events.filter(e => e.id !== id);
      STORE.syncCollection("events");
      renderHubView();
      showToast("Event removed.");
    }

    function saveAdminFromModal() {
      const name = document.getElementById("admin-name-input").value.trim();
      const email = document.getElementById("admin-email-input").value.trim().toLowerCase();
      const password = document.getElementById("admin-pass-input").value.trim();
      const deviceLimit = parseInt(document.getElementById("admin-device-limit-select").value, 10) || 2;

      const perms = [];
      if (document.getElementById("perm-cars").checked) perms.push("cars");
      if (document.getElementById("perm-events").checked) perms.push("events");
      if (document.getElementById("perm-updates").checked) perms.push("updates");
      if (document.getElementById("perm-tyres").checked) perms.push("tyres");
      if (document.getElementById("perm-maps").checked) perms.push("maps");
      if (document.getElementById("perm-rules").checked) perms.push("rules");

      const newAdmin = {
        id: "adm_" + Date.now(),
        name,
        email,
        password,
        deviceLimit,
        activeLogins: 0,
        permissions: perms,
        roleName: "Staff Admin"
      };

      if (!STORE.state.admins) STORE.state.admins = [];
      STORE.state.admins.push(newAdmin);
      STORE.addLog("security", AUTH.user.username, "Create Admin", `Created administrator ${name} (${email}).`);
      STORE.syncCollection("admins");

      closeAppModal("modal-admin-editor");
      renderHubView();
      showToast(`Administrator ${name} created!`);
    }

    function deleteAdmin(id) {
      if (!confirm("Revoke admin credentials for this user?")) return;
      STORE.state.admins = STORE.state.admins.filter(a => a.id !== id);
      STORE.syncCollection("admins");
      renderHubView();
      showToast("Admin revoked.");
    }

    function saveUiCustomization() {
      const title = document.getElementById("ui-game-name-input").value.trim();
      const logo = document.getElementById("ui-logo-input").value.trim();
      const about = document.getElementById("ui-about-input").value.trim();
      const bgType = document.getElementById("ui-bg-type-select").value;
      const bgMediaUrl = document.getElementById("ui-bg-media-input").value.trim();
      const discordUrl = document.getElementById("ui-discord-input").value.trim();
      const instagramUrl = document.getElementById("ui-instagram-input").value.trim();
      const googlePlayUrl = document.getElementById("ui-googleplay-input").value.trim();
      const appStoreUrl = document.getElementById("ui-appstore-input").value.trim();

      Object.assign(STORE.state.hubConfig, {
        title, logo, about, bgType, bgMediaUrl, discordUrl, instagramUrl, googlePlayUrl, appStoreUrl
      });

      STORE.syncCollection("config");
      applyHubConfigToUI();
      closeAppModal("modal-ui-editor");
      showToast("Portal branding updated and synchronized!");
    }

    function applyHubConfigToUI() {
      const cfg = STORE.state.hubConfig || {};
      
      // Update Title & About
      if (cfg.title) {
        const splashTitle = document.getElementById("splash-main-title");
        const headerTitle = document.getElementById("header-brand-title");
        if (splashTitle) splashTitle.textContent = cfg.title;
        if (headerTitle) headerTitle.textContent = cfg.title;
      }
      if (cfg.logo) {
        const splashLogo = document.getElementById("splash-main-logo");
        const headerLogo = document.getElementById("header-brand-logo");
        if (splashLogo) splashLogo.src = cfg.logo;
        if (headerLogo) headerLogo.src = cfg.logo;
      }
      if (cfg.about) {
        const splashAbout = document.getElementById("splash-main-about");
        if (splashAbout) splashAbout.textContent = cfg.about;
      }

      // Social Links
      if (cfg.discordUrl) {
        const el = document.getElementById("link-splash-discord");
        if (el) el.href = cfg.discordUrl;
      }
      if (cfg.instagramUrl) {
        const el = document.getElementById("link-splash-instagram");
        if (el) el.href = cfg.instagramUrl;
      }
      if (cfg.googlePlayUrl) {
        const el = document.getElementById("link-splash-googleplay");
        if (el) el.href = cfg.googlePlayUrl;
      }
      if (cfg.appStoreUrl) {
        const el = document.getElementById("link-splash-appstore");
        if (el) el.href = cfg.appStoreUrl;
      }

      // Background Media Toggle: Video vs Image (Crucial fix: hides video when image is selected!)
      const videoEl = document.getElementById("bg-video-main");
      const videoSrc = document.getElementById("bg-video-src");
      const imageEl = document.getElementById("bg-image-fallback");

      if (cfg.bgType === "image" && cfg.bgMediaUrl) {
        if (videoEl) videoEl.style.display = "none";
        if (imageEl) {
          imageEl.src = cfg.bgMediaUrl;
          imageEl.style.display = "block";
        }
      } else {
        if (imageEl) imageEl.style.display = "none";
        if (videoEl) {
          if (videoSrc && cfg.bgMediaUrl && videoSrc.src !== cfg.bgMediaUrl) {
            videoSrc.src = cfg.bgMediaUrl;
            videoEl.load();
          }
          videoEl.style.display = "block";
        }
      }
    }

    /* ==========================================================================
       BOOTSTRAP & EVENT LISTENERS
       ========================================================================== */
    window.addEventListener("DOMContentLoaded", () => {
      // 1. Restore Theme
      const savedTheme = localStorage.getItem("RDS_APP_THEME") || "frost";
      changeAppTheme(savedTheme);

      // 2. Restore Nav Position
      applyNavPosition();

      // 3. Mouse Wheel horizontal scrolling for Category Dock
      const catBar = document.getElementById("hub-main-category-dock");
      if (catBar) {
        catBar.addEventListener("wheel", (e) => {
          if (e.deltaY !== 0) {
            e.preventDefault();
            catBar.scrollLeft += e.deltaY;
          }
        }, { passive: false });
      }

      // 4. Rebuild Custom Categories
      rebuildCustomCategoryNav();

      // 5. Apply UI Config
      applyHubConfigToUI();

      // 6. Initialize Motion Canvas Engine
      MOTION.init();

      // 7. Update Sound State
      updateSoundIcon();

      // 8. Update User Header UI
      updateHeaderUserUI();

      // 9. Render Initial View
      renderHubView();

      // 10. Check Mobile for PWA Install container
      if (/Android|iPhone|iPad|iPod|webOS/i.test(navigator.userAgent)) {
        const pwaBox = document.getElementById("pwa-install-container");
        if (pwaBox) pwaBox.style.display = "block";
      }

      // 11. Pre-fill UI editor inputs if owner
      const uiGameName = document.getElementById("ui-game-name-input");
      if (uiGameName && STORE.state.hubConfig) {
        uiGameName.value = STORE.state.hubConfig.title || "REAL DRIVING SCHOOL";
        document.getElementById("ui-logo-input").value = STORE.state.hubConfig.logo || "";
        document.getElementById("ui-about-input").value = STORE.state.hubConfig.about || "";
        document.getElementById("ui-bg-type-select").value = STORE.state.hubConfig.bgType || "video";
        document.getElementById("ui-bg-media-input").value = STORE.state.hubConfig.bgMediaUrl || "";
        document.getElementById("ui-discord-input").value = STORE.state.hubConfig.discordUrl || "";
        document.getElementById("ui-instagram-input").value = STORE.state.hubConfig.instagramUrl || "";
        document.getElementById("ui-googleplay-input").value = STORE.state.hubConfig.googlePlayUrl || "";
        document.getElementById("ui-appstore-input").value = STORE.state.hubConfig.appStoreUrl || "";
      }
    });
  </script>
</body>
</html>
'''
