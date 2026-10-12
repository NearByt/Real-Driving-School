# part_js_views.py - View Renderers, Calculator (Without package, ceramic, edition) & Full Owner Panel
import sys
sys.stdout.reconfigure(encoding='utf-8')

JS_VIEWS_CONTENT = r'''
    /* ==========================================================================
       VIEW ROUTING & RENDERING LOGIC
       ========================================================================== */
    let currentHubView = "car-prices";
    let currentAdminSubtab = "admins";
    let calcActiveCarId = null;
    let calcSelectedStage = 1;
    let calcCustomStage = null;
    let calcHasRainbow = false;
    let calcHasPolice = false;
    let calcHasCoating = false;
    let calcHasPremium = false;
    let calcHasCustomLivery = false;
    let calcCustomLiveryPrice = "5M";
    let carCatalogSearchQuery = "";
    let currentUpdatesChannel = "public";

    function switchHubView(viewName) {
      currentHubView = viewName;
      document.querySelectorAll(".hub-nav-btn").forEach(btn => {
        btn.classList.toggle("active", btn.getAttribute("data-view") === viewName);
      });
      renderHubView();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    function scrollNavDock(amount) {
      const catBar = document.getElementById("hub-main-category-dock");
      if (catBar) {
        catBar.scrollBy({ left: amount, behavior: "smooth" });
      }
    }

    function renderHubView() {
      const container = document.getElementById("hub-main-content");
      if (!container) return;

      if (currentHubView === "car-prices") renderCarPrices(container);
      else if (currentHubView === "tyre-codes") renderTyreCodes(container);
      else if (currentHubView === "events") renderEvents(container);
      else if (currentHubView === "updates") renderUpdates(container);
      else if (currentHubView === "maps") renderMaps(container);
      else if (currentHubView === "multiplayer") renderMultiplayer(container);
      else if (currentHubView === "rules") renderRules(container);
      else if (currentHubView === "grinders") renderGrinders(container);
      else if (currentHubView === "owner") renderOwnerPanel(container);
      else if (currentHubView.startsWith("custom_")) {
        const catId = currentHubView.replace("custom_", "");
        renderCustomCategoryView(container, catId);
      }
    }

    /* ==========================================================================
       1. CAR PRICES & VALUE CALCULATOR
       Add-on names strictly: Rainbow Smoke, Police, Coating, Premium, Custom Livery
       (Words package, ceramic, edition REMOVED)
       ========================================================================== */
    function filterCarCatalog(val) {
      carCatalogSearchQuery = (val || "").trim().toLowerCase();
      renderHubView();
    }

    function jumpToCalculator() {
      const calcEl = document.getElementById("car-calculator-section");
      if (calcEl) calcEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function renderCarPrices(container) {
      const allCars = (STORE.state.cars || []).slice().sort((a,b) => (a.order || 99) - (b.order || 99));
      
      const filteredCars = allCars.filter(c => {
        if (!carCatalogSearchQuery) return true;
        const nameMatch = (c.name || "").toLowerCase().includes(carCatalogSearchQuery);
        const orderMatch = ("#" + (c.order || "")).includes(carCatalogSearchQuery);
        return nameMatch || orderMatch;
      });

      if (!calcActiveCarId && allCars.length > 0) {
        calcActiveCarId = allCars[0].id;
      }
      const activeCar = allCars.find(c => c.id === calcActiveCarId) || allCars[0];

      const canEdit = AUTH.hasPerm("cars") || STORE.state.isEditingMode;

      // Calculate bill price
      const billData = calculateCarBill(activeCar);

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">🚗 Car Prices & Value Calculator</h2>
            <p class="view-subtitle-main">Official valuation index, stage speed metrics (km/h & mph), and customizable bill invoice generator.</p>
          </div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button class="btn-brand-secondary" onclick="jumpToCalculator()"><i class="fa-solid fa-calculator"></i> Jump to Calculator</button>
            ${canEdit ? `<button class="btn-brand-primary" onclick="openCarModal(null)"><i class="fa-solid fa-plus"></i> Add New Car</button>` : ""}
          </div>
        </div>

        <!-- Vehicle Catalog Header with Live Search -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1rem;">
          <h3 style="font-family: var(--font-heading); text-transform: uppercase; color: var(--brand-orange); font-size: 1.25rem;">
            <i class="fa-solid fa-car-side"></i> Vehicle Catalog (Designated Order)
          </h3>
          <div style="min-width: 260px; flex: 1; max-width: 380px;">
            <input type="text" class="input-box-field" placeholder="🔍 Search car by name or #order..." value="${carCatalogSearchQuery}" oninput="filterCarCatalog(this.value)" style="padding: 0.5rem 0.85rem; font-size: 0.85rem;">
          </div>
        </div>

        <!-- Catalog Grid (At least 2 side by side on mobile) -->
        <div class="cars-grid-catalog">
          ${filteredCars.map(c => `
            <div class="car-display-card">
              <div class="car-photo-box" onclick="openPhotoViewer('${c.image}', '${c.name}')">
                <img src="${c.image}" alt="${c.name}" class="car-photo-img" onerror="this.src='https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=600&q=80'">
                <span class="car-order-pill">#${c.order || 1}</span>
              </div>
              <div class="car-card-body">
                <h4 class="car-title-heading">${c.name}</h4>
                <div class="car-quick-specs">
                  <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-dim);">Base Value:</span> <strong>${c.basePrice || '30M'}</strong></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-dim);">Stage 1 Top:</span> <strong>${c.stages && c.stages[0] ? c.stages[0].speedTurboKmph : 340} km/h</strong></div>
                  <div style="display: flex; justify-content: space-between;"><span style="color: var(--text-dim);">Stage 7 Top:</span> <strong style="color: var(--accent-green);">${c.stages && c.stages[6] ? c.stages[6].speedTurboKmph : 495} km/h</strong></div>
                </div>
                <div style="display: flex; gap: 0.4rem; margin-top: auto;">
                  <button class="btn-brand-primary" style="flex: 1; padding: 0.45rem; font-size: 0.78rem;" onclick="selectCarForCalc('${c.id}')">Select in Calc</button>
                  <button class="btn-brand-secondary" style="padding: 0.45rem 0.6rem; font-size: 0.78rem;" onclick="viewCarTechnicalData('${c.id}')"><i class="fa-solid fa-circle-info"></i> Specs</button>
                  ${canEdit ? `
                    <button class="btn-brand-secondary" style="padding: 0.45rem;" onclick="openCarModal('${c.id}')"><i class="fa-solid fa-pen"></i></button>
                    <button class="btn-brand-danger" style="padding: 0.45rem;" onclick="deleteCar('${c.id}')"><i class="fa-solid fa-trash"></i></button>
                  ` : ""}
                </div>
              </div>
            </div>
          `).join("")}
        </div>

        <!-- CALCULATOR & LUXURY INVOICE (No print/share buttons) -->
        <div class="calculator-two-col" id="car-calculator-section">
          <div class="liquid-glass" style="padding: 1.75rem;">
            <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange); margin-bottom: 1rem;">
              <i class="fa-solid fa-calculator"></i> Price & Specs Customizer
            </h3>

            <!-- Active Vehicle Dropdown -->
            <div class="form-group-item">
              <label class="form-field-label">Active Vehicle</label>
              <select class="select-box-field" onchange="selectCarForCalc(this.value)">
                ${allCars.map(c => `<option value="${c.id}" ${activeCar && activeCar.id === c.id ? 'selected' : ''}>#${c.order || 1} - ${c.name}</option>`).join("")}
              </select>
            </div>

            <!-- Stage 1-7 Selection Chips -->
            <div class="form-group-item">
              <label class="form-field-label">Tuning Stage (Stage 1 to 7 or Custom Stage)</label>
              <div class="stage-chips-wrap">
                ${[1, 2, 3, 4, 5, 6, 7].map(s => `
                  <div class="stage-choice-chip ${!calcCustomStage && calcSelectedStage === s ? 'active' : ''}" onclick="pickStage(${s})">Stage ${s}</div>
                `).join("")}
              </div>

              <!-- Custom Stage Input (> 7) -->
              <div style="margin-top: 0.65rem; background: rgba(255, 255, 255, 0.25); padding: 0.65rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
                <label class="form-field-label" style="font-size: 0.75rem;">Enter Custom Stage (> Stage 7 - Extrapolates Dynamic Value)</label>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem;">
                  <input type="number" min="1" max="50" class="input-box-field" placeholder="e.g. 8, 10, 15" value="${calcCustomStage || ''}" oninput="onCustomStageInput(this.value)" style="padding: 0.45rem 0.75rem;">
                  <button type="button" class="btn-brand-secondary" onclick="clearCustomStage()" style="padding: 0.45rem 0.75rem; font-size: 0.78rem;">Reset</button>
                </div>
              </div>
              ${calcCustomStage && calcCustomStage > 7 ? `
                <div style="margin-top: 0.4rem; font-size: 0.75rem; color: #d97706; font-weight: 700;">
                  ⚠️ Note: Stage ${calcCustomStage} is an approximate valuation based on exponential stage scaling.
                </div>
              ` : ''}
            </div>

            <!-- The 4 Add-ons + Custom Livery (Strictly without package, ceramic, edition) -->
            <div class="form-group-item">
              <label class="form-field-label">Vehicle Add-ons & Packages</label>
              <div style="display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.35rem;">
                <!-- 1. Rainbow Smoke -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.3); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 700;">🌈 Rainbow Smoke (${activeCar ? activeCar.rainbowPrice || '15M' : '15M'})</span>
                  <input type="checkbox" ${calcHasRainbow ? 'checked' : ''} onchange="calcHasRainbow = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 2. Police (Package removed) -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.3); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 700;">🚓 Police (${activeCar ? activeCar.policePrice || '20M' : '20M'})</span>
                  <input type="checkbox" ${calcHasPolice ? 'checked' : ''} onchange="calcHasPolice = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 3. Coating (Ceramic removed) -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.3); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 700;">🛡️ Coating (${activeCar ? activeCar.coatingPrice || '8M' : '8M'})</span>
                  <input type="checkbox" ${calcHasCoating ? 'checked' : ''} onchange="calcHasCoating = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 4. Premium (Edition removed) -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.3); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 700;">⭐ Premium (${activeCar ? activeCar.premiumPrice || '10M' : '10M'})</span>
                  <input type="checkbox" ${calcHasPremium ? 'checked' : ''} onchange="calcHasPremium = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 5. Custom Livery (Asks for price if yes) -->
                <div style="background: rgba(255, 255, 255, 0.3); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.88rem; font-weight: 700;">🎨 Custom Livery</span>
                    <input type="checkbox" ${calcHasCustomLivery ? 'checked' : ''} onchange="calcHasCustomLivery = this.checked; renderHubView();" style="transform: scale(1.3);">
                  </div>
                  ${calcHasCustomLivery ? `
                    <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                      <span style="font-size: 0.78rem; color: var(--text-muted); font-weight: 600;">Livery Custom Price:</span>
                      <input type="text" class="input-box-field" value="${calcCustomLiveryPrice}" oninput="calcCustomLiveryPrice = this.value; renderHubView();" style="padding: 0.35rem 0.6rem; font-size: 0.82rem; width: 90px;" placeholder="e.g. 5M">
                    </div>
                  ` : ''}
                </div>
              </div>
            </div>
          </div>

          <!-- LUXURY BILL RECEIPT BREAKDOWN (NO PRINT OR SHARE BUTTONS) -->
          <div class="luxury-receipt-container">
            <div class="receipt-header-row">
              <div>
                <div style="font-family: var(--font-heading); font-size: 1.25rem; font-weight: 800; color: var(--brand-orange);">RDS OFFICIAL INVOICE</div>
                <div style="font-size: 0.75rem; color: var(--text-dim);">Real Driving School Valuation System</div>
              </div>
              <div style="text-align: right;">
                <div style="font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;">#${activeCar ? activeCar.order || 1 : 1}</div>
                <div style="font-size: 0.72rem; color: var(--accent-green); font-weight: 700;">CERTIFIED</div>
              </div>
            </div>

            <div style="margin-bottom: 1rem;">
              <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.2rem;">${activeCar ? activeCar.name : 'Vehicle'}</h4>
              <div style="font-size: 0.82rem; color: var(--text-muted); font-weight: 600;">${billData.stageTitle}</div>
            </div>

            <!-- Technical Performance Metrics -->
            <div style="background: rgba(255, 255, 255, 0.28); border: 1px solid var(--glass-border-subtle); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-size: 0.8rem; display: flex; flex-direction: column; gap: 0.25rem;">
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-dim);">Top Speed (No Turbo):</span>
                <strong>${billData.speedNoTurboKmph} km/h (${billData.speedNoTurboMph} mph)</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-dim);">Top Speed (With Turbo):</span>
                <strong style="color: var(--brand-orange);">${billData.speedTurboKmph} km/h (${billData.speedTurboMph} mph)</strong>
              </div>
            </div>

            <!-- Itemized Pricing Breakdown (Without package, ceramic, edition) -->
            <div style="display: flex; flex-direction: column; gap: 0.35rem; border-top: 1px dashed var(--glass-border-subtle); padding-top: 0.75rem;">
              <div class="receipt-item-row">
                <span style="color: var(--text-muted);">${billData.stageTitle} Base:</span>
                <strong>$${formatNumberAbbr(billData.stagePriceNum)}</strong>
              </div>
              ${billData.items.map(item => `
                <div class="receipt-item-row">
                  <span style="color: var(--text-muted);">${item.label}:</span>
                  <strong>+$${formatNumberAbbr(item.priceNum)}</strong>
                </div>
              `).join("")}
            </div>

            <!-- Total Valuation Approximate Range -->
            <div class="receipt-total-box">
              <div>
                <div style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--text-dim);">Valuation Range</div>
                <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">${billData.isApprox ? 'Approximate Estimate' : 'Calculated Value'}</div>
              </div>
              <div class="receipt-total-range">
                $${formatNumberAbbr(billData.minTotal)} - $${formatNumberAbbr(billData.maxTotal)}
              </div>
            </div>
            <div style="text-align: right; font-size: 0.75rem; color: var(--text-dim); margin-top: 0.25rem;">
              ($${billData.minTotal.toLocaleString()} - $${billData.maxTotal.toLocaleString()})
            </div>
          </div>
        </div>
      `;
    }

    function calculateCarBill(car) {
      if (!car) {
        return {
          stageTitle: "Stage 1",
          stagePriceNum: 30000000,
          speedNoTurboKmph: 300,
          speedNoTurboMph: 186,
          speedTurboKmph: 340,
          speedTurboMph: 211,
          items: [],
          minTotal: 30000000,
          maxTotal: 35000000,
          isApprox: false
        };
      }

      let stageNum = calcCustomStage ? parseInt(calcCustomStage, 10) : calcSelectedStage;
      if (isNaN(stageNum) || stageNum < 1) stageNum = 1;

      let stagePriceNum = 0;
      let speedNoTurboKmph = 300;
      let speedNoTurboMph = 186;
      let speedTurboKmph = 340;
      let speedTurboMph = 211;
      let isApprox = false;

      const stages = car.stages || [];
      if (stageNum <= 7 && stages[stageNum - 1]) {
        const st = stages[stageNum - 1];
        stagePriceNum = parseValueToNumber(st.price || car.basePrice || "30M");
        speedNoTurboKmph = st.speedNoTurboKmph || 320;
        speedNoTurboMph = st.speedNoTurboMph || Math.round(speedNoTurboKmph * 0.621371);
        speedTurboKmph = st.speedTurboKmph || 350;
        speedTurboMph = st.speedTurboMph || Math.round(speedTurboKmph * 0.621371);
      } else {
        // Stage > 7 Extrapolation
        isApprox = true;
        const lastSt = stages[stages.length - 1] || { price: "200M", speedNoTurboKmph: 430, speedTurboKmph: 495 };
        const lastPrice = parseValueToNumber(lastSt.price || "200M");
        const extraStages = stageNum - 7;
        stagePriceNum = lastPrice * Math.pow(1.35, extraStages);
        speedNoTurboKmph = (lastSt.speedNoTurboKmph || 430) + (extraStages * 14);
        speedNoTurboMph = Math.round(speedNoTurboKmph * 0.621371);
        speedTurboKmph = (lastSt.speedTurboKmph || 495) + (extraStages * 16);
        speedTurboMph = Math.round(speedTurboKmph * 0.621371);
      }

      const items = [];
      let addOnsTotal = 0;

      // Words package, ceramic, edition STRICTLY REMOVED
      if (calcHasRainbow) {
        const p = parseValueToNumber(car.rainbowPrice || "15M");
        items.push({ label: "🌈 Rainbow Smoke", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasPolice) {
        const p = parseValueToNumber(car.policePrice || "20M");
        items.push({ label: "🚓 Police", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasCoating) {
        const p = parseValueToNumber(car.coatingPrice || "8M");
        items.push({ label: "🛡️ Coating", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasPremium) {
        const p = parseValueToNumber(car.premiumPrice || "10M");
        items.push({ label: "⭐ Premium", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasCustomLivery) {
        const p = parseValueToNumber(calcCustomLiveryPrice || "5M");
        items.push({ label: "🎨 Custom Livery", priceNum: p });
        addOnsTotal += p;
      }

      const baseCalc = stagePriceNum + addOnsTotal;
      // Valuation Range: between 95% and 115% of total
      const minTotal = Math.round(baseCalc * 0.95);
      const maxTotal = Math.round(baseCalc * 1.15);

      return {
        stageTitle: `Stage ${stageNum}`,
        stagePriceNum,
        speedNoTurboKmph,
        speedNoTurboMph,
        speedTurboKmph,
        speedTurboMph,
        items,
        minTotal,
        maxTotal,
        isApprox
      };
    }

    function selectCarForCalc(carId) {
      calcActiveCarId = carId;
      renderHubView();
    }

    function pickStage(stageNum) {
      calcSelectedStage = stageNum;
      calcCustomStage = null;
      renderHubView();
    }

    function onCustomStageInput(val) {
      const num = parseInt(val, 10);
      if (num && num > 0) {
        calcCustomStage = num;
      } else {
        calcCustomStage = null;
      }
      renderHubView();
    }

    function clearCustomStage() {
      calcCustomStage = null;
      calcSelectedStage = 1;
      renderHubView();
    }

    /* ==========================================================================
       2. RDS UPDATES (SPLIT INTO PUBLIC UPDATES & BETA UPDATES)
       ========================================================================== */
    function renderUpdates(container) {
      const allUpdates = STORE.state.updates || [];
      const publicUpdates = allUpdates.filter(u => (u.channel || 'public') === 'public');
      const betaUpdates = allUpdates.filter(u => (u.channel || '') === 'beta');

      const activeList = currentUpdatesChannel === 'beta' ? betaUpdates : publicUpdates;
      const canEdit = AUTH.hasPerm("updates") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">🚀 RDS Updates & Patch Notes</h2>
            <p class="view-subtitle-main">Official releases, beta test branches, and engine changelogs.</p>
          </div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openAppModal('modal-update-editor')"><i class="fa-solid fa-plus"></i> Announce Update</button>` : ""}
        </div>

        <!-- 2 Distinct Tabs: Public Updates & Beta Updates -->
        <div class="update-channel-tabs">
          <button class="update-tab-btn ${currentUpdatesChannel === 'public' ? 'active' : ''}" onclick="currentUpdatesChannel = 'public'; renderHubView();">
            🌐 Public Releases (${publicUpdates.length})
          </button>
          <button class="update-tab-btn ${currentUpdatesChannel === 'beta' ? 'active' : ''}" onclick="currentUpdatesChannel = 'beta'; renderHubView();">
            🧪 Beta Branches (${betaUpdates.length})
          </button>
        </div>

        <!-- Updates Listing -->
        <div style="display: flex; flex-direction: column; gap: 1.25rem;">
          ${activeList.length === 0 ? `
            <div class="liquid-glass" style="padding: 2.5rem; text-align: center; color: var(--text-dim);">
              No updates in this channel yet.
            </div>
          ` : activeList.map(u => `
            <div class="liquid-glass" style="padding: 1.75rem;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.75rem;">
                <div>
                  <span style="font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; color: var(--brand-orange);">${u.version}</span>
                  <span class="role-badge-tag" style="background: rgba(15, 23, 42, 0.1); margin-left: 0.5rem; padding: 0.25rem 0.6rem; border-radius: var(--radius-pill); font-size: 0.75rem; font-weight: 700;">
                    ${u.channel === 'beta' ? '🧪 Beta Test Branch' : '🌐 Official Public Release'}
                  </span>
                  ${u.author ? `<span style="font-size: 0.8rem; color: var(--text-dim); margin-left: 0.5rem;">By <strong>${u.author}</strong></span>` : ''}
                </div>
                <div style="display: flex; gap: 0.4rem;">
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-green); background: rgba(22, 163, 74, 0.15); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm);">
                    <i class="fa-brands fa-android"></i> Android: ${u.publishedAndroid ? 'Live' : 'Pending'}
                  </span>
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-green); background: rgba(22, 163, 74, 0.15); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm);">
                    <i class="fa-brands fa-apple"></i> iOS: ${u.publishedIos ? 'Live' : 'Pending'}
                  </span>
                </div>
              </div>

              <h3 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 0.5rem;">${u.title}</h3>
              ${u.image ? `<img src="${u.image}" style="width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; margin: 0.75rem 0; cursor: pointer;" onclick="openPhotoViewer('${u.image}', '${u.title}')">` : ''}

              <ul style="padding-left: 1.25rem; color: var(--text-muted); font-size: 0.9rem; line-height: 1.6; font-weight: 500;">
                ${(u.notes || []).map(note => `<li>${note}</li>`).join("")}
              </ul>

              ${canEdit ? `
                <div style="display: flex; justify-content: flex-end; gap: 0.5rem; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--glass-border-subtle);">
                  <button class="btn-brand-danger" onclick="deleteUpdate('${u.id}')"><i class="fa-solid fa-trash"></i> Delete</button>
                </div>
              ` : ''}
            </div>
          `).join("")}
        </div>
      `;
    }

    /* ==========================================================================
       3. TYRE CODES CATALOG (FULL CRUD + ONE-CLICK COPY)
       ========================================================================== */
    function renderTyreCodes(container) {
      const tyres = STORE.state.tyres || [];
      const canEdit = AUTH.hasPerm("tyres") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">⚙️ Tyre Codes & Tuning Compounds</h2>
            <p class="view-subtitle-main">Official friction compounds for drift, drag, grip and rally terrain.</p>
          </div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openTyreModal(null)"><i class="fa-solid fa-plus"></i> Add Tyre Code</button>` : ""}
        </div>

        <div class="tyres-grid-container">
          ${tyres.map(t => `
            <div class="liquid-glass" style="padding: 1.25rem; display: flex; flex-direction: column;">
              <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.4rem;">
                <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: var(--brand-orange);">${t.category}</span>
                <span style="font-size: 0.75rem; color: var(--accent-green); font-weight: 800;">${t.frictionIndex || ''}</span>
              </div>
              <h4 style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.35rem;">${t.name}</h4>
              <p style="font-size: 0.82rem; color: var(--text-muted); flex: 1; margin-bottom: 0.75rem; font-weight: 500;">${t.description}</p>
              <div style="background: rgba(255, 255, 255, 0.3); border: 1px solid var(--glass-border-subtle); padding: 0.65rem; border-radius: var(--radius-sm); display: flex; justify-content: space-between; align-items: center;">
                <code style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem;">${t.code}</code>
                <button class="btn-brand-primary" style="padding: 0.35rem 0.65rem; font-size: 0.75rem;" onclick="copyTyreCode('${t.code}')">
                  <i class="fa-regular fa-copy"></i> Copy
                </button>
              </div>
              ${canEdit ? `
                <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--glass-border-subtle);">
                  <button class="btn-brand-secondary" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="openTyreModal('${t.id}')"><i class="fa-solid fa-pen"></i></button>
                  <button class="btn-brand-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteTyre('${t.id}')"><i class="fa-solid fa-trash"></i></button>
                </div>
              ` : ''}
            </div>
          `).join("")}
        </div>
      `;
    }

    function copyTyreCode(code) {
      navigator.clipboard.writeText(code);
      AUDIO.play(880, 0.25);
      showToast(`Copied code: ${code}`);
    }

    /* ==========================================================================
       4. EVENTS (LIVE BADGE, TIMESTAMPS)
       ========================================================================== */
    function renderEvents(container) {
      const events = STORE.state.events || [];
      const canEdit = AUTH.hasPerm("events") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">🏆 Tournaments & Community Events</h2>
            <p class="view-subtitle-main">Official drag championships, touge battles, and prize events.</p>
          </div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openAppModal('modal-event-editor')"><i class="fa-solid fa-plus"></i> Create Event</button>` : ""}
        </div>

        <div class="events-grid-container">
          ${events.map(ev => `
            <div class="liquid-glass" style="overflow: hidden; display: flex; flex-direction: column;">
              <div style="height: 160px; position: relative;">
                <img src="${ev.image}" style="width: 100%; height: 100%; object-fit: cover;">
                ${ev.isLive ? `
                  <span style="position: absolute; top: 10px; left: 10px; background: var(--accent-red); color: #fff; padding: 0.25rem 0.6rem; border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 800;">
                    🔴 CURRENT LIVE EVENT
                  </span>
                ` : ''}
              </div>
              <div style="padding: 1.15rem; display: flex; flex-direction: column; flex: 1;">
                <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.4rem;">${ev.title}</h4>
                <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.5rem;"><i class="fa-solid fa-location-dot"></i> ${ev.location}</div>
                <p style="font-size: 0.82rem; color: var(--text-muted); flex: 1; margin-bottom: 0.75rem; font-weight: 500;">${ev.description}</p>
                <div style="background: rgba(255, 255, 255, 0.28); border: 1px solid var(--glass-border-subtle); padding: 0.65rem; border-radius: var(--radius-sm); font-size: 0.78rem;">
                  <strong>Prizes:</strong> ${ev.prizes}
                </div>
                ${canEdit ? `
                  <div style="display: flex; justify-content: flex-end; gap: 0.4rem; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--glass-border-subtle);">
                    <button class="btn-brand-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteEvent('${ev.id}')"><i class="fa-solid fa-trash"></i> Delete</button>
                  </div>
                ` : ''}
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }

    /* ==========================================================================
       5. MAPS, MULTIPLAYER & RULES
       ========================================================================== */
    function renderMaps(container) {
      const maps = STORE.state.maps || [];
      const canEdit = AUTH.hasPerm("maps") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">🗺️ Secret Locations & Drift Passes</h2><p class="view-subtitle-main">Key locations and drag runways across Real Driving School.</p></div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openMapModal(null)"><i class="fa-solid fa-plus"></i> Add Location</button>` : ""}
        </div>
        <div class="maps-grid-container">
          ${maps.map(m => `
            <div class="liquid-glass" style="overflow: hidden; display: flex; flex-direction: column;">
              <img src="${m.image}" style="width: 100%; height: 160px; object-fit: cover;">
              <div style="padding: 1.15rem; display: flex; flex-direction: column; flex: 1;">
                <span style="font-size: 0.72rem; color: var(--brand-orange); font-weight: 800; text-transform: uppercase;">${m.tag}</span>
                <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0.2rem 0 0.4rem 0;">${m.title}</h4>
                <p style="font-size: 0.82rem; color: var(--text-muted); font-weight: 500; flex: 1;">${m.description}</p>
                ${canEdit ? `
                  <div style="display: flex; justify-content: flex-end; margin-top: 0.75rem; padding-top: 0.5rem; border-top: 1px solid var(--glass-border-subtle);">
                    <button class="btn-brand-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteMap('${m.id}')"><i class="fa-solid fa-trash"></i> Delete</button>
                  </div>
                ` : ''}
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }

    function renderMultiplayer(container) {
      const guides = STORE.state.multiplayerGuides || [];
      const canEdit = AUTH.hasPerm("rules") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">👥 Multiplayer & Clan Etiquette</h2><p class="view-subtitle-main">Official server guidelines and race regulations.</p></div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openMpModal(null)"><i class="fa-solid fa-plus"></i> Add Guide</button>` : ""}
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${guides.map(g => `
            <div class="liquid-glass" style="padding: 1.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.5rem; color: var(--brand-orange);">${g.title}</h4>
                ${canEdit ? `<button class="btn-brand-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteMp('${g.id}')"><i class="fa-solid fa-trash"></i></button>` : ''}
              </div>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; font-weight: 500;">${g.content}</p>
            </div>
          `).join("")}
        </div>
      `;
    }

    function renderRules(container) {
      const rules = STORE.state.rules || [];
      const canEdit = AUTH.hasPerm("rules") || STORE.state.isEditingMode;

      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">⚖️ Rules of Conduct</h2><p class="view-subtitle-main">Fair play and trading protection rules.</p></div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openRuleModal(null)"><i class="fa-solid fa-plus"></i> Add Rule</button>` : ""}
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${rules.map(r => `
            <div class="liquid-glass" style="padding: 1.5rem;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.5rem; color: var(--accent-red);">${r.title}</h4>
                ${canEdit ? `<button class="btn-brand-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteRule('${r.id}')"><i class="fa-solid fa-trash"></i></button>` : ''}
              </div>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6; font-weight: 500;">${r.content}</p>
            </div>
          `).join("")}
        </div>
      `;
    }

    /* ==========================================================================
       6. ACTIVE GRINDERS & ONLINE USERS (CLEAN IN-GAME NAMES)
       ========================================================================== */
    function renderGrinders(container) {
      const list = STORE.activeOnlineDrivers && STORE.activeOnlineDrivers.length > 0
        ? STORE.activeOnlineDrivers
        : [
            { username: AUTH.user.username, avatar: AUTH.user.avatar, role: AUTH.user.roleName, lastActive: Date.now() },
            { username: "「 ⚡| Hyper_DαʀкSтαʀ 」", avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80", role: "Driver", lastActive: Date.now() - 60000 },
            { username: "ApexPredator_99", avatar: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=128&q=80", role: "Driver", lastActive: Date.now() - 180000 }
          ];

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">🔥 Active Grinders & Online Drivers</h2>
            <p class="view-subtitle-main">Live registered RDS drivers currently in lobbies and on this portal.</p>
          </div>
          <span class="cloud-sync-pill"><span class="cloud-sync-indicator"></span> ${list.length} Online</span>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem;">
          ${list.map(d => `
            <div class="liquid-glass" style="padding: 1rem; display: flex; align-items: center; gap: 0.85rem;">
              <img src="${d.avatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80'}" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover; border: 2px solid var(--brand-orange);">
              <div style="flex: 1; overflow: hidden;">
                <!-- Clean parsed name strictly displayed -->
                <div style="font-weight: 800; font-size: 0.92rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${d.username}</div>
                <div style="font-size: 0.75rem; color: var(--text-dim); display: flex; align-items: center; gap: 0.35rem;">
                  <span style="width: 6px; height: 6px; border-radius: 50%; background: var(--accent-green);"></span> Online
                </div>
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }

    /* ==========================================================================
       7. OWNER & STAFF CONTROL PANEL (COMPLETE WITH ALL 6 SUBTABS)
       ========================================================================== */
    function renderOwnerPanel(container) {
      // If user is not logged in as staff/owner, show login form inside the page
      if (!AUTH.user.isLoggedIn) {
        container.innerHTML = `
          <div class="liquid-glass" style="max-width: 540px; margin: 2rem auto; padding: 2.5rem;">
            <div style="text-align: center; margin-bottom: 1.5rem;">
              <div style="width: 60px; height: 60px; border-radius: 50%; background: rgba(255,107,0,0.15); color: var(--brand-orange); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 1rem auto; border: 1px solid rgba(255,107,0,0.4);">
                <i class="fa-solid fa-crown"></i>
              </div>
              <h2 style="font-family: var(--font-heading); font-size: 2rem; font-weight: 800; text-transform: uppercase;">Staff & Owner Portal</h2>
              <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 0.3rem;">Log in to access administrative controls, edit live website data, manage categories and sync.</p>
            </div>

            <form onsubmit="event.preventDefault(); submitInPageViewLogin();">
              <div class="form-group-item">
                <label class="form-field-label">Email Address</label>
                <input type="email" class="input-box-field" id="owner-page-email" placeholder="pennabadicharith@gmail.com" required>
              </div>
              <div class="form-group-item">
                <label class="form-field-label">Password</label>
                <input type="password" class="input-box-field" id="owner-page-pass" placeholder="••••••••" required>
              </div>
              <div id="owner-page-login-error" style="color: var(--accent-red); font-size: 0.82rem; margin-bottom: 0.75rem; display: none;"></div>
              <button type="submit" class="btn-brand-primary" style="width: 100%; justify-content: center; padding: 0.85rem; font-size: 1rem;">
                <i class="fa-solid fa-lock-open"></i> Log In to Staff Dashboard
              </button>
            </form>

            <div style="margin-top: 1.5rem; text-align: center; font-size: 0.78rem; color: var(--text-dim); border-top: 1px solid var(--glass-border-subtle); padding-top: 1rem;">
              💡 Tip: You can also tap <code>v1.2.120</code> 10 times in Settings to open the quick staff gate.
            </div>
          </div>
        `;
        return;
      }

      // User IS logged in: Render the complete Owner & Staff Dashboard
      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <div style="display: flex; align-items: center; gap: 0.6rem;">
              <h2 class="view-title-main">👑 Owner & Staff Control Center</h2>
              <span class="role-badge-tag" style="background: rgba(255,107,0,0.2); color: var(--brand-orange); border: 1px solid rgba(255,107,0,0.4); padding: 0.25rem 0.75rem; border-radius: var(--radius-pill); font-weight: 800; font-size: 0.8rem;">
                ${AUTH.user.roleName.toUpperCase()}
              </span>
            </div>
            <p class="view-subtitle-main">Full control of vehicle valuations, staff admins, Discord roles, categories, cloud database, and branding.</p>
          </div>

          <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            <!-- Live Editing Mode Toggle -->
            <label style="display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(255,255,255,0.4); border: 1px solid var(--glass-border); padding: 0.5rem 0.85rem; border-radius: var(--radius-pill); font-size: 0.85rem; font-weight: 700; cursor: pointer;">
              <i class="fa-solid fa-pen-ruler" style="color: var(--brand-orange);"></i>
              Live Editing Mode
              <input type="checkbox" ${STORE.state.isEditingMode ? 'checked' : ''} onchange="toggleEditingMode(this.checked)" style="transform: scale(1.2);">
            </label>

            <button class="btn-brand-danger" onclick="AUTH.logout(); renderHubView();">
              <i class="fa-solid fa-right-from-bracket"></i> Sign Out
            </button>
          </div>
        </div>

        <!-- Quick Action Shortcuts Bar -->
        <div class="liquid-glass" style="padding: 1rem; margin-bottom: 1.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center;">
          <span style="font-size: 0.8rem; font-weight: 800; color: var(--brand-orange); text-transform: uppercase; margin-right: 0.5rem;">
            <i class="fa-solid fa-bolt"></i> Quick Add:
          </span>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openCarModal(null)"><i class="fa-solid fa-car"></i> New Car</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openTyreModal(null)"><i class="fa-solid fa-circle-notch"></i> Tyre Code</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openAppModal('modal-event-editor')"><i class="fa-solid fa-trophy"></i> Event</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openAppModal('modal-update-editor')"><i class="fa-solid fa-rocket"></i> Update</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openMapModal(null)"><i class="fa-solid fa-map-pin"></i> Map</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openRuleModal(null)"><i class="fa-solid fa-scale-balanced"></i> Rule</button>
          <button class="btn-brand-secondary" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" onclick="openMpModal(null)"><i class="fa-solid fa-users"></i> Clan Guide</button>
        </div>

        <!-- Subtab Navigation Bar -->
        <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem; overflow-x: auto; padding-bottom: 0.5rem;">
          <button class="admin-subtab-btn ${currentAdminSubtab === 'admins' ? 'active' : ''}" onclick="switchAdminSubtab('admins')">
            <i class="fa-solid fa-user-shield"></i> Staff & Admins (${(STORE.state.admins||[]).length})
          </button>
          <button class="admin-subtab-btn ${currentAdminSubtab === 'roles' ? 'active' : ''}" onclick="switchAdminSubtab('roles')">
            <i class="fa-solid fa-shield"></i> Discord Roles (${(STORE.state.roles||[]).length})
          </button>
          <button class="admin-subtab-btn ${currentAdminSubtab === 'custom_cats' ? 'active' : ''}" onclick="switchAdminSubtab('custom_cats')">
            <i class="fa-solid fa-folder-tree"></i> Custom Categories (${(STORE.state.customCategories||[]).length})
          </button>
          <button class="admin-subtab-btn ${currentAdminSubtab === 'ui_settings' ? 'active' : ''}" onclick="switchAdminSubtab('ui_settings')">
            <i class="fa-solid fa-paintbrush"></i> UI & Branding
          </button>
          <button class="admin-subtab-btn ${currentAdminSubtab === 'security_db' ? 'active' : ''}" onclick="switchAdminSubtab('security_db')">
            <i class="fa-solid fa-database"></i> Cloud Database & Sync
          </button>
          <button class="admin-subtab-btn ${currentAdminSubtab === 'logs' ? 'active' : ''}" onclick="switchAdminSubtab('logs')">
            <i class="fa-solid fa-clock-rotate-left"></i> Security Audit Logs (${(STORE.state.auditLogs||[]).length})
          </button>
        </div>

        <!-- Subtab Content Area -->
        <div id="admin-subtab-container"></div>
      `;

      renderAdminSubtabContent();
    }

    function switchAdminSubtab(tabName) {
      currentAdminSubtab = tabName;
      document.querySelectorAll(".admin-subtab-btn").forEach(btn => {
        btn.classList.toggle("active", btn.textContent.toLowerCase().includes(tabName.replace('_', ' ')));
      });
      renderAdminSubtabContent();
    }

    function renderAdminSubtabContent() {
      const container = document.getElementById("admin-subtab-container");
      if (!container) return;

      if (currentAdminSubtab === "admins") {
        renderSubtabAdmins(container);
      } else if (currentAdminSubtab === "roles") {
        renderSubtabRoles(container);
      } else if (currentAdminSubtab === "custom_cats") {
        renderSubtabCustomCats(container);
      } else if (currentAdminSubtab === "ui_settings") {
        renderSubtabUiSettings(container);
      } else if (currentAdminSubtab === "security_db") {
        renderSubtabSecurityDb(container);
      } else if (currentAdminSubtab === "logs") {
        renderSubtabLogs(container);
      }
    }

    function renderSubtabAdmins(container) {
      const admins = STORE.state.admins || [];
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
              <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange);"><i class="fa-solid fa-user-shield"></i> Staff Administrators</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">Create admins with custom passwords, device limits, and category permissions.</p>
            </div>
            ${AUTH.user.isOwner ? `<button class="btn-brand-primary" onclick="openAppModal('modal-admin-editor')"><i class="fa-solid fa-user-plus"></i> Create Admin</button>` : ''}
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            ${admins.map(a => `
              <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.3); border: 1px solid var(--glass-border-subtle); padding: 0.85rem 1.15rem; border-radius: var(--radius-sm); flex-wrap: wrap; gap: 0.5rem;">
                <div>
                  <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <strong style="font-size: 1rem;">${a.name}</strong>
                    <span style="font-size: 0.75rem; color: var(--text-dim);">(${a.email})</span>
                    <span style="background: rgba(255,107,0,0.15); color: var(--brand-orange); font-size: 0.72rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 700;">${a.roleName || 'Admin'}</span>
                  </div>
                  <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.3rem;">
                    Device Limit: <strong>${a.deviceLimit || 2}</strong> | Custom Pass: <code>${a.password ? '••••••••' : 'Default'}</code> | Permissions: <em>${(a.permissions||[]).join(', ')}</em>
                  </div>
                </div>
                <div>
                  ${a.id !== 'adm_owner' && AUTH.user.isOwner ? `
                    <button class="btn-brand-danger" style="padding: 0.35rem 0.7rem; font-size: 0.78rem;" onclick="deleteAdmin('${a.id}')"><i class="fa-solid fa-trash"></i> Revoke</button>
                  ` : '<span style="font-size: 0.8rem; font-weight: 800; color: var(--brand-orange);"><i class="fa-solid fa-crown"></i> Game Owner</span>'}
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderSubtabRoles(container) {
      const roles = STORE.state.roles || [];
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
              <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange);"><i class="fa-solid fa-shield"></i> Discord-Style Roles</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">Manage roles, badges, colors, and assigned access levels.</p>
            </div>
            ${AUTH.user.isOwner ? `<button class="btn-brand-primary" onclick="openRoleModal(null)"><i class="fa-solid fa-plus"></i> Create Role</button>` : ''}
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            ${roles.map(r => `
              <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.3); border: 1px solid var(--glass-border-subtle); padding: 0.85rem 1.15rem; border-radius: var(--radius-sm);">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                  <span style="width: 14px; height: 14px; border-radius: 50%; background: ${r.color || '#ff6b00'}; border: 1px solid #fff;"></span>
                  <strong style="color: ${r.color || '#ff6b00'};">${r.name}</strong>
                  <span style="font-size: 0.78rem; color: var(--text-dim);">${(r.perms||[]).join(', ') || 'No permissions'}</span>
                </div>
                <div>
                  ${r.id !== 'owner' && AUTH.user.isOwner ? `
                    <button class="btn-brand-danger" style="padding: 0.35rem 0.65rem; font-size: 0.75rem;" onclick="deleteRole('${r.id}')"><i class="fa-solid fa-trash"></i></button>
                  ` : ''}
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderSubtabCustomCats(container) {
      const cats = STORE.state.customCategories || [];
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
              <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange);"><i class="fa-solid fa-folder-tree"></i> Custom Navigation Categories</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">Add new sections and content tabs to the main category dock.</p>
            </div>
            <button class="btn-brand-primary" onclick="openCategoryModal(null)"><i class="fa-solid fa-plus"></i> Add Category</button>
          </div>

          ${cats.length === 0 ? `
            <div style="padding: 2rem; text-align: center; color: var(--text-dim);">No custom categories created yet. Click above to add one!</div>
          ` : `
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
              ${cats.map(c => `
                <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.3); border: 1px solid var(--glass-border-subtle); padding: 0.85rem 1.15rem; border-radius: var(--radius-sm);">
                  <div>
                    <i class="${c.icon || 'fa-solid fa-star'}" style="color: var(--brand-orange); margin-right: 0.5rem;"></i>
                    <strong>${c.title}</strong>
                  </div>
                  <button class="btn-brand-danger" style="padding: 0.35rem 0.65rem; font-size: 0.75rem;" onclick="deleteCategory('${c.id}')"><i class="fa-solid fa-trash"></i> Delete</button>
                </div>
              `).join("")}
            </div>
          `}
        </div>
      `;
    }

    function renderSubtabUiSettings(container) {
      const cfg = STORE.state.hubConfig || {};
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
              <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange);"><i class="fa-solid fa-paintbrush"></i> Portal UI & Branding Customizer</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">Edit game title, branding logo, background video/photo wallpaper, and social invite links.</p>
            </div>
            <button class="btn-brand-primary" onclick="openAppModal('modal-ui-editor')"><i class="fa-solid fa-pen"></i> Edit Branding</button>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
            <div style="background: rgba(255,255,255,0.3); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
              <div style="font-size: 0.78rem; text-transform: uppercase; font-weight: 700; color: var(--text-dim);">Portal Title</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--brand-orange);">${cfg.title || 'REAL DRIVING SCHOOL'}</div>
              <div style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted);">${cfg.about || ''}</div>
            </div>

            <div style="background: rgba(255,255,255,0.3); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
              <div style="font-size: 0.78rem; text-transform: uppercase; font-weight: 700; color: var(--text-dim);">Background Mode</div>
              <div style="font-size: 1.05rem; font-weight: 800;">${cfg.bgType === 'image' ? '🖼️ Photo Wallpaper' : '🎥 High-Definition Video'}</div>
              <div style="font-size: 0.78rem; color: var(--text-muted); word-break: break-all; margin-top: 0.25rem;">${cfg.bgMediaUrl || ''}</div>
            </div>
          </div>
        </div>
      `;
    }

    function renderSubtabSecurityDb(container) {
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange); margin-bottom: 0.5rem;">
            <i class="fa-solid fa-database"></i> Zero-Budget Cloud Database ($0 Free Tier)
          </h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem;">
            Connected to Google Firebase Real-Time Firestore & Storage. Multi-document architecture prevents document limit errors.
          </p>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
            <div style="background: rgba(255,255,255,0.3); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-dim); font-weight: 700;">Connection Status</div>
              <div style="font-size: 1.1rem; font-weight: 800; color: var(--accent-green); display: flex; align-items: center; gap: 0.5rem; margin-top: 0.25rem;">
                <span class="cloud-sync-indicator"></span> 🟢 Online & Live Synced
              </div>
              <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.25rem;">Firebase Project: <code>rds-a95fc</code></div>
            </div>

            <div style="background: rgba(255,255,255,0.3); padding: 1rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-dim); font-weight: 700;">Storage Bucket</div>
              <div style="font-size: 0.92rem; font-weight: 700; margin-top: 0.25rem;"><code>rds-a95fc.firebasestorage.app</code></div>
              <div style="font-size: 0.78rem; color: var(--accent-green); margin-top: 0.25rem;"><i class="fa-solid fa-check"></i> Canvas auto-compression enabled (~40KB/img)</div>
            </div>
          </div>

          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button class="btn-brand-primary" onclick="triggerManualSync()"><i class="fa-solid fa-arrows-rotate"></i> Sync All to Cloud Now</button>
            <button class="btn-brand-secondary" onclick="exportDataJson()"><i class="fa-solid fa-download"></i> Backup Data (JSON)</button>
          </div>
        </div>
      `;
    }

    function renderSubtabLogs(container) {
      const logs = STORE.state.auditLogs || [];
      container.innerHTML = `
        <div class="liquid-glass" style="padding: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
            <div>
              <h3 style="font-family: var(--font-heading); font-size: 1.35rem; color: var(--brand-orange);"><i class="fa-solid fa-clock-rotate-left"></i> Security & Audit Logs</h3>
              <p style="font-size: 0.85rem; color: var(--text-muted);">Real-time recording of all logins, content additions, edits and admin privileges.</p>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.5rem; max-height: 420px; overflow-y: auto;">
            ${logs.length === 0 ? `<div style="font-size: 0.85rem; color: var(--text-dim);">No audit logs recorded yet.</div>` : logs.map(l => `
              <div style="background: rgba(255,255,255,0.3); border: 1px solid var(--glass-border-subtle); padding: 0.65rem 0.95rem; border-radius: var(--radius-sm); font-size: 0.82rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <span style="font-weight: 800; color: var(--brand-orange);">[${l.category.toUpperCase()}]</span>
                  <strong>${l.user}</strong>: ${l.action} - <span style="color: var(--text-muted); font-weight: 500;">${l.details}</span>
                </div>
                <span style="font-size: 0.72rem; color: var(--text-dim);">${new Date(l.timestamp).toLocaleTimeString()}</span>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    function renderCustomCategoryView(container, catId) {
      const cat = (STORE.state.customCategories || []).find(c => c.id === catId);
      if (!cat) {
        container.innerHTML = `<div class="liquid-glass" style="padding: 2rem;"><h3>Category Not Found</h3></div>`;
        return;
      }

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main"><i class="${cat.icon || 'fa-solid fa-star'}"></i> ${cat.title}</h2>
            <p class="view-subtitle-main">Custom community category created by Game Owner.</p>
          </div>
        </div>
        <div class="liquid-glass" style="padding: 2rem; font-size: 0.95rem; line-height: 1.7;">
          ${cat.content || 'No content provided.'}
        </div>
      `;
    }

    function toggleEditingMode(val) {
      STORE.state.isEditingMode = val;
      renderHubView();
      showToast(val ? "Live Editing Mode ON" : "Live Editing Mode OFF");
    }

    function submitInPageViewLogin() {
      const email = document.getElementById("owner-page-email").value;
      const pass = document.getElementById("owner-page-pass").value;
      const res = AUTH.login(email, pass);
      const errBox = document.getElementById("owner-page-login-error");

      if (res.success) {
        if (errBox) errBox.style.display = "none";
        AUDIO.play(880, 0.4);
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

    async function triggerManualSync() {
      showToast("Syncing all data with cloud...");
      await FIREBASE.syncAll();
    }

    function exportDataJson() {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(STORE.state, null, 2));
      const downloadAnchor = document.createElement("a");
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `RDS_Portal_Backup_${Date.now()}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
      showToast("Backup exported successfully!");
    }
'''
