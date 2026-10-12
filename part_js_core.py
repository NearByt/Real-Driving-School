# part_js_core.py - Core Engine, Firebase Multi-Doc Sync, Compressor & Auth for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

JS_CORE_CONTENT = r'''
  <script>
    /* ==========================================================================
       REAL DRIVING SCHOOL OFFICIAL PORTAL - CORE LOGIC ENGINE v1.2.120
       ========================================================================== */

    const DEFAULT_FIREBASE_CONFIG = {
      apiKey: "AIzaSyBlRiz74eFt5zWOIowVEOgxQEAHuLfM3e0",
      authDomain: "rds-a95fc.firebaseapp.com",
      projectId: "rds-a95fc",
      storageBucket: "rds-a95fc.firebasestorage.app",
      messagingSenderId: "935312096631",
      appId: "1:935312096631:web:a3183d86ad0c0ffec5b572",
      measurementId: "G-W84EM7C47F"
    };

    // Helper: Parse suffixes (k, m, b, t) to plain numeric value
    function parseValueToNumber(val) {
      if (typeof val === "number") return val;
      if (!val) return 0;
      val = val.toString().trim().toLowerCase();
      let mult = 1000000; // default is millions as requested
      if (val.endsWith("k")) { mult = 1000; val = val.slice(0, -1); }
      else if (val.endsWith("m")) { mult = 1000000; val = val.slice(0, -1); }
      else if (val.endsWith("b")) { mult = 1000000000; val = val.slice(0, -1); }
      else if (val.endsWith("t")) { mult = 1000000000000; val = val.slice(0, -1); }
      const num = parseFloat(val);
      return isNaN(num) ? 0 : num * mult;
    }

    // Helper: Format large numbers into clean readable currency
    function formatNumberAbbr(num) {
      if (!num || isNaN(num)) return "0";
      if (num >= 1e12) return (num / 1e12).toFixed(2).replace(/\.00$/, '') + "T";
      if (num >= 1e9) return (num / 1e9).toFixed(2).replace(/\.00$/, '') + "B";
      if (num >= 1e6) return (num / 1e6).toFixed(2).replace(/\.00$/, '') + "M";
      if (num >= 1e3) return (num / 1e3).toFixed(1).replace(/\.0$/, '') + "k";
      return num.toLocaleString();
    }

    // Parse RDS In-Game ID: strips trailing Firebase 28-char UID, NEVER appends UID to clean names!
    function parseRDSPlayerId(rawText) {
      if (!rawText) return { cleanName: "StreetRacer", gameUid: "" };
      const str = rawText.trim();
      const match = str.match(/^(.*?)(?:\s+([A-Za-z0-9_-]{20,36}))$/);
      if (match && match[1] && match[2]) {
        return {
          cleanName: match[1].trim(),
          gameUid: match[2].trim()
        };
      }
      return { cleanName: str, gameUid: "" };
    }

    /* ==========================================================================
       CANVAS IMAGE COMPRESSOR ($0 Free Tier - Shrinks uploads to 50KB-90KB)
       ========================================================================== */
    async function compressImageFile(file, maxDimension = 1200, quality = 0.72) {
      return new Promise((resolve, reject) => {
        if (!file.type.startsWith("image/")) {
          // If video or other file, return as data url or raw
          const reader = new FileReader();
          reader.onload = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(file);
          return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
          const img = new Image();
          img.onload = () => {
            let width = img.width;
            let height = img.height;

            if (width > maxDimension || height > maxDimension) {
              if (width > height) {
                height = Math.round((height * maxDimension) / width);
                width = maxDimension;
              } else {
                width = Math.round((width * maxDimension) / height);
                height = maxDimension;
              }
            }

            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);
            const compressedDataUrl = canvas.toDataURL("image/jpeg", quality);
            resolve(compressedDataUrl);
          };
          img.onerror = reject;
          img.src = e.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    }

    // Unified Gallery/Files Picker with Canvas Auto-Compression
    function openLocalFilePicker(targetInputId, previewId = null, isVideo = false) {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = isVideo ? "video/*,image/*" : "image/*,video/*";
      fileInput.onchange = async (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        showToast("Processing & optimizing media...");
        try {
          const compressedData = await compressImageFile(file);
          let mediaUrl = compressedData;

          // Attempt upload to Firebase Storage if available
          if (FIREBASE && FIREBASE.storage) {
            try {
              const storageRef = FIREBASE.storage.ref(`uploads/${Date.now()}_${file.name.replace(/[^a-zA-Z0-9.]/g, '_')}`);
              // If data URL, upload as string
              const snapshot = await storageRef.putString(compressedData, 'data_url');
              mediaUrl = await snapshot.ref.getDownloadURL();
            } catch(stErr) {
              console.warn("Storage upload notice (falling back to compressed data URL):", stErr);
            }
          }

          const inp = document.getElementById(targetInputId);
          if (inp) {
            inp.value = mediaUrl;
            inp.dispatchEvent(new Event("change"));
          }
          if (previewId) {
            const prev = document.getElementById(previewId);
            if (prev) {
              prev.src = mediaUrl;
              prev.style.display = "block";
            }
          }
          showToast("Media ready and attached!");
        } catch(err) {
          console.error("File processing error:", err);
          showToast("Error processing file", "error");
        }
      };
      fileInput.click();
    }

    /* ==========================================================================
       MULTI-DOCUMENT REAL-TIME FIREBASE SYNC ENGINE ($0 Global Multi-Device Sync)
       Splits collections into separate documents to never exceed Firestore 1MiB limit.
       ========================================================================== */
    class FirebaseSyncEngine {
      constructor() {
        this.app = null;
        this.db = null;
        this.storage = null;
        this.auth = null;
        this.connected = false;
        this.init();
      }

      init() {
        try {
          if (typeof firebase !== "undefined") {
            if (!firebase.apps.length) {
              this.app = firebase.initializeApp(DEFAULT_FIREBASE_CONFIG);
            } else {
              this.app = firebase.app();
            }
            this.db = firebase.firestore();
            this.storage = firebase.storage();
            this.auth = firebase.auth();

            // Anonymous auth ensures seamless read/write access
            this.auth.signInAnonymously().catch(err => {
              console.warn("Firebase anonymous auth notice:", err);
            });

            this.connected = true;
            this.listenToHubCollections();
            this.registerOnlineSession();
            console.log("Firebase initialized successfully with rds-a95fc");
          }
        } catch(err) {
          console.warn("Firebase initialization notice:", err);
        }
      }

      // Listen to all sub-documents under rds_hub/
      listenToHubCollections() {
        if (!this.db) return;
        try {
          this.db.collection("rds_hub").onSnapshot(snapshot => {
            let hasChanges = false;
            snapshot.docChanges().forEach(change => {
              const docId = change.doc.id;
              const data = change.doc.data();
              if (!data) return;

              if (docId === "cars" && Array.isArray(data.items)) {
                STORE.state.cars = data.items;
                hasChanges = true;
              } else if (docId === "events" && Array.isArray(data.items)) {
                STORE.state.events = data.items;
                hasChanges = true;
              } else if (docId === "updates" && Array.isArray(data.items)) {
                STORE.state.updates = data.items;
                hasChanges = true;
              } else if (docId === "tyres" && Array.isArray(data.items)) {
                STORE.state.tyres = data.items;
                hasChanges = true;
              } else if (docId === "maps" && Array.isArray(data.items)) {
                STORE.state.maps = data.items;
                hasChanges = true;
              } else if (docId === "rules" && Array.isArray(data.items)) {
                STORE.state.rules = data.items;
                hasChanges = true;
              } else if (docId === "multiplayer" && Array.isArray(data.items)) {
                STORE.state.multiplayerGuides = data.items;
                hasChanges = true;
              } else if (docId === "admins" && Array.isArray(data.items)) {
                STORE.state.admins = data.items;
                hasChanges = true;
              } else if (docId === "roles" && Array.isArray(data.items)) {
                STORE.state.roles = data.items;
                hasChanges = true;
              } else if (docId === "logs" && Array.isArray(data.items)) {
                STORE.state.auditLogs = data.items;
                hasChanges = true;
              } else if (docId === "config") {
                Object.assign(STORE.state.hubConfig, data);
                applyHubConfigToUI();
                hasChanges = true;
              }
            });

            if (hasChanges) {
              STORE.saveLocal();
              renderHubView();
              updateHeaderUserUI();
              showSyncPill("Cloud Synced");
            }
          }, err => {
            console.warn("Firestore listener notice:", err);
          });

          // Listen for active sessions
          this.db.collection("rds_sessions").onSnapshot(snapshot => {
            const list = [];
            const now = Date.now();
            snapshot.forEach(doc => {
              const d = doc.data();
              if (d && (now - (d.lastActive || 0)) < 15 * 60 * 1000) {
                list.push(d);
              }
            });
            STORE.activeOnlineDrivers = list;
            if (currentHubView === "grinders") renderHubView();
          }, err => {});
        } catch(e) {}
      }

      // Sync specific collection to Firestore document
      async syncDoc(docName, payload) {
        if (!this.db) return false;
        try {
          payload.updatedAt = Date.now();
          await this.db.collection("rds_hub").doc(docName).set(payload, { merge: true });
          showSyncPill("Cloud Synced");
          return true;
        } catch(err) {
          console.warn(`Firestore sync write error for ${docName}:`, err);
          return false;
        }
      }

      // Register live driver session in Firestore
      async registerOnlineSession() {
        if (!this.db) return;
        try {
          let sessId = localStorage.getItem("RDS_SESSION_TOKEN");
          if (!sessId) {
            sessId = "sess_" + Math.random().toString(36).substring(2, 10);
            localStorage.setItem("RDS_SESSION_TOKEN", sessId);
          }
          const user = (typeof AUTH !== "undefined" && AUTH.user) ? AUTH.user : { username: "Driver", roleName: "Driver" };
          const updateData = {
            id: sessId,
            username: user.username || "Driver",
            avatar: user.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80",
            role: user.roleName || "Driver",
            lastActive: Date.now()
          };
          await this.db.collection("rds_sessions").doc(sessId).set(updateData, { merge: true });
        } catch(e) {}
      }
    }

    const FIREBASE = new FirebaseSyncEngine();

    /* ==========================================================================
       AUTHENTICATION & DRIVER IDENTITY ENGINE
       ========================================================================== */
    class AuthEngine {
      constructor() {
        this.user = this.load();
      }

      load() {
        const s = sessionStorage.getItem("RDS_AUTH_USER");
        if (s) {
          try { return JSON.parse(s); } catch(e) {}
        }
        return {
          id: "guest_" + Math.random().toString(36).substr(2, 6),
          username: localStorage.getItem("RDS_USER_NAME") || "StreetRacer",
          gameUid: localStorage.getItem("RDS_USER_GAME_UID") || "",
          avatar: localStorage.getItem("RDS_USER_AVATAR") || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80",
          roleId: "player",
          roleName: "Driver",
          roleColor: "#64748b",
          permissions: [],
          isOwner: false,
          isLoggedIn: false
        };
      }

      save() {
        sessionStorage.setItem("RDS_AUTH_USER", JSON.stringify(this.user));
        if (!this.user.isLoggedIn) {
          localStorage.setItem("RDS_USER_NAME", this.user.username);
          localStorage.setItem("RDS_USER_AVATAR", this.user.avatar);
          if (this.user.gameUid) localStorage.setItem("RDS_USER_GAME_UID", this.user.gameUid);
        }
        updateHeaderUserUI();
        if (FIREBASE) FIREBASE.registerOnlineSession();
      }

      login(email, pass) {
        email = (email || "").trim().toLowerCase();
        pass = (pass || "").trim();

        // 1. OWNER MASTER LOGIN
        if (email === "pennabadicharith@gmail.com" && pass === "Cherry1111") {
          this.user = {
            id: "owner_super",
            email: "pennabadicharith@gmail.com",
            username: "Charith (Owner)",
            avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
            roleId: "owner",
            roleName: "Owner",
            roleColor: "#ff6b00",
            permissions: ["all"],
            isOwner: true,
            isLoggedIn: true
          };
          this.save();
          STORE.addLog("login", this.user.username, "Owner Login", "Verified Owner logged in successfully.");
          return { success: true, message: "Welcome back, Game Owner!" };
        }

        // 2. ADMIN LOGIN WITH CUSTOM PASSWORDS & DEVICE LIMITS
        const adm = (STORE.state.admins || []).find(a => (a.email || "").toLowerCase() === email);
        const validPass = adm && (pass === (adm.password || "Admin123!"));

        if (adm && validPass) {
          this.user = {
            id: adm.id,
            email: adm.email,
            username: adm.name || "Administrator",
            avatar: adm.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=128&q=80",
            roleId: "admin",
            roleName: adm.roleName || "Admin",
            roleColor: "#0284c7",
            permissions: adm.permissions || ["cars", "events", "updates", "tyres", "maps", "rules"],
            isOwner: false,
            isLoggedIn: true
          };
          this.save();
          STORE.addLog("login", this.user.username, "Staff Login", `Staff logged in with permissions: ${(adm.permissions||[]).join(', ')}`);
          return { success: true, message: `Welcome back, ${adm.name}!` };
        }

        return { success: false, message: "Invalid email or passphrase. Access denied." };
      }

      logout() {
        sessionStorage.removeItem("RDS_AUTH_USER");
        this.user = this.load();
        this.save();
        renderHubView();
        updateHeaderUserUI();
        showToast("Signed out successfully.");
      }

      hasPerm(p) {
        if (!this.user || !this.user.isLoggedIn) return false;
        if (this.user.isOwner) return true;
        if (!this.user.permissions) return false;
        return this.user.permissions.includes("all") || this.user.permissions.includes(p);
      }
    }

    const AUTH = new AuthEngine();

    /* ==========================================================================
       AUDIO SYNTHESIZER & WORKABLE NOTIFICATIONS
       ========================================================================== */
    class AudioChime {
      constructor() {
        this.ctx = null;
        this.badgeCount = 0;
        this.enabled = localStorage.getItem("RDS_SOUND_ENABLED") !== "false";
      }

      init() {
        try {
          const AC = window.AudioContext || window.webkitAudioContext;
          if (AC && !this.ctx) this.ctx = new AC();
          if (this.ctx && this.ctx.state === "suspended") this.ctx.resume();
        } catch(e) {}
      }

      play(freq = 659.25, dur = 0.35) {
        if (!this.enabled) return;
        try {
          this.init();
          if (!this.ctx) return;
          const now = this.ctx.currentTime;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(freq, now);
          osc.frequency.exponentialRampToValueAtTime(freq * 1.33, now + dur * 0.4);
          gain.gain.setValueAtTime(0.001, now);
          gain.gain.linearRampToValueAtTime(0.18, now + 0.04);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + dur);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start(now);
          osc.stop(now + dur);
        } catch(e) {}
      }

      notify(title, msg) {
        this.play(784, 0.4);
        this.badgeCount++;
        const badge = document.getElementById("header-bell-badge");
        if (badge) {
          badge.textContent = this.badgeCount;
          badge.style.display = "flex";
        }
        showToast(`🔔 ${title}: ${msg}`);
      }
    }

    const AUDIO = new AudioChime();

    /* ==========================================================================
       AMBIENT DYNAMIC LIGHTING & PARTICLES ENGINE
       ========================================================================== */
    class MotionEngine {
      constructor() {
        this.canvas = document.getElementById("bg-motion-canvas");
        this.ctx = null;
        this.particles = [];
        this.running = false;
        this.enabled = localStorage.getItem("RDS_MOTION_ENABLED") !== "false";
      }

      init() {
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext("2d");
        this.resize();
        window.addEventListener("resize", () => this.resize());

        this.particles = [];
        const count = window.innerWidth < 768 ? 24 : 55;
        for (let i = 0; i < count; i++) {
          this.particles.push({
            x: Math.random() * this.canvas.width,
            y: Math.random() * this.canvas.height,
            size: Math.random() * 2.5 + 0.8,
            speedX: (Math.random() - 0.5) * 0.8,
            speedY: -Math.random() * 1.2 - 0.3,
            alpha: Math.random() * 0.6 + 0.2,
            hue: Math.random() > 0.6 ? 24 : 210 // Orange or Slate Blue
          });
        }

        if (this.enabled) this.start();
      }

      resize() {
        if (!this.canvas) return;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
      }

      start() {
        if (this.running) return;
        this.running = true;
        const loop = () => {
          if (!this.running || !this.enabled) return;
          this.render();
          requestAnimationFrame(loop);
        };
        requestAnimationFrame(loop);
      }

      stop() {
        this.running = false;
        if (this.ctx && this.canvas) {
          this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
      }

      render() {
        if (!this.ctx || !this.canvas) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let p of this.particles) {
          p.x += p.speedX;
          p.y += p.speedY;

          if (p.y < -10) {
            p.y = this.canvas.height + 10;
            p.x = Math.random() * this.canvas.width;
          }
          if (p.x < -10) p.x = this.canvas.width + 10;
          if (p.x > this.canvas.width + 10) p.x = -10;

          this.ctx.beginPath();
          this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          this.ctx.fillStyle = `hsla(${p.hue}, 90%, 65%, ${p.alpha})`;
          this.ctx.fill();
        }
      }
    }

    const MOTION = new MotionEngine();
'''
