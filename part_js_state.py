# part_js_state.py - Default Hub State & Store Manager for Real Driving School Portal v1.2.120
import sys
sys.stdout.reconfigure(encoding='utf-8')

JS_STATE_CONTENT = r'''
    /* ==========================================================================
       DEFAULT HUB STATE & INITIAL SEED DATA
       ========================================================================== */
    const DEFAULT_STATE = {
      hubConfig: {
        title: "REAL DRIVING SCHOOL",
        logo: "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=200&q=80",
        about: "Experience the next generation of realistic driving simulation in Real Driving School. Ultra-realistic clutch physics, dynamic weather, custom liveries, multiplayer lobbies, and an expansive open world.",
        bgType: "video",
        bgMediaUrl: "https://assets.mixkit.co/videos/preview/mixkit-sports-car-driving-at-night-41584-large.mp4",
        discordUrl: "https://discord.gg/realdrivingschool",
        instagramUrl: "https://instagram.com/realdrivingschool",
        googlePlayUrl: "https://play.google.com/store/apps/details?id=com.qizz.rds",
        appStoreUrl: "https://apps.apple.com/app/real-driving-school/id1498327827"
      },
      isEditingMode: false,
      cars: [
        {
          id: "car_chiron",
          order: 1,
          name: "Bugatti Chiron Pur Sport",
          image: "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=800&q=80",
          description: "Quad-turbocharged 8.0L W16 apex predator engineered for ultimate lateral grip and acceleration.",
          basePrice: "35M",
          premiumPrice: "10M",
          coatingPrice: "8M",
          policePrice: "20M",
          rainbowPrice: "15M",
          stages: [
            { stage: 1, price: "35M", speedNoTurboKmph: 340, speedNoTurboMph: 211, speedTurboKmph: 375, speedTurboMph: 233 },
            { stage: 2, price: "48M", speedNoTurboKmph: 355, speedNoTurboMph: 221, speedTurboKmph: 395, speedTurboMph: 245 },
            { stage: 3, price: "65M", speedNoTurboKmph: 370, speedNoTurboMph: 230, speedTurboKmph: 415, speedTurboMph: 258 },
            { stage: 4, price: "88M", speedNoTurboKmph: 385, speedNoTurboMph: 239, speedTurboKmph: 435, speedTurboMph: 270 },
            { stage: 5, price: "120M", speedNoTurboKmph: 400, speedNoTurboMph: 248, speedTurboKmph: 455, speedTurboMph: 283 },
            { stage: 6, price: "165M", speedNoTurboKmph: 415, speedNoTurboMph: 258, speedTurboKmph: 475, speedTurboMph: 295 },
            { stage: 7, price: "220M", speedNoTurboKmph: 430, speedNoTurboMph: 267, speedTurboKmph: 495, speedTurboMph: 308 }
          ]
        },
        {
          id: "car_jesko",
          order: 2,
          name: "Koenigsegg Jesko Attack",
          image: "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
          description: "Twin-turbo V8 producing 1600 HP on E85 biofuel with 1400 kg of aerodynamic downforce.",
          basePrice: "40M",
          premiumPrice: "12M",
          coatingPrice: "9M",
          policePrice: "22M",
          rainbowPrice: "16M",
          stages: [
            { stage: 1, price: "40M", speedNoTurboKmph: 350, speedNoTurboMph: 217, speedTurboKmph: 385, speedTurboMph: 239 },
            { stage: 2, price: "55M", speedNoTurboKmph: 368, speedNoTurboMph: 229, speedTurboKmph: 405, speedTurboMph: 252 },
            { stage: 3, price: "75M", speedNoTurboKmph: 385, speedNoTurboMph: 239, speedTurboKmph: 425, speedTurboMph: 264 },
            { stage: 4, price: "100M", speedNoTurboKmph: 400, speedNoTurboMph: 248, speedTurboKmph: 445, speedTurboMph: 276 },
            { stage: 5, price: "135M", speedNoTurboKmph: 415, speedNoTurboMph: 258, speedTurboKmph: 468, speedTurboMph: 291 },
            { stage: 6, price: "180M", speedNoTurboKmph: 430, speedNoTurboMph: 267, speedTurboKmph: 490, speedTurboMph: 304 },
            { stage: 7, price: "240M", speedNoTurboKmph: 445, speedNoTurboMph: 276, speedTurboKmph: 512, speedTurboMph: 318 }
          ]
        },
        {
          id: "car_sf90",
          order: 3,
          name: "Ferrari SF90 Stradale",
          image: "https://images.unsplash.com/photo-1592198084033-aade902d1aae?auto=format&fit=crop&w=800&q=80",
          description: "Hyper hybrid combining a twin-turbo V8 and three electric motors with AWD traction control.",
          basePrice: "28M",
          premiumPrice: "8M",
          coatingPrice: "7M",
          policePrice: "18M",
          rainbowPrice: "12M",
          stages: [
            { stage: 1, price: "28M", speedNoTurboKmph: 320, speedNoTurboMph: 199, speedTurboKmph: 350, speedTurboMph: 217 },
            { stage: 2, price: "38M", speedNoTurboKmph: 335, speedNoTurboMph: 208, speedTurboKmph: 370, speedTurboMph: 230 },
            { stage: 3, price: "52M", speedNoTurboKmph: 350, speedNoTurboMph: 217, speedTurboKmph: 390, speedTurboMph: 242 },
            { stage: 4, price: "70M", speedNoTurboKmph: 365, speedNoTurboMph: 227, speedTurboKmph: 410, speedTurboMph: 255 },
            { stage: 5, price: "95M", speedNoTurboKmph: 380, speedNoTurboMph: 236, speedTurboKmph: 430, speedTurboMph: 267 },
            { stage: 6, price: "130M", speedNoTurboKmph: 395, speedNoTurboMph: 245, speedTurboKmph: 450, speedTurboMph: 280 },
            { stage: 7, price: "175M", speedNoTurboKmph: 410, speedNoTurboMph: 255, speedTurboKmph: 470, speedTurboMph: 292 }
          ]
        },
        {
          id: "car_gt3rs",
          order: 4,
          name: "Porsche 911 GT3 RS",
          image: "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=800&q=80",
          description: "Naturally aspirated 4.0L flat-six with DRS swan-neck rear wing and active aerodynamics.",
          basePrice: "22M",
          premiumPrice: "7M",
          coatingPrice: "6M",
          policePrice: "16M",
          rainbowPrice: "10M",
          stages: [
            { stage: 1, price: "22M", speedNoTurboKmph: 300, speedNoTurboMph: 186, speedTurboKmph: 330, speedTurboMph: 205 },
            { stage: 2, price: "30M", speedNoTurboKmph: 315, speedNoTurboMph: 196, speedTurboKmph: 348, speedTurboMph: 216 },
            { stage: 3, price: "42M", speedNoTurboKmph: 330, speedNoTurboMph: 205, speedTurboKmph: 365, speedTurboMph: 227 },
            { stage: 4, price: "58M", speedNoTurboKmph: 345, speedNoTurboMph: 214, speedTurboKmph: 382, speedTurboMph: 237 },
            { stage: 5, price: "78M", speedNoTurboKmph: 360, speedNoTurboMph: 224, speedTurboKmph: 400, speedTurboMph: 248 },
            { stage: 6, price: "105M", speedNoTurboKmph: 375, speedNoTurboMph: 233, speedTurboKmph: 418, speedTurboMph: 260 },
            { stage: 7, price: "140M", speedNoTurboKmph: 390, speedNoTurboMph: 242, speedTurboKmph: 435, speedTurboMph: 270 }
          ]
        },
        {
          id: "car_aventador",
          order: 5,
          name: "Lamborghini Aventador SVJ",
          image: "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80",
          description: "Naturally aspirated 6.5L V12 delivering 770 HP with ALA 2.0 active aerodynamics vectoring.",
          basePrice: "25M",
          premiumPrice: "8M",
          coatingPrice: "7M",
          policePrice: "18M",
          rainbowPrice: "12M",
          stages: [
            { stage: 1, price: "25M", speedNoTurboKmph: 310, speedNoTurboMph: 193, speedTurboKmph: 340, speedTurboMph: 211 },
            { stage: 2, price: "34M", speedNoTurboKmph: 325, speedNoTurboMph: 202, speedTurboKmph: 358, speedTurboMph: 222 },
            { stage: 3, price: "48M", speedNoTurboKmph: 340, speedNoTurboMph: 211, speedTurboKmph: 378, speedTurboMph: 235 },
            { stage: 4, price: "65M", speedNoTurboKmph: 355, speedNoTurboMph: 221, speedTurboKmph: 398, speedTurboMph: 247 },
            { stage: 5, price: "90M", speedNoTurboKmph: 370, speedNoTurboMph: 230, speedTurboKmph: 418, speedTurboMph: 260 },
            { stage: 6, price: "120M", speedNoTurboKmph: 385, speedNoTurboMph: 239, speedTurboKmph: 438, speedTurboMph: 272 },
            { stage: 7, price: "160M", speedNoTurboKmph: 400, speedNoTurboMph: 248, speedTurboKmph: 458, speedTurboMph: 285 }
          ]
        },
        {
          id: "car_gtr",
          order: 6,
          name: "Nissan GT-R Nismo (R35)",
          image: "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=800&q=80",
          description: "Godzilla VR38DETT twin-turbo V6 with ATTESA E-TS all-wheel drive launch control.",
          basePrice: "16M",
          premiumPrice: "5M",
          coatingPrice: "5M",
          policePrice: "14M",
          rainbowPrice: "9M",
          stages: [
            { stage: 1, price: "16M", speedNoTurboKmph: 290, speedNoTurboMph: 180, speedTurboKmph: 320, speedTurboMph: 199 },
            { stage: 2, price: "22M", speedNoTurboKmph: 305, speedNoTurboMph: 190, speedTurboKmph: 338, speedTurboMph: 210 },
            { stage: 3, price: "31M", speedNoTurboKmph: 320, speedNoTurboMph: 199, speedTurboKmph: 356, speedTurboMph: 221 },
            { stage: 4, price: "44M", speedNoTurboKmph: 335, speedNoTurboMph: 208, speedTurboKmph: 374, speedTurboMph: 232 },
            { stage: 5, price: "60M", speedNoTurboKmph: 350, speedNoTurboMph: 217, speedTurboKmph: 392, speedTurboMph: 244 },
            { stage: 6, price: "82M", speedNoTurboKmph: 365, speedNoTurboMph: 227, speedTurboKmph: 410, speedTurboMph: 255 },
            { stage: 7, price: "110M", speedNoTurboKmph: 380, speedNoTurboMph: 236, speedTurboKmph: 428, speedTurboMph: 266 }
          ]
        }
      ],
      tyres: [
        {
          id: "tyre_grip",
          name: "Tokyo Grip Pro-Spec",
          category: "Track & Circuit",
          code: "RDS-GRIP-99X",
          surface: "Asphalt & Dry Track",
          frictionIndex: "0.98 Lateral G",
          description: "Sticky slick compound providing maximum downforce traction on high-speed hairpins."
        },
        {
          id: "tyre_drift",
          name: "Haruna Smoke Compound",
          category: "Drift & Tandem",
          code: "RDS-DFRT-SMK7",
          surface: "Smooth Tarmac & Docks",
          frictionIndex: "0.42 Breakaway",
          description: "Ultra high smoke density compound engineered for effortless countersteering and tandem entries."
        },
        {
          id: "tyre_drag",
          name: "Nitrous Drag Radial",
          category: "Quarter Mile Drag",
          code: "RDS-DRAG-RAD1",
          surface: "Prep Strip & Highway",
          frictionIndex: "1.12 Launch G",
          description: "Soft wall wrinkle slick engineered for sub-2.0s zero to sixty launches."
        },
        {
          id: "tyre_rally",
          name: "Nordic Snow & Gravel",
          category: "Offroad & Rally",
          code: "RDS-RALLY-ICE4",
          surface: "Snow, Dirt & Mud",
          frictionIndex: "0.85 Mud Traction",
          description: "Deep tread siping with tungsten studs for grip through treacherous mountain conditions."
        }
      ],
      events: [
        {
          id: "event_1",
          title: "Tokyo Midnight Drag Championship",
          image: "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80",
          startTime: new Date(Date.now() - 3600000).toISOString(),
          endTime: new Date(Date.now() + 86400000 * 3).toISOString(),
          location: "Wangan Bayshore Route & Tunnel",
          prizes: "1st: $500M Cash + Pur Sport Carbon Livery | 2nd: $250M | 3rd: $100M",
          isLive: true,
          description: "High speed quarter-mile drag knockouts with no speed limit. Top stage builds allowed."
        },
        {
          id: "event_2",
          title: "Akina Downhill Touge Drift Royale",
          image: "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80",
          startTime: new Date(Date.now() + 86400000 * 5).toISOString(),
          endTime: new Date(Date.now() + 86400000 * 8).toISOString(),
          location: "Mount Akina Five Hairpins",
          prizes: "1st: $350M Cash + Haruna Smoke Title | 2nd: $150M",
          isLive: false,
          description: "Tandem drift battles scored on proximity, angle, and speed. Contact causes elimination."
        }
      ],
      updates: [
        {
          id: "upd_1",
          version: "v1.2.120",
          channel: "public",
          type: "Official Public Release",
          title: "The Ultimate Hypercar Update & Real-Time Portal",
          image: "https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?auto=format&fit=crop&w=800&q=80",
          author: "Charith (Owner)",
          publishedAndroid: true,
          publishedIos: true,
          notes: [
            "Introduced Bugatti Chiron Pur Sport with Stage 1-7 tuning specs.",
            "Complete audio synthesizer sound engine overhaul with realistic blow-off valves.",
            "Live multi-device cloud synchronization powered by Google Firebase ($0 tier).",
            "Added official upgrade options: Rainbow Smoke, Police, Coating & Premium.",
            "Optimized mobile responsive layout with 2-by-2 grid and detached floating dock."
          ]
        },
        {
          id: "upd_2",
          version: "v1.2.125-Beta",
          channel: "beta",
          type: "Official Beta Branch",
          title: "Dynamic Rain Shaders & Manual Clutch Revamp",
          image: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
          author: "Charith (Owner)",
          publishedAndroid: true,
          publishedIos: false,
          notes: [
            "🧪 Beta experimental wet tarmac surface reflections and hydroplaning tire physics.",
            "Added interior cockpit 900-degree steering wheel rotation animation.",
            "Implemented realistic rev matching downshifts for manual gearbox mode.",
            "Optimized multiplayer lobby synchronization tickrate to 60 Hz."
          ]
        }
      ],
      maps: [
        {
          id: "map_wangan",
          title: "Bayshore Wangan Highway",
          tag: "Top Speed & Drag",
          image: "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80",
          description: "Longest continuous asphalt straightaway in RDS. Perfect for testing Stage 7 top speed runs."
        },
        {
          id: "map_akina",
          title: "Mount Haruna (Akina Touge)",
          tag: "Tandem Drift Zone",
          image: "https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?auto=format&fit=crop&w=800&q=80",
          description: "Steep technical downhill mountain pass with 5 consecutive hairpins and guardrail clipping points."
        },
        {
          id: "map_docks",
          title: "Industrial Shipping Docks",
          tag: "Gymkhana Playground",
          image: "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80",
          description: "Sprawling shipping container maze with obstacle jumps, tight donuts, and hidden tunnel entrances."
        }
      ],
      multiplayerGuides: [
        {
          id: "mp_1",
          title: "Lobby Hosting & Zero-Lag Setup",
          content: "Always select the closest geographic server region (Asia / Europe / US West). Ensure background downloads are paused. Keep lobby limit to 16 players for smooth 60 FPS physics synchronization."
        },
        {
          id: "mp_2",
          title: "Official Clan Etiquette & Drag Lines",
          content: "When lining up at the drag strip, flash headlights twice to initiate race countdown. No false starts or cutting lanes. Ramming results in an immediate 48-hour clan blacklist."
        }
      ],
      rules: [
        {
          id: "rule_1",
          title: "Fair Play & Anti-Griefing Policy",
          content: "Intentional pit maneuvering, blocking race lines, or ghost ramming in cruise rooms is strictly prohibited. Violators face temporary or permanent room bans."
        },
        {
          id: "rule_2",
          title: "Vehicle Economy & Safe Trading",
          content: "Never send in-game cash or vehicle pink slips without verified in-person confirmation. Always check the official Car Valuation Index on this portal before trading."
        },
        {
          id: "rule_3",
          title: "Community Respect & Clan Conduct",
          content: "Hate speech, harassment, impersonation of staff or owners, and exploit spreading will result in an immediate game ID ban."
        }
      ],
      customCategories: [],
      admins: [
        {
          id: "adm_owner",
          name: "Charith (Owner)",
          email: "pennabadicharith@gmail.com",
          password: "Cherry1111",
          deviceLimit: 5,
          activeLogins: 1,
          permissions: ["all"],
          roleName: "Owner"
        }
      ],
      roles: [
        { id: "owner", name: "Owner", color: "#ff6b00", perms: ["all"] },
        { id: "admin", name: "Administrator", color: "#0284c7", perms: ["cars", "events", "updates", "tyres", "maps", "rules"] },
        { id: "moderator", name: "Moderator", color: "#16a34a", perms: ["events", "rules"] },
        { id: "player", name: "Driver", color: "#64748b", perms: [] }
      ],
      auditLogs: []
    };

    /* ==========================================================================
       CENTRAL STATE STORE WITH MULTI-DOCUMENT SYNC
       ========================================================================== */
    class Store {
      constructor() {
        this.state = this.loadLocal();
        this.activeOnlineDrivers = [];
      }

      loadLocal() {
        const local = localStorage.getItem("RDS_PORTAL_STATE_MASTER");
        if (local) {
          try {
            const parsed = JSON.parse(local);
            return {
              ...DEFAULT_STATE,
              ...parsed,
              hubConfig: { ...DEFAULT_STATE.hubConfig, ...(parsed.hubConfig || {}) }
            };
          } catch(e) {}
        }
        return JSON.parse(JSON.stringify(DEFAULT_STATE));
      }

      saveLocal() {
        localStorage.setItem("RDS_PORTAL_STATE_MASTER", JSON.stringify(this.state));
      }

      // Sync specific collection to Firestore document
      async syncCollection(collectionName) {
        this.saveLocal();
        if (FIREBASE && FIREBASE.connected) {
          const payload = {};
          if (collectionName === "config") {
            Object.assign(payload, this.state.hubConfig);
          } else if (collectionName === "cars") {
            payload.items = this.state.cars;
          } else if (collectionName === "events") {
            payload.items = this.state.events;
          } else if (collectionName === "updates") {
            payload.items = this.state.updates;
          } else if (collectionName === "tyres") {
            payload.items = this.state.tyres;
          } else if (collectionName === "maps") {
            payload.items = this.state.maps;
          } else if (collectionName === "rules") {
            payload.items = this.state.rules;
          } else if (collectionName === "multiplayer") {
            payload.items = this.state.multiplayerGuides;
          } else if (collectionName === "admins") {
            payload.items = this.state.admins;
          } else if (collectionName === "roles") {
            payload.items = this.state.roles;
          } else if (collectionName === "custom_cats") {
            payload.items = this.state.customCategories;
          } else if (collectionName === "logs") {
            payload.items = this.state.auditLogs;
          }
          await FIREBASE.syncDoc(collectionName, payload);
        }
      }

      addLog(category, user, action, details) {
        if (!this.state.auditLogs) this.state.auditLogs = [];
        this.state.auditLogs.unshift({
          id: "log_" + Date.now(),
          category,
          user: user || (AUTH.user ? AUTH.user.username : "Driver"),
          action,
          details,
          timestamp: new Date().toISOString()
        });
        if (this.state.auditLogs.length > 50) this.state.auditLogs.pop();
        this.syncCollection("logs");
      }
    }

    const STORE = new Store();
'''
