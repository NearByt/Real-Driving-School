# part_js_init.py - Modals, CRUD, Handlers & Bootstrap for Real Driving School Portal v1.2.120
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
          border: 1px solid rgba(255,255,255,0.15);
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
        pill.style.borderColor = "rgba(22, 163, 74, 0.4)";
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
      const ownerTab = document.getElementById("nav-owner-tab");
      const settingsUser = document.getElementById("settings-user-display");
      const settingsRole = document.getElementById("settings-role-display");
      const settingsLogout = document.getElementById("settings-logout-row");

      if (avatar) avatar.src = u.avatar;
      if (name) name.textContent = u.username;
      if (role) role.textContent = u.roleName;

      if (settingsUser) settingsUser.textContent = u.username;
      if (settingsRole) settingsRole.textContent = `Role: ${u.roleName}`;
      if (settingsLogout) settingsLogout.style.display = u.isLoggedIn ? "block" : "none";

      if (ownerTab) {
        ownerTab.style.display = (u.isOwner || (u.permissions && u.permissions.length > 0)) ? "inline-flex" : "none";
      }
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
      const dock = document.getElementById("hub-main-category-dock");

      if (pos === "bottom") {
        document.body.classList.add("nav-pos-bottom");
        if (dock) {
          dock.classList.remove("nav-dock-top");
          dock.classList.add("nav-dock-bottom");
        }
      } else if (pos === "top") {
        document.body.classList.add("nav-pos-top");
        if (dock) {
          dock.classList.remove("nav-dock-bottom");
          dock.classList.add("nav-dock-top");
        }
      } else {
        // Auto: Top on PC, Bottom Dock on mobile (handled by media query)
        if (dock) {
          dock.classList.remove("nav-dock-bottom");
          dock.classList.add("nav-dock-top");
        }
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
      
      const prevImg = document.getElementById("preview-car-editor-img");
      if (prevImg) {
        if (car && car.image) {
          prevImg.src = car.image;
          prevImg.style.display = "block";
        } else {
          prevImg.style.display = "none";
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
            <div style="background: var(--bg-base); border: 1px solid var(--glass-border-subtle); border-radius: var(--radius-sm); padding: 0.75rem;">
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
                <tr style="background: var(--bg-base); border-bottom: 2px solid var(--glass-border-subtle);">
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

    function toggleUiBgTypeInputs(val) {
      // Toggle inputs if necessary
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

      // 4. Apply UI Config
      applyHubConfigToUI();

      // 5. Initialize Motion Canvas Engine
      MOTION.init();

      // 6. Update Sound State
      updateSoundIcon();

      // 7. Update User Header UI
      updateHeaderUserUI();

      // 8. Render Initial View
      renderHubView();

      // 9. Check Mobile for PWA Install container
      if (/Android|iPhone|iPad|iPod|webOS/i.test(navigator.userAgent)) {
        const pwaBox = document.getElementById("pwa-install-container");
        if (pwaBox) pwaBox.style.display = "block";
      }

      // 10. Pre-fill UI editor inputs if owner
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
