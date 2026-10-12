# part_js_views.py - View Renderers & Calculator for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

JS_VIEWS_CONTENT = r'''
    /* ==========================================================================
       VIEW ROUTING & RENDERING LOGIC
       ========================================================================== */
    let currentHubView = "car-prices";
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
    }

    /* ==========================================================================
       1. CAR PRICES & VALUE CALCULATOR (SEARCH, JUMP, STAGES 1-7, 4 ADD-ONS)
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

      const canEdit = AUTH.hasPerm("cars");

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
              <div style="margin-top: 0.65rem; background: var(--bg-base); padding: 0.65rem; border-radius: var(--radius-sm); border: 1px solid var(--glass-border-subtle);">
                <label class="form-field-label" style="font-size: 0.75rem;">Enter Custom Stage (> Stage 7 - Extrapolates Dynamic Value)</label>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem;">
                  <input type="number" min="1" max="50" class="input-box-field" placeholder="e.g. 8, 10, 15" value="${calcCustomStage || ''}" oninput="onCustomStageInput(this.value)" style="padding: 0.45rem 0.75rem;">
                  <button type="button" class="btn-brand-secondary" onclick="clearCustomStage()" style="padding: 0.45rem 0.75rem; font-size: 0.78rem;">Reset</button>
                </div>
              </div>
              ${calcCustomStage && calcCustomStage > 7 ? `
                <div style="margin-top: 0.4rem; font-size: 0.75rem; color: #d97706; font-weight: 600;">
                  ⚠️ Note: Stage ${calcCustomStage} is an approximate valuation based on exponential stage scaling.
                </div>
              ` : ''}
            </div>

            <!-- The 4 Add-ons + Custom Livery -->
            <div class="form-group-item">
              <label class="form-field-label">Vehicle Add-ons & Packages</label>
              <div style="display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.35rem;">
                <!-- 1. Rainbow Smoke -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 600;">🌈 Rainbow Smoke (${activeCar ? activeCar.rainbowPrice || '15M' : '15M'})</span>
                  <input type="checkbox" ${calcHasRainbow ? 'checked' : ''} onchange="calcHasRainbow = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 2. Police Package -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 600;">🚓 Police Siren / Package (${activeCar ? activeCar.policePrice || '20M' : '20M'})</span>
                  <input type="checkbox" ${calcHasPolice ? 'checked' : ''} onchange="calcHasPolice = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 3. Ceramic Coating -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 600;">🛡️ Ceramic Coating (${activeCar ? activeCar.coatingPrice || '8M' : '8M'})</span>
                  <input type="checkbox" ${calcHasCoating ? 'checked' : ''} onchange="calcHasCoating = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 4. Premium Edition -->
                <label style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); cursor: pointer;">
                  <span style="font-size: 0.88rem; font-weight: 600;">⭐ Premium Edition (${activeCar ? activeCar.premiumPrice || '10M' : '10M'})</span>
                  <input type="checkbox" ${calcHasPremium ? 'checked' : ''} onchange="calcHasPremium = this.checked; renderHubView();" style="transform: scale(1.3);">
                </label>

                <!-- 5. Custom Livery (Asks for price if yes) -->
                <div style="background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm);">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.88rem; font-weight: 600;">🎨 Custom Livery / Vinyl Wrap</span>
                    <input type="checkbox" ${calcHasCustomLivery ? 'checked' : ''} onchange="calcHasCustomLivery = this.checked; renderHubView();" style="transform: scale(1.3);">
                  </div>
                  ${calcHasCustomLivery ? `
                    <div style="margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                      <span style="font-size: 0.78rem; color: var(--text-muted);">Livery Custom Price:</span>
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
                <div style="font-size: 0.72rem; color: var(--text-dim);">CERTIFIED</div>
              </div>
            </div>

            <div style="margin-bottom: 1rem;">
              <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.2rem;">${activeCar ? activeCar.name : 'Vehicle'}</h4>
              <div style="font-size: 0.82rem; color: var(--text-muted);">${billData.stageTitle}</div>
            </div>

            <!-- Technical Performance Metrics -->
            <div style="background: var(--bg-base); padding: 0.65rem 0.85rem; border-radius: var(--radius-sm); margin-bottom: 1rem; font-size: 0.8rem; display: flex; flex-direction: column; gap: 0.25rem;">
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-dim);">Top Speed (No Turbo):</span>
                <strong>${billData.speedNoTurboKmph} km/h (${billData.speedNoTurboMph} mph)</strong>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-dim);">Top Speed (With Turbo):</span>
                <strong style="color: var(--brand-orange);">${billData.speedTurboKmph} km/h (${billData.speedTurboMph} mph)</strong>
              </div>
            </div>

            <!-- Itemized Pricing Breakdown -->
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
                <div style="font-size: 0.72rem; color: var(--text-muted);">${billData.isApprox ? 'Approximate Estimate' : 'Calculated Value'}</div>
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

      if (calcHasRainbow) {
        const p = parseValueToNumber(car.rainbowPrice || "15M");
        items.push({ label: "🌈 Rainbow Smoke", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasPolice) {
        const p = parseValueToNumber(car.policePrice || "20M");
        items.push({ label: "🚓 Police Siren / Package", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasCoating) {
        const p = parseValueToNumber(car.coatingPrice || "8M");
        items.push({ label: "🛡️ Ceramic Coating", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasPremium) {
        const p = parseValueToNumber(car.premiumPrice || "10M");
        items.push({ label: "⭐ Premium Edition", priceNum: p });
        addOnsTotal += p;
      }
      if (calcHasCustomLivery) {
        const p = parseValueToNumber(calcCustomLiveryPrice || "5M");
        items.push({ label: "🎨 Custom Livery / Wrap", priceNum: p });
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
      const canEdit = AUTH.hasPerm("updates");

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
                  <span class="role-badge-tag" style="background: rgba(15, 23, 42, 0.08); margin-left: 0.5rem; padding: 0.25rem 0.6rem; border-radius: var(--radius-pill); font-size: 0.75rem; font-weight: 700;">
                    ${u.channel === 'beta' ? '🧪 Beta Test Branch' : '🌐 Official Public Release'}
                  </span>
                  ${u.author ? `<span style="font-size: 0.8rem; color: var(--text-dim); margin-left: 0.5rem;">By <strong>${u.author}</strong></span>` : ''}
                </div>
                <div style="display: flex; gap: 0.4rem;">
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-green); background: rgba(22, 163, 74, 0.12); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm);">
                    <i class="fa-brands fa-android"></i> Android: ${u.publishedAndroid ? 'Live' : 'Pending'}
                  </span>
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-green); background: rgba(22, 163, 74, 0.12); padding: 0.25rem 0.5rem; border-radius: var(--radius-sm);">
                    <i class="fa-brands fa-apple"></i> iOS: ${u.publishedIos ? 'Live' : 'Pending'}
                  </span>
                </div>
              </div>

              <h3 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 0.5rem;">${u.title}</h3>
              ${u.image ? `<img src="${u.image}" style="width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; margin: 0.75rem 0; cursor: pointer;" onclick="openPhotoViewer('${u.image}', '${u.title}')">` : ''}

              <ul style="padding-left: 1.25rem; color: var(--text-muted); font-size: 0.9rem; line-height: 1.6;">
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
       3. TYRE CODES CATALOG (COPY TO CLIPBOARD WITH SOUND)
       ========================================================================== */
    function renderTyreCodes(container) {
      const tyres = STORE.state.tyres || [];
      const canEdit = AUTH.hasPerm("tyres");

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">⚙️ Tyre Codes & Tuning Compounds</h2>
            <p class="view-subtitle-main">Official friction compounds for drift, drag, grip and rally terrain.</p>
          </div>
          ${canEdit ? `<button class="btn-brand-primary" onclick="openAppModal('modal-tyre-editor')"><i class="fa-solid fa-plus"></i> Add Tyre Code</button>` : ""}
        </div>

        <div class="tyres-grid-container">
          ${tyres.map(t => `
            <div class="liquid-glass" style="padding: 1.25rem; display: flex; flex-direction: column;">
              <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.4rem;">
                <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: var(--brand-orange);">${t.category}</span>
                <span style="font-size: 0.75rem; color: var(--accent-green); font-weight: 700;">${t.frictionIndex || ''}</span>
              </div>
              <h4 style="font-size: 1.1rem; font-weight: 800; margin-bottom: 0.35rem;">${t.name}</h4>
              <p style="font-size: 0.82rem; color: var(--text-muted); flex: 1; margin-bottom: 0.75rem;">${t.description}</p>
              <div style="background: var(--bg-base); padding: 0.65rem; border-radius: var(--radius-sm); display: flex; justify-content: space-between; align-items: center;">
                <code style="font-family: var(--font-mono); font-weight: 700; font-size: 0.85rem;">${t.code}</code>
                <button class="btn-brand-primary" style="padding: 0.35rem 0.65rem; font-size: 0.75rem;" onclick="copyTyreCode('${t.code}')">
                  <i class="fa-regular fa-copy"></i> Copy
                </button>
              </div>
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
      const canEdit = AUTH.hasPerm("events");

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
                  <span style="position: absolute; top: 10px; left: 10px; background: var(--accent-red); color: #fff; padding: 0.25rem 0.6rem; border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 800; animation: pulse 1.5s infinite;">
                    🔴 CURRENT LIVE EVENT
                  </span>
                ` : ''}
              </div>
              <div style="padding: 1.15rem; display: flex; flex-direction: column; flex: 1;">
                <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.4rem;">${ev.title}</h4>
                <div style="font-size: 0.8rem; color: var(--text-dim); margin-bottom: 0.5rem;"><i class="fa-solid fa-location-dot"></i> ${ev.location}</div>
                <p style="font-size: 0.82rem; color: var(--text-muted); flex: 1; margin-bottom: 0.75rem;">${ev.description}</p>
                <div style="background: var(--bg-base); padding: 0.65rem; border-radius: var(--radius-sm); font-size: 0.78rem;">
                  <strong>Prizes:</strong> ${ev.prizes}
                </div>
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
      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">🗺️ Secret Locations & Drift Passes</h2><p class="view-subtitle-main">Key locations and drag runways across Real Driving School.</p></div>
        </div>
        <div class="maps-grid-container">
          ${maps.map(m => `
            <div class="liquid-glass" style="overflow: hidden;">
              <img src="${m.image}" style="width: 100%; height: 160px; object-fit: cover;">
              <div style="padding: 1.15rem;">
                <span style="font-size: 0.72rem; color: var(--brand-orange); font-weight: 800; text-transform: uppercase;">${m.tag}</span>
                <h4 style="font-size: 1.1rem; font-weight: 800; margin: 0.2rem 0 0.4rem 0;">${m.title}</h4>
                <p style="font-size: 0.82rem; color: var(--text-muted);">${m.description}</p>
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }

    function renderMultiplayer(container) {
      const guides = STORE.state.multiplayerGuides || [];
      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">👥 Multiplayer & Clan Etiquette</h2><p class="view-subtitle-main">Official server guidelines and race regulations.</p></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${guides.map(g => `
            <div class="liquid-glass" style="padding: 1.5rem;">
              <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.5rem; color: var(--brand-orange);">${g.title}</h4>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">${g.content}</p>
            </div>
          `).join("")}
        </div>
      `;
    }

    function renderRules(container) {
      const rules = STORE.state.rules || [];
      container.innerHTML = `
        <div class="view-header-bar">
          <div><h2 class="view-title-main">⚖️ Rules of Conduct</h2><p class="view-subtitle-main">Fair play and trading protection rules.</p></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1rem;">
          ${rules.map(r => `
            <div class="liquid-glass" style="padding: 1.5rem;">
              <h4 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.5rem; color: var(--accent-red);">${r.title}</h4>
              <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">${r.content}</p>
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
       7. OWNER & STAFF CONTROL PANEL
       ========================================================================== */
    function renderOwnerPanel(container) {
      if (!AUTH.user.isOwner && !AUTH.user.isLoggedIn) {
        container.innerHTML = `<div class="liquid-glass" style="padding: 3rem; text-align: center;"><h3>Access Restricted</h3><p style="color: var(--text-dim);">Please authenticate via the Staff Security Gate.</p></div>`;
        return;
      }

      const admins = STORE.state.admins || [];
      const logs = STORE.state.auditLogs || [];

      container.innerHTML = `
        <div class="view-header-bar">
          <div>
            <h2 class="view-title-main">👑 Portal Administration & Owner Panel</h2>
            <p class="view-subtitle-main">Global styling, administrator creation, permissions, and security audit logs.</p>
          </div>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            ${AUTH.user.isOwner ? `<button class="btn-brand-primary" onclick="openAppModal('modal-ui-editor')"><i class="fa-solid fa-paintbrush"></i> Customize UI & Branding</button>` : ""}
            ${AUTH.user.isOwner ? `<button class="btn-brand-secondary" onclick="openAppModal('modal-admin-editor')"><i class="fa-solid fa-user-plus"></i> Create Admin</button>` : ""}
          </div>
        </div>

        <!-- Admins Table (For Owner) -->
        ${AUTH.user.isOwner ? `
          <div class="liquid-glass" style="padding: 1.5rem; margin-bottom: 1.5rem;">
            <h3 style="font-family: var(--font-heading); color: var(--brand-orange); margin-bottom: 0.75rem;">
              <i class="fa-solid fa-users-gear"></i> Staff Administrators (${admins.length})
            </h3>
            <div style="display: flex; flex-direction: column; gap: 0.65rem;">
              ${admins.map(a => `
                <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-base); padding: 0.75rem 1rem; border-radius: var(--radius-sm); flex-wrap: wrap; gap: 0.5rem;">
                  <div>
                    <strong>${a.name}</strong> <span style="font-size: 0.78rem; color: var(--text-dim);">(${a.email})</span>
                    <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem;">
                      Device Limit: <strong>${a.deviceLimit || 2}</strong> | Passphrase: <code>${a.password ? '••••••••' : 'Default'}</code>
                    </div>
                  </div>
                  <div>
                    ${a.id !== 'adm_owner' ? `
                      <button class="btn-brand-danger" style="padding: 0.35rem 0.6rem; font-size: 0.75rem;" onclick="deleteAdmin('${a.id}')"><i class="fa-solid fa-trash"></i> Revoke</button>
                    ` : '<span style="font-size: 0.78rem; color: var(--brand-orange); font-weight: 700;">Owner (Superadmin)</span>'}
                  </div>
                </div>
              `).join("")}
            </div>
          </div>
        ` : ''}

        <!-- Audit Logs -->
        <div class="liquid-glass" style="padding: 1.5rem;">
          <h3 style="font-family: var(--font-heading); color: var(--brand-orange); margin-bottom: 0.75rem;">
            <i class="fa-solid fa-clock-rotate-left"></i> Security & Operation Audit Logs
          </h3>
          <div style="display: flex; flex-direction: column; gap: 0.5rem; max-height: 400px; overflow-y: auto;">
            ${logs.length === 0 ? `<div style="font-size: 0.85rem; color: var(--text-dim);">No audit logs recorded yet.</div>` : logs.map(l => `
              <div style="background: var(--bg-base); padding: 0.6rem 0.85rem; border-radius: var(--radius-sm); font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center;">
                <div>
                  <span style="font-weight: 700; color: var(--brand-orange);">[${l.category.toUpperCase()}]</span>
                  <strong>${l.user}</strong>: ${l.action} - <span style="color: var(--text-muted);">${l.details}</span>
                </div>
                <span style="font-size: 0.72rem; color: var(--text-dim);">${new Date(l.timestamp).toLocaleTimeString()}</span>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }
'''
