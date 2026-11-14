require('dotenv').config();
const fs = require('fs');
const path = require('path');
const http = require('http');
const {
  Client,
  GatewayIntentBits,
  REST,
  Routes,
  SlashCommandBuilder,
  EmbedBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  ModalBuilder,
  TextInputBuilder,
  TextInputStyle,
  MessageFlags
} = require('discord.js');

// Optional Mongoose load (only used if MONGO_URI is set in .env)
let mongoose = null;
try {
  mongoose = require('mongoose');
} catch (err) {
  // Mongoose is optional when using Built-in JSON DB or Google Firebase DB
}

// ==========================================
// 0. 24/7 KEEP-ALIVE SERVER (FOR FREE HOSTS)
// ==========================================
const PORT = process.env.PORT || 3000;
http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('RDS Car Bot is Online 24/7!');
}).listen(PORT, () => {
  console.log(`🌐 24/7 Keep-Alive HTTP Server listening on port ${PORT}`);
});

// ==========================================
// 1. CONFIGURATION & CONSTANTS
// ==========================================
const OWNER_USERNAME = (process.env.OWNER_USERNAME || 'hyper_legend_1_og').toLowerCase();
const LOCAL_DB_FILE = path.join(__dirname, 'database.json');

const RDS_DISCLAIMER = [
  '**FYI:** These prices are approximate and not based on real-time pricing and serve as a guide if any **Car Dealer** is absent. This section will be subject to updates periodically.',
  '',
  '__**Coating Prices**__',
  '• Varies on what car it\'s applied on.',
  '• **Low-Mid End Cars:** Coating adds **30m–35m** of value.',
  '• **High End Cars:** Coating adds **25m–30m** of value.',
  '• **Additional Note:** If a car is hard to find with coating, the coating cost can exceed **30m** and go well into **40m+**.'
].join('\n');

// ==========================================
// 2. UNIVERSAL 24/7 DATABASE ENGINE
// Supports:
//   1. Built-in Local Database (database.json) -> 0 setup, 100% Free, Never expires!
//   2. Google Firebase Realtime DB (FIREBASE_DB_URL) -> 100% Free 24/7 Cloud DB, No renewals ever!
//   3. MongoDB Atlas (MONGO_URI) -> Optional if you still want MongoDB
// ==========================================
let dbMode = 'json'; // 'json' | 'firebase' | 'mongo'
let CarModel = null;
let StaffModel = null;

// Local cache synced with database.json and/or Firebase
let memoryStore = {
  cars: [],
  staff: []
};

function loadLocalJsonDb() {
  try {
    if (fs.existsSync(LOCAL_DB_FILE)) {
      const raw = fs.readFileSync(LOCAL_DB_FILE, 'utf8');
      const parsed = JSON.parse(raw);
      memoryStore.cars = Array.isArray(parsed.cars) ? parsed.cars : [];
      memoryStore.staff = Array.isArray(parsed.staff) ? parsed.staff : [];
    } else {
      fs.writeFileSync(LOCAL_DB_FILE, JSON.stringify(memoryStore, null, 2), 'utf8');
    }
  } catch (err) {
    console.error('⚠️ Error reading database.json, initializing fresh store:', err.message);
  }
}

function saveLocalJsonDb() {
  try {
    fs.writeFileSync(LOCAL_DB_FILE, JSON.stringify(memoryStore, null, 2), 'utf8');
  } catch (err) {
    console.error('⚠️ Error saving database.json:', err.message);
  }
}

async function syncFromFirebase() {
  if (!process.env.FIREBASE_DB_URL) return;
  const baseUrl = process.env.FIREBASE_DB_URL.replace(/\/$/, '');
  const secretParam = process.env.FIREBASE_SECRET ? `?auth=${process.env.FIREBASE_SECRET}` : '';
  const res = await fetch(`${baseUrl}/rds_bot.json${secretParam}`);
  if (!res.ok) throw new Error(`Firebase HTTP ${res.status}`);
  const data = await res.json();
  if (data) {
    memoryStore.cars = Array.isArray(data.cars) ? data.cars : Object.values(data.cars || {});
    memoryStore.staff = Array.isArray(data.staff) ? data.staff : Object.values(data.staff || {});
    saveLocalJsonDb();
  }
}

async function syncToFirebase() {
  saveLocalJsonDb(); // Always keep local backup too
  if (dbMode !== 'firebase' || !process.env.FIREBASE_DB_URL) return;
  try {
    const baseUrl = process.env.FIREBASE_DB_URL.replace(/\/$/, '');
    const secretParam = process.env.FIREBASE_SECRET ? `?auth=${process.env.FIREBASE_SECRET}` : '';
    await fetch(`${baseUrl}/rds_bot.json${secretParam}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(memoryStore)
    });
  } catch (err) {
    console.error('⚠️ Firebase cloud sync warning (saved locally):', err.message);
  }
}

async function initDatabase() {
  loadLocalJsonDb();

  // Priority 1: Google Firebase Realtime Database (24/7 Free Forever, HTTPS port 443 - never blocked!)
  if (process.env.FIREBASE_DB_URL && process.env.FIREBASE_DB_URL.startsWith('http')) {
    try {
      console.log('🔄 Connecting to Google Firebase Realtime Database...');
      await syncFromFirebase();
      dbMode = 'firebase';
      console.log('✅ Connected to Google Firebase Realtime Database (with local backup)!');
      return;
    } catch (err) {
      console.warn('⚠️ Firebase connection failed, falling back to Built-in Local Database:', err.message);
    }
  }

  // Priority 2: MongoDB (if MONGO_URI is set and valid)
  if (process.env.MONGO_URI && process.env.MONGO_URI.startsWith('mongodb') && mongoose) {
    try {
      console.log('🔄 Connecting to MongoDB...');
      const StageSchema = new mongoose.Schema({
        priceRaw: { type: String, default: '0' },
        priceMin: { type: Number, default: 0 },
        priceMax: { type: Number, default: 0 },
        isPlus: { type: Boolean, default: false },
        noTurboMph: { type: String, default: 'N/A' },
        noTurboKph: { type: String, default: 'N/A' },
        withTurboMph: { type: String, default: 'N/A' },
        withTurboKph: { type: String, default: 'N/A' }
      }, { _id: false });

      const PriceRangeSchema = new mongoose.Schema({
        raw: { type: String, default: '0' },
        min: { type: Number, default: 0 },
        max: { type: Number, default: 0 },
        isPlus: { type: Boolean, default: false }
      }, { _id: false });

      const CarSchema = new mongoose.Schema({
        name: { type: String, required: true, unique: true },
        nameLower: { type: String, required: true, index: true },
        imageUrl: { type: String, default: '' },
        addons: {
          police: { type: PriceRangeSchema, default: () => ({}) },
          rainbowSmoke: { type: PriceRangeSchema, default: () => ({}) },
          premium: { type: PriceRangeSchema, default: () => ({}) },
          coating: { type: PriceRangeSchema, default: () => ({}) }
        },
        stages: {
          stage1: { type: StageSchema, default: () => ({}) },
          stage2: { type: StageSchema, default: () => ({}) },
          stage3: { type: StageSchema, default: () => ({}) },
          stage4: { type: StageSchema, default: () => ({}) },
          stage5: { type: StageSchema, default: () => ({}) },
          stage6: { type: StageSchema, default: () => ({}) },
          stage7: { type: StageSchema, default: () => ({}) }
        },
        updatedBy: { type: String, default: '' },
        updatedAt: { type: Date, default: Date.now }
      });

      const StaffSchema = new mongoose.Schema({
        userId: { type: String, required: true, unique: true },
        username: { type: String, required: true },
        role: { type: String, enum: ['admin', 'mod'], required: true },
        addedBy: { type: String, default: '' },
        addedAt: { type: Date, default: Date.now }
      });

      CarModel = mongoose.models.Car || mongoose.model('Car', CarSchema);
      StaffModel = mongoose.models.Staff || mongoose.model('Staff', StaffSchema);

      await mongoose.connect(process.env.MONGO_URI, { serverSelectionTimeoutMS: 7000 });
      dbMode = 'mongo';
      console.log('✅ Connected to MongoDB successfully!');
      return;
    } catch (err) {
      console.warn('⚠️ MongoDB connection failed, automatically switching to Built-in Local Database (database.json):', err.message);
    }
  }

  // Priority 3: Built-in 24/7 Local JSON Database (Zero external setup required!)
  dbMode = 'json';
  console.log('✅ Using Built-in 24/7 Persistent Database (database.json) — No external database setup required!');
}

// Unified Database Operations (Works identically across JSON, Firebase, and MongoDB)
const DB = {
  async getStaffByUserId(userId) {
    if (dbMode === 'mongo') return await StaffModel.findOne({ userId }).lean();
    return memoryStore.staff.find(s => s.userId === userId) || null;
  },

  async upsertStaff(userId, username, role, addedBy) {
    if (dbMode === 'mongo') {
      return await StaffModel.findOneAndUpdate(
        { userId },
        { userId, username, role, addedBy, addedAt: new Date() },
        { upsert: true, new: true }
      ).lean();
    }
    const existingIdx = memoryStore.staff.findIndex(s => s.userId === userId);
    const record = { userId, username, role, addedBy, addedAt: new Date().toISOString() };
    if (existingIdx >= 0) {
      memoryStore.staff[existingIdx] = record;
    } else {
      memoryStore.staff.push(record);
    }
    await syncToFirebase();
    return record;
  },

  async removeStaff(userId, role) {
    if (dbMode === 'mongo') {
      return await StaffModel.deleteOne({ userId, role });
    }
    memoryStore.staff = memoryStore.staff.filter(s => !(s.userId === userId && s.role === role));
    await syncToFirebase();
  },

  async getAllStaff() {
    if (dbMode === 'mongo') return await StaffModel.find().lean();
    return [...memoryStore.staff];
  },

  async countCars() {
    if (dbMode === 'mongo') return await CarModel.countDocuments();
    return memoryStore.cars.length;
  },

  async searchCarsAutocomplete(focusedValue) {
    if (dbMode === 'mongo') {
      let query = {};
      if (focusedValue.length > 0) {
        const escaped = focusedValue.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        query = { nameLower: { $regex: escaped, $options: 'i' } };
      }
      return await CarModel.find(query).sort({ name: 1 }).limit(25).lean();
    }
    const q = focusedValue.toLowerCase();
    return memoryStore.cars
      .filter(c => !q || c.nameLower.includes(q))
      .sort((a, b) => a.name.localeCompare(b.name))
      .slice(0, 25);
  },

  async findCarByName(carQuery) {
    const lower = carQuery.toLowerCase().trim();
    if (dbMode === 'mongo') {
      const escaped = carQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      return await CarModel.findOne({
        $or: [
          { nameLower: lower },
          { nameLower: { $regex: escaped, $options: 'i' } }
        ]
      }).lean();
    }
    // Exact match first, then partial match
    return (
      memoryStore.cars.find(c => c.nameLower === lower) ||
      memoryStore.cars.find(c => c.nameLower.includes(lower)) ||
      null
    );
  },

  async saveCar(lookupNameLower, carPayload) {
    if (dbMode === 'mongo') {
      return await CarModel.findOneAndUpdate(
        { nameLower: lookupNameLower || carPayload.nameLower },
        carPayload,
        { upsert: true, new: true }
      ).lean();
    }
    const targetLower = lookupNameLower || carPayload.nameLower;
    const idx = memoryStore.cars.findIndex(c => c.nameLower === targetLower);
    const record = {
      _id: idx >= 0 ? memoryStore.cars[idx]._id : `car_${Date.now()}`,
      ...carPayload
    };
    if (idx >= 0) {
      memoryStore.cars[idx] = record;
    } else {
      memoryStore.cars.push(record);
    }
    await syncToFirebase();
    return record;
  },

  async deleteCarByIdOrName(identifier) {
    if (dbMode === 'mongo') {
      return await CarModel.findByIdAndDelete(identifier).lean();
    }
    const idx = memoryStore.cars.findIndex(
      c => String(c._id) === String(identifier) || c.nameLower === String(identifier).toLowerCase()
    );
    if (idx === -1) return null;
    const [deleted] = memoryStore.cars.splice(idx, 1);
    await syncToFirebase();
    return deleted;
  }
};

// In-memory state for active wizards and price calculators
const adminSessions = new Map();
const calcSessions = new Map();

// ==========================================
// 3. SMART NUMBER PARSER & FORMATTERS
// ==========================================
/**
 * Smartly parses inputs like:
 * - "400-550" -> 400,000,000 to 550,000,000 (Auto-Millions)
 * - "30.3-83.5" -> 30,300,000 to 83,500,000 (Auto-Millions)
 * - "10-15m" -> 10,000,000 to 15,000,000
 * - "850+" -> 850,000,000+
 * - "$92,500" or "92500" -> 92,500 (Exact Dollar value for numbers >= 10,000 without 'm')
 */
function parseSmartPrice(inputStr) {
  if (!inputStr || typeof inputStr !== 'string') {
    return { raw: '0', min: 0, max: 0, isPlus: false };
  }

  const cleaned = inputStr.trim().replace(/\$/g, '').replace(/,/g, '');
  if (!cleaned || cleaned === '0' || cleaned.toLowerCase() === 'no' || cleaned.toLowerCase() === 'none') {
    return { raw: '0', min: 0, max: 0, isPlus: false };
  }

  const isPlus = cleaned.includes('+');
  const normalized = cleaned.replace(/\+/g, '').replace(/~/g, '-');
  const parts = normalized.split('-').map(s => s.trim()).filter(Boolean);

  const convertSingleValue = (valStr) => {
    const lower = valStr.toLowerCase();
    let multiplier = 1;

    if (lower.endsWith('b')) {
      multiplier = 1_000_000_000;
    } else if (lower.endsWith('m')) {
      multiplier = 1_000_000;
    } else if (lower.endsWith('k')) {
      multiplier = 1_000;
    }

    const num = parseFloat(lower.replace(/[a-z]/g, ''));
    if (isNaN(num) || num <= 0) return 0;

    // If no suffix was typed, apply the Auto-Million rule for numbers < 10,000 (e.g., 400-550, 30.3-83.5, 2.5-3)
    if (multiplier === 1 && num > 0 && num < 10000) {
      multiplier = 1_000_000;
    }

    return Math.round(num * multiplier);
  };

  if (parts.length === 1) {
    const val = convertSingleValue(parts[0]);
    return { raw: inputStr.trim(), min: val, max: val, isPlus };
  } else {
    const minVal = convertSingleValue(parts[0]);
    const maxVal = convertSingleValue(parts[1]);
    return {
      raw: inputStr.trim(),
      min: Math.min(minVal, maxVal),
      max: Math.max(minVal, maxVal),
      isPlus
    };
  }
}

function formatFullCurrency(num) {
  return '$' + Math.round(num).toLocaleString('en-US');
}

function formatPriceRange(min, max, isPlus = false, includeEstimatedText = true) {
  if ((!min || min <= 0) && (!max || max <= 0)) return 'N/A';
  const estSuffix = includeEstimatedText ? ' *(Estimated)*' : '';

  if (min === max) {
    return `${formatFullCurrency(min)}${isPlus ? '+' : ''}${estSuffix}`;
  }
  return `${formatFullCurrency(min)} ~ ${formatFullCurrency(max)}${isPlus ? '+' : ''}${estSuffix}`;
}

// ==========================================
// 4. PERMISSION HELPERS
// ==========================================
async function getUserRole(user) {
  if (user.username.toLowerCase() === OWNER_USERNAME) {
    return 'owner';
  }
  const staffRecord = await DB.getStaffByUserId(user.id);
  if (!staffRecord) return null;
  return staffRecord.role; // 'admin' or 'mod'
}

// ==========================================
// 5. SLASH COMMAND DEFINITIONS
// ==========================================
const commands = [
  new SlashCommandBuilder()
    .setName('admin-cars')
    .setDescription('Open the Car Management Panel (Add, Edit, or Delete cars - Staff Only)'),

  new SlashCommandBuilder()
    .setName('admin-add')
    .setDescription('Add or remove an Admin (Owner hyper_legend_1_og only)')
    .addUserOption(opt =>
      opt.setName('user').setDescription('Select the user').setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName('action')
        .setDescription('Add or Remove Admin')
        .setRequired(true)
        .addChoices(
          { name: 'Add Admin', value: 'add' },
          { name: 'Remove Admin', value: 'remove' }
        )
    ),

  new SlashCommandBuilder()
    .setName('mod-add')
    .setDescription('Add or remove a Moderator who can add/edit cars (Owner & Admins only)')
    .addUserOption(opt =>
      opt.setName('user').setDescription('Select the user').setRequired(true)
    )
    .addStringOption(opt =>
      opt.setName('action')
        .setDescription('Add or Remove Moderator')
        .setRequired(true)
        .addChoices(
          { name: 'Add Moderator', value: 'add' },
          { name: 'Remove Moderator', value: 'remove' }
        )
    ),

  new SlashCommandBuilder()
    .setName('staff-list')
    .setDescription('View all current Bot Owner, Admins, and Moderators'),

  new SlashCommandBuilder()
    .setName('car-info')
    .setDescription('Check full speed, stage breakdown, and estimated price info for a car')
    .addStringOption(opt =>
      opt.setName('car')
        .setDescription('Start typing the car name (e.g., tyc) to search')
        .setRequired(true)
        .setAutocomplete(true)
    ),

  new SlashCommandBuilder()
    .setName('car-price')
    .setDescription('Interactive Car Price Calculator with Add-ons, Livery, Turbo & Stage options')
    .addStringOption(opt =>
      opt.setName('car')
        .setDescription('Start typing the car name (e.g., tyc) to search')
        .setRequired(true)
        .setAutocomplete(true)
    )
].map(cmd => cmd.toJSON());

// ==========================================
// 6. UI BUILDERS (WIZARDS, EMBEDS, PANELS)
// ==========================================

// Builds the progress panel for the Add/Edit Car Wizard
function buildWizardProgressPayload(session, stageSavedMessage = '') {
  const car = session.data;
  const embed = new EmbedBuilder()
    .setColor(0x5865F2)
    .setTitle(`🛠️ ${session.mode === 'add' ? 'Adding New Car' : 'Editing Car'}: ${car.name || 'Unnamed'}`)
    .setDescription(
      [
        stageSavedMessage ? `✅ **${stageSavedMessage}**\n` : '',
        `**Car Name:** ${car.name || 'Not set'}`,
        `**Image URL:** ${car.imageUrl ? '[Image Link Set](' + car.imageUrl + ')' : 'Not set'}`,
        '',
        '**Add-on Prices:**',
        `• **Police (Cop):** ${formatPriceRange(car.addons.police.min, car.addons.police.max, car.addons.police.isPlus, false)}`,
        `• **Rainbow Smoke:** ${formatPriceRange(car.addons.rainbowSmoke.min, car.addons.rainbowSmoke.max, car.addons.rainbowSmoke.isPlus, false)}`,
        `• **Premium:** ${formatPriceRange(car.addons.premium.min, car.addons.premium.max, car.addons.premium.isPlus, false)}`,
        `• **Coating:** ${formatPriceRange(car.addons.coating.min, car.addons.coating.max, car.addons.coating.isPlus, false)}`,
        '',
        '**Stages Configured:**',
        ...[1, 2, 3, 4, 5, 6].map(num => {
          const st = car.stages[`stage${num}`];
          const pText = formatPriceRange(st.priceMin, st.priceMax, st.isPlus, false);
          return `• **Stage ${num}:** ${pText} | No Turbo: ${st.noTurboMph}mph/${st.noTurboKph}kph | Turbo: ${st.withTurboMph}mph/${st.withTurboKph}kph`;
        }),
        `• **Stage 7 (Price Only):** ${formatPriceRange(car.stages.stage7.priceMin, car.stages.stage7.priceMax, car.stages.stage7.isPlus, false)}`
      ].join('\n')
    )
    .setFooter({ text: 'Click the highlighted Next button below to continue, or jump to any section.' });

  if (car.imageUrl && car.imageUrl.startsWith('http')) {
    embed.setThumbnail(car.imageUrl);
  }

  const nextStepLabelMap = {
    addons: 'Next: Add-on Prices ➡',
    stage1: 'Next: Stage 1 (Speed & Price) ➡',
    stage2: 'Next: Stage 2 (Speed & Price) ➡',
    stage3: 'Next: Stage 3 (Speed & Price) ➡',
    stage4: 'Next: Stage 4 (Speed & Price) ➡',
    stage5: 'Next: Stage 5 (Speed & Price) ➡',
    stage6: 'Next: Stage 6 (Speed & Price) ➡',
    stage7: 'Next: Stage 7 (Price Only) ➡',
    finish: '✅ Save & Publish Car'
  };

  const primaryRow = new ActionRowBuilder();

  if (session.nextStep !== 'finish') {
    primaryRow.addComponents(
      new ButtonBuilder()
        .setCustomId(`wiz_step_${session.nextStep}`)
        .setLabel(nextStepLabelMap[session.nextStep] || 'Next ➡')
        .setStyle(ButtonStyle.Primary)
    );
  }

  primaryRow.addComponents(
    new ButtonBuilder()
      .setCustomId('wiz_save_finish')
      .setLabel('💾 Save & Finish Now')
      .setStyle(ButtonStyle.Success),
    new ButtonBuilder()
      .setCustomId('wiz_step_basic')
      .setLabel('Edit Name/Image')
      .setStyle(ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId('wiz_step_addons')
      .setLabel('Edit Add-ons')
      .setStyle(ButtonStyle.Secondary)
  );

  const stageRow1 = new ActionRowBuilder().addComponents(
    [1, 2, 3, 4].map(n =>
      new ButtonBuilder()
        .setCustomId(`wiz_step_stage${n}`)
        .setLabel(`Stage ${n}`)
        .setStyle(session.nextStep === `stage${n}` ? ButtonStyle.Primary : ButtonStyle.Secondary)
    )
  );

  const stageRow2 = new ActionRowBuilder().addComponents(
    [5, 6, 7].map(n =>
      new ButtonBuilder()
        .setCustomId(`wiz_step_stage${n}`)
        .setLabel(`Stage ${n}`)
        .setStyle(session.nextStep === `stage${n}` ? ButtonStyle.Primary : ButtonStyle.Secondary)
    )
  );

  return { embeds: [embed], components: [primaryRow, stageRow1, stageRow2] };
}

// Builds the Public Car Info Embed (/car-info)
function buildCarInfoEmbed(car) {
  const embed = new EmbedBuilder()
    .setColor(0x00B0F4)
    .setTitle(`🏎️ ${car.name.toUpperCase()} — CAR INFORMATION & ESTIMATED PRICES`)
    .setDescription('*Estimated prices for every car in RDS.*');

  const speedLines = [];
  for (let i = 1; i <= 6; i++) {
    const st = car.stages[`stage${i}`];
    if (st && (st.noTurboMph !== 'N/A' || st.withTurboMph !== 'N/A')) {
      speedLines.push(
        `**Stage ${i}:**\n` +
        `Top Speed (No Turbo): **${st.noTurboMph}mph / ${st.noTurboKph}kph**\n` +
        `Top Speed (With Turbo): **${st.withTurboMph}mph / ${st.withTurboKph}kph**`
      );
    }
  }

  embed.addFields({
    name: '⚡ Stage Top Speeds (MPH / KPH)',
    value: speedLines.length > 0 ? speedLines.join('\n\n') : 'No stage speeds recorded yet.',
    inline: false
  });

  const priceLines = [];
  for (let i = 1; i <= 7; i++) {
    const st = car.stages[`stage${i}`];
    if (st && (st.priceMin > 0 || st.priceMax > 0)) {
      priceLines.push(`**Stage ${i}:** ${formatPriceRange(st.priceMin, st.priceMax, st.isPlus, true)}`);
    }
  }

  embed.addFields({
    name: '💰 Stage Estimated Prices',
    value: priceLines.length > 0 ? priceLines.join('\n') : 'No stage prices recorded yet.',
    inline: false
  });

  const addonLines = [
    `**+ Prem (Premium):** ${formatPriceRange(car.addons.premium.min, car.addons.premium.max, car.addons.premium.isPlus, false)}`,
    `**+ Coating:** ${formatPriceRange(car.addons.coating.min, car.addons.coating.max, car.addons.coating.isPlus, false)}`,
    `**+ Cop (Police):** ${formatPriceRange(car.addons.police.min, car.addons.police.max, car.addons.police.isPlus, false)}`,
    `**+ RB (Rainbow Smoke):** ${formatPriceRange(car.addons.rainbowSmoke.min, car.addons.rainbowSmoke.max, car.addons.rainbowSmoke.isPlus, false)}`
  ];

  embed.addFields({
    name: '✨ Add-On Values',
    value: addonLines.join('\n'),
    inline: false
  });

  embed.addFields({
    name: '📌 Important RDS Notes & Coating Guide',
    value: RDS_DISCLAIMER,
    inline: false
  });

  if (car.imageUrl && car.imageUrl.startsWith('http')) {
    embed.setImage(car.imageUrl);
  }

  embed.setFooter({ text: 'RDS Community Car Database • Prices are Estimated' });
  embed.setTimestamp();

  return embed;
}

// Builds the Interactive Calculator Question Panel (/car-price)
function buildCalculatorPanel(session) {
  const car = session.car;
  const embed = new EmbedBuilder()
    .setColor(0x2B2D31)
    .setTitle(`🧮 Car Price Calculator — ${car.name}`)
    .setDescription(
      [
        'Configure your car options below from top to bottom.',
        '• **Red (NO)** = Not included | **Green (YES)** = Included',
        '• **Default:** `NO` for all add-ons, and **`MAX (Stage 6)`** for Car Upgrade.',
        '',
        `1️⃣ **Premium:** ${session.premium ? '🟢 YES' : '🔴 NO'}`,
        `2️⃣ **Police (Cop):** ${session.police ? '🟢 YES' : '🔴 NO'}`,
        `3️⃣ **Rainbow Smoke (RB):** ${session.rainbowSmoke ? '🟢 YES' : '🔴 NO'}`,
        `4️⃣ **Coating:** ${session.coating ? '🟢 YES' : '🔴 NO'}`,
        `5️⃣ **Livery:** ${session.livery ? `🟢 YES (${formatPriceRange(session.liveryMin, session.liveryMax, false, false)})` : '🔴 NO'}`,
        `6️⃣ **Turbo Installed:** ${session.turbo ? '🟢 YES (With Turbo)' : '🔴 NO (No Turbo)'}`,
        `7️⃣ **Car Condition / Upgrade:** 🟢 **${session.upgrade.toUpperCase()}** ${session.upgrade === 'max' ? '(Stage 6)' : session.upgrade === 'stock' ? '(Stage 1)' : '(Stage 7)'}`
      ].join('\n')
    )
    .setFooter({ text: 'Click "✅ Generate Estimated Price" at the bottom when ready!' });

  if (car.imageUrl && car.imageUrl.startsWith('http')) {
    embed.setThumbnail(car.imageUrl);
  }

  const row1 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('calc_toggle_premium')
      .setLabel(`Premium: ${session.premium ? 'YES' : 'NO'}`)
      .setStyle(session.premium ? ButtonStyle.Success : ButtonStyle.Danger),
    new ButtonBuilder()
      .setCustomId('calc_toggle_police')
      .setLabel(`Police: ${session.police ? 'YES' : 'NO'}`)
      .setStyle(session.police ? ButtonStyle.Success : ButtonStyle.Danger),
    new ButtonBuilder()
      .setCustomId('calc_toggle_rb')
      .setLabel(`Rainbow Smoke: ${session.rainbowSmoke ? 'YES' : 'NO'}`)
      .setStyle(session.rainbowSmoke ? ButtonStyle.Success : ButtonStyle.Danger)
  );

  const row2 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('calc_toggle_coating')
      .setLabel(`Coating: ${session.coating ? 'YES' : 'NO'}`)
      .setStyle(session.coating ? ButtonStyle.Success : ButtonStyle.Danger),
    new ButtonBuilder()
      .setCustomId('calc_toggle_livery')
      .setLabel(session.livery ? `Livery: YES (${session.liveryRaw})` : 'Livery: NO (Click if Yes)')
      .setStyle(session.livery ? ButtonStyle.Success : ButtonStyle.Danger)
  );

  const row3 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('calc_toggle_turbo')
      .setLabel(`Car Turbo: ${session.turbo ? 'YES (With Turbo)' : 'NO (No Turbo)'}`)
      .setStyle(session.turbo ? ButtonStyle.Success : ButtonStyle.Danger)
  );

  const row4 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('calc_upgrade_max')
      .setLabel('Car: MAX (Stage 6) [Default]')
      .setStyle(session.upgrade === 'max' ? ButtonStyle.Success : ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId('calc_upgrade_stock')
      .setLabel('Car: STOCK (Stage 1)')
      .setStyle(session.upgrade === 'stock' ? ButtonStyle.Success : ButtonStyle.Secondary)
  );

  if (car.stages.stage7 && (car.stages.stage7.priceMin > 0 || car.stages.stage7.priceMax > 0)) {
    row4.addComponents(
      new ButtonBuilder()
        .setCustomId('calc_upgrade_stage7')
        .setLabel('Car: STAGE 7')
        .setStyle(session.upgrade === 'stage7' ? ButtonStyle.Success : ButtonStyle.Secondary)
    );
  }

  const row5 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('calc_generate_final')
      .setLabel('✅ Generate Estimated Price (Public)')
      .setStyle(ButtonStyle.Primary)
  );

  return { embeds: [embed], components: [row1, row2, row3, row4, row5] };
}

// Builds the Final Generated Car Price Result Embed (Public)
function buildFinalPriceEmbed(session, requestedByUser) {
  const car = session.car;

  const stageKey = session.upgrade === 'stock' ? 'stage1' : session.upgrade === 'stage7' ? 'stage7' : 'stage6';
  const stageLabel = session.upgrade === 'stock' ? 'STOCK (Stage 1)' : session.upgrade === 'stage7' ? 'STAGE 7' : 'MAX (Stage 6)';
  const selectedStage = car.stages[stageKey] || car.stages.stage6;

  const speedStage = stageKey === 'stage7' ? car.stages.stage6 : selectedStage;
  const speedText = session.turbo
    ? `**${speedStage.withTurboMph}mph / ${speedStage.withTurboKph}kph** *(With Turbo)*`
    : `**${speedStage.noTurboMph}mph / ${speedStage.noTurboKph}kph** *(No Turbo)*`;

  let totalMin = selectedStage.priceMin || 0;
  let totalMax = selectedStage.priceMax || 0;
  let isPlus = Boolean(selectedStage.isPlus);

  const basePriceFormatted = formatPriceRange(selectedStage.priceMin, selectedStage.priceMax, selectedStage.isPlus, true);

  const addedLines = [];

  if (session.premium) {
    totalMin += car.addons.premium.min || 0;
    totalMax += car.addons.premium.max || 0;
    addedLines.push(`🟢 **+ Premium:** ${formatPriceRange(car.addons.premium.min, car.addons.premium.max, car.addons.premium.isPlus, false)}`);
  } else {
    addedLines.push('🔴 **Premium:** No');
  }

  if (session.police) {
    totalMin += car.addons.police.min || 0;
    totalMax += car.addons.police.max || 0;
    addedLines.push(`🟢 **+ Police (Cop):** ${formatPriceRange(car.addons.police.min, car.addons.police.max, car.addons.police.isPlus, false)}`);
  } else {
    addedLines.push('🔴 **Police (Cop):** No');
  }

  if (session.rainbowSmoke) {
    totalMin += car.addons.rainbowSmoke.min || 0;
    totalMax += car.addons.rainbowSmoke.max || 0;
    addedLines.push(`🟢 **+ Rainbow Smoke (RB):** ${formatPriceRange(car.addons.rainbowSmoke.min, car.addons.rainbowSmoke.max, car.addons.rainbowSmoke.isPlus, false)}`);
  } else {
    addedLines.push('🔴 **Rainbow Smoke (RB):** No');
  }

  if (session.coating) {
    totalMin += car.addons.coating.min || 0;
    totalMax += car.addons.coating.max || 0;
    addedLines.push(`🟢 **+ Coating:** ${formatPriceRange(car.addons.coating.min, car.addons.coating.max, car.addons.coating.isPlus, false)}`);
  } else {
    addedLines.push('🔴 **Coating:** No');
  }

  if (session.livery) {
    totalMin += session.liveryMin || 0;
    totalMax += session.liveryMax || 0;
    addedLines.push(`🟢 **+ Custom Livery:** ${formatPriceRange(session.liveryMin, session.liveryMax, false, false)}`);
  } else {
    addedLines.push('🔴 **Livery:** No');
  }

  addedLines.push(`${session.turbo ? '🟢' : '🔴'} **Turbo:** ${session.turbo ? 'Yes (With Turbo)' : 'No (No Turbo)'}`);

  const totalEstimatedFormatted = formatPriceRange(totalMin, totalMax, isPlus, true);

  const embed = new EmbedBuilder()
    .setColor(0x00F59B)
    .setTitle(`🚘 ${car.name.toUpperCase()} — ESTIMATED PRICE & SPECS`)
    .setDescription('*Estimated prices for every car in RDS.*')
    .addFields(
      {
        name: '📊 Top Car Info (Speed & Base Stage Price)',
        value: [
          `• **Upgrade Spec:** ${stageLabel}`,
          `• **Top Speed:** ${speedText}`,
          `• **Base Car Price (${stageLabel}):** ${basePriceFormatted}`
        ].join('\n'),
        inline: false
      },
      {
        name: '🛠️ Selected Options & Add-On Values',
        value: addedLines.join('\n'),
        inline: false
      },
      {
        name: '💵 TOTAL ESTIMATED PRICE',
        value: `### ${totalEstimatedFormatted}`,
        inline: false
      },
      {
        name: '📌 Important RDS Notes & Coating Guide',
        value: RDS_DISCLAIMER,
        inline: false
      }
    )
    .setFooter({ text: `Generated by ${requestedByUser.username} • Estimated RDS Pricing Guide` })
    .setTimestamp();

  if (car.imageUrl && car.imageUrl.startsWith('http')) {
    embed.setImage(car.imageUrl);
  }

  return embed;
}

// ==========================================
// 7. DISCORD CLIENT INITIALIZATION & EVENTS
// ==========================================
const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.once('ready', async () => {
  console.log(`✅ Logged in as ${client.user.tag}`);
  console.log(`👑 Configured Bot Owner Username: ${OWNER_USERNAME}`);
  console.log(`🗄️ Active Database Mode: ${dbMode.toUpperCase()}`);

  const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);
  try {
    console.log('🔄 Registering global slash commands...');
    await rest.put(
      Routes.applicationCommands(process.env.CLIENT_ID || client.user.id),
      { body: commands }
    );
    console.log('✅ Slash commands registered successfully!');
  } catch (err) {
    console.error('❌ Failed to register slash commands:', err);
  }
});

// ==========================================
// 8. INTERACTION HANDLER
// ==========================================
client.on('interactionCreate', async (interaction) => {
  try {
    // ----------------------------------------
    // A. AUTOCOMPLETE SEARCH (/car-info & /car-price)
    // ----------------------------------------
    if (interaction.isAutocomplete()) {
      const focusedValue = interaction.options.getFocused().toLowerCase().trim();
      const matchedCars = await DB.searchCarsAutocomplete(focusedValue);
      return await interaction.respond(
        matchedCars.map(c => ({ name: c.name, value: c.name }))
      );
    }

    // ----------------------------------------
    // B. SLASH COMMANDS
    // ----------------------------------------
    if (interaction.isChatInputCommand()) {
      const { commandName } = interaction;

      // 1. /admin-add (Owner only)
      if (commandName === 'admin-add') {
        const callerRole = await getUserRole(interaction.user);
        if (callerRole !== 'owner') {
          return interaction.reply({
            content: `❌ Only the Bot Owner (**${OWNER_USERNAME}**) can use \`/admin-add\`!`,
            flags: MessageFlags.Ephemeral
          });
        }

        const targetUser = interaction.options.getUser('user');
        const action = interaction.options.getString('action');

        if (action === 'add') {
          await DB.upsertStaff(targetUser.id, targetUser.username, 'admin', interaction.user.username);
          return interaction.reply({
            content: `✅ **${targetUser.username}** has been promoted to **Bot Admin**! They can now use \`/mod-add\` and \`/admin-cars\` (Add, Edit, Delete).`,
            flags: MessageFlags.Ephemeral
          });
        } else {
          await DB.removeStaff(targetUser.id, 'admin');
          return interaction.reply({
            content: `🗑️ **${targetUser.username}** has been removed from **Bot Admins**.`,
            flags: MessageFlags.Ephemeral
          });
        }
      }

      // 2. /mod-add (Owner & Admins)
      if (commandName === 'mod-add') {
        const callerRole = await getUserRole(interaction.user);
        if (callerRole !== 'owner' && callerRole !== 'admin') {
          return interaction.reply({
            content: '❌ Only the Bot Owner and Admins can use `/mod-add`!',
            flags: MessageFlags.Ephemeral
          });
        }

        const targetUser = interaction.options.getUser('user');
        const action = interaction.options.getString('action');

        if (action === 'add') {
          await DB.upsertStaff(targetUser.id, targetUser.username, 'mod', interaction.user.username);
          return interaction.reply({
            content: `✅ **${targetUser.username}** has been added as a **Bot Moderator**! They can now Add and Edit cars using \`/admin-cars\`.`,
            flags: MessageFlags.Ephemeral
          });
        } else {
          await DB.removeStaff(targetUser.id, 'mod');
          return interaction.reply({
            content: `🗑️ **${targetUser.username}** has been removed from **Bot Moderators**.`,
            flags: MessageFlags.Ephemeral
          });
        }
      }

      // 3. /staff-list
      if (commandName === 'staff-list') {
        const staffList = await DB.getAllStaff();
        const admins = staffList.filter(s => s.role === 'admin').map(s => `• **${s.username}** (<@${s.userId}>)`);
        const mods = staffList.filter(s => s.role === 'mod').map(s => `• **${s.username}** (<@${s.userId}>)`);

        const embed = new EmbedBuilder()
          .setColor(0x5865F2)
          .setTitle('🛡️ RDS Car Bot — Staff Directory')
          .addFields(
            { name: '👑 Bot Owner', value: `• **${OWNER_USERNAME}**`, inline: false },
            { name: '⚔️ Bot Admins (Can Add Mods & Add/Edit/Delete Cars)', value: admins.length ? admins.join('\n') : 'None', inline: false },
            { name: '🔧 Bot Moderators (Can Add & Edit Cars)', value: mods.length ? mods.join('\n') : 'None', inline: false }
          );

        return interaction.reply({ embeds: [embed], flags: MessageFlags.Ephemeral });
      }

      // 4. /admin-cars (Owner, Admins, Mods)
      if (commandName === 'admin-cars') {
        const callerRole = await getUserRole(interaction.user);
        if (!callerRole) {
          return interaction.reply({
            content: '❌ Access Denied! Only **hyper_legend_1_og**, Admins, and Moderators can access `/admin-cars`.',
            flags: MessageFlags.Ephemeral
          });
        }

        const totalCars = await DB.countCars();
        const panelEmbed = new EmbedBuilder()
          .setColor(0x5865F2)
          .setTitle('🚗 RDS Admin Car Management Panel')
          .setDescription(
            [
              `Welcome, **${interaction.user.username}**! Your Role: **${callerRole.toUpperCase()}**`,
              `Total Cars in Database: **${totalCars}** *(DB Mode: ${dbMode.toUpperCase()})*`,
              '',
              'Select an action below:',
              '• **➕ Add Car:** Launch step-by-step wizard (Name & Image ➔ Add-ons ➔ Stages 1–7).',
              '• **✏️ Edit Car:** Update speeds, prices, or images of an existing car.',
              '• **🗑️ Delete Car:** Permanently remove a car *(Owner & Admins only)*.'
            ].join('\n')
          )
          .setFooter({ text: 'Tip: When entering prices like 400-550 or 30.3-83.5, the bot automatically counts them as Millions!' });

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId('admin_btn_add')
            .setLabel('➕ Add Car')
            .setStyle(ButtonStyle.Success),
          new ButtonBuilder()
            .setCustomId('admin_btn_edit')
            .setLabel('✏️ Edit Car')
            .setStyle(ButtonStyle.Primary),
          new ButtonBuilder()
            .setCustomId('admin_btn_delete')
            .setLabel('🗑️ Delete Car')
            .setStyle(ButtonStyle.Danger)
            .setDisabled(callerRole === 'mod')
        );

        return interaction.reply({
          embeds: [panelEmbed],
          components: [row],
          flags: MessageFlags.Ephemeral
        });
      }

      // 5. /car-info (Public output so everyone can see it)
      if (commandName === 'car-info') {
        const carQuery = interaction.options.getString('car').trim();
        const car = await DB.findCarByName(carQuery);

        if (!car) {
          return interaction.reply({
            content: `❌ Could not find any car matching **"${carQuery}"**. Try typing a few letters in \`/car-info\` and picking from the autocomplete list!`,
            flags: MessageFlags.Ephemeral
          });
        }

        const infoEmbed = buildCarInfoEmbed(car);
        return interaction.reply({ embeds: [infoEmbed] });
      }

      // 6. /car-price (Opens interactive Yes/No selector panel, then generates public panel)
      if (commandName === 'car-price') {
        const carQuery = interaction.options.getString('car').trim();
        const car = await DB.findCarByName(carQuery);

        if (!car) {
          return interaction.reply({
            content: `❌ Could not find any car matching **"${carQuery}"**. Try typing a few letters in \`/car-price\` and selecting from the search suggestions!`,
            flags: MessageFlags.Ephemeral
          });
        }

        const sessionData = {
          userId: interaction.user.id,
          car,
          premium: false,
          police: false,
          rainbowSmoke: false,
          coating: false,
          livery: false,
          liveryRaw: '0',
          liveryMin: 0,
          liveryMax: 0,
          turbo: false,
          upgrade: 'max' // 'max' is default selected option
        };

        calcSessions.set(interaction.user.id, sessionData);
        const panelPayload = buildCalculatorPanel(sessionData);

        return interaction.reply({
          ...panelPayload,
          flags: MessageFlags.Ephemeral
        });
      }
    }

    // ----------------------------------------
    // C. BUTTON INTERACTIONS
    // ----------------------------------------
    if (interaction.isButton()) {
      const { customId } = interaction;

      // 1. Admin Panel: Add Car button -> Opens Page 1 Modal (Car Name & Car Image Link)
      if (customId === 'admin_btn_add') {
        const role = await getUserRole(interaction.user);
        if (!role) return interaction.reply({ content: '❌ Unauthorized.', flags: MessageFlags.Ephemeral });

        adminSessions.set(interaction.user.id, {
          mode: 'add',
          nextStep: 'addons',
          data: {
            name: '',
            imageUrl: '',
            addons: {
              police: { raw: '10m', min: 10_000_000, max: 10_000_000, isPlus: false },
              rainbowSmoke: { raw: '10-15m', min: 10_000_000, max: 15_000_000, isPlus: false },
              premium: { raw: '$92,500', min: 92500, max: 92500, isPlus: false },
              coating: { raw: '30m', min: 30_000_000, max: 30_000_000, isPlus: false }
            },
            stages: {
              stage1: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage2: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage3: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage4: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage5: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage6: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' },
              stage7: { priceRaw: '0', priceMin: 0, priceMax: 0, isPlus: false, noTurboMph: 'N/A', noTurboKph: 'N/A', withTurboMph: 'N/A', withTurboKph: 'N/A' }
            }
          }
        });

        const modal = new ModalBuilder()
          .setCustomId('modal_wiz_basic')
          .setTitle('Add Car — Step 1: Name & Image');

        const nameInput = new TextInputBuilder()
          .setCustomId('car_name')
          .setLabel('Car Name')
          .setPlaceholder('e.g. Porsche Taycan Turbo S')
          .setStyle(TextInputStyle.Short)
          .setRequired(true);

        const imageInput = new TextInputBuilder()
          .setCustomId('car_image')
          .setLabel('Car Image Link (Direct URL)')
          .setPlaceholder('https://i.imgur.com/example.png')
          .setStyle(TextInputStyle.Short)
          .setRequired(false);

        modal.addComponents(
          new ActionRowBuilder().addComponents(nameInput),
          new ActionRowBuilder().addComponents(imageInput)
        );

        return await interaction.showModal(modal);
      }

      // 2. Admin Panel: Edit Car button
      if (customId === 'admin_btn_edit') {
        const role = await getUserRole(interaction.user);
        if (!role) return interaction.reply({ content: '❌ Unauthorized.', flags: MessageFlags.Ephemeral });

        const modal = new ModalBuilder()
          .setCustomId('modal_find_car_edit')
          .setTitle('Edit Car — Enter Car Name');

        const nameInput = new TextInputBuilder()
          .setCustomId('search_car_name')
          .setLabel('Car Name (full or partial name)')
          .setPlaceholder('e.g. tyc')
          .setStyle(TextInputStyle.Short)
          .setRequired(true);

        modal.addComponents(new ActionRowBuilder().addComponents(nameInput));
        return await interaction.showModal(modal);
      }

      // 3. Admin Panel: Delete Car button (Owner & Admins only)
      if (customId === 'admin_btn_delete') {
        const role = await getUserRole(interaction.user);
        if (role !== 'owner' && role !== 'admin') {
          return interaction.reply({
            content: '❌ Only the Bot Owner and Admins are allowed to delete cars!',
            flags: MessageFlags.Ephemeral
          });
        }

        const modal = new ModalBuilder()
          .setCustomId('modal_find_car_delete')
          .setTitle('Delete Car — Enter Car Name');

        const nameInput = new TextInputBuilder()
          .setCustomId('delete_car_name')
          .setLabel('Exact or Partial Car Name to Delete')
          .setPlaceholder('e.g. Porsche Taycan')
          .setStyle(TextInputStyle.Short)
          .setRequired(true);

        modal.addComponents(new ActionRowBuilder().addComponents(nameInput));
        return await interaction.showModal(modal);
      }

      // 4. Confirm Delete Button
      if (customId.startsWith('confirm_delete_')) {
        const role = await getUserRole(interaction.user);
        if (role !== 'owner' && role !== 'admin') {
          return interaction.reply({ content: '❌ Unauthorized.', flags: MessageFlags.Ephemeral });
        }

        const carIdentifier = customId.replace('confirm_delete_', '');
        const deleted = await DB.deleteCarByIdOrName(carIdentifier);
        if (!deleted) {
          return interaction.update({ content: '⚠️ Car was already deleted or not found.', embeds: [], components: [] });
        }
        return interaction.update({
          content: `🗑️ Successfully deleted **${deleted.name}** from the database!`,
          embeds: [],
          components: []
        });
      }

      // 5. Wizard Step Buttons (Basic, Add-ons, Stages 1-7, Save)
      if (customId.startsWith('wiz_')) {
        const session = adminSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({
            content: '⚠️ Your editing session expired. Please run `/admin-cars` again.',
            flags: MessageFlags.Ephemeral
          });
        }

        if (customId === 'wiz_save_finish') {
          if (!session.data.name) {
            return interaction.reply({ content: '❌ Car Name cannot be empty!', flags: MessageFlags.Ephemeral });
          }

          const updatePayload = {
            ...session.data,
            nameLower: session.data.name.toLowerCase(),
            updatedBy: interaction.user.username,
            updatedAt: new Date().toISOString()
          };

          const savedCar = await DB.saveCar(session.originalNameLower, updatePayload);
          adminSessions.delete(interaction.user.id);
          const previewEmbed = buildCarInfoEmbed(savedCar);

          return interaction.update({
            content: `✅ **${savedCar.name}** has been saved to the database! Here is how it looks in \`/car-info\`:`,
            embeds: [previewEmbed],
            components: []
          });
        }

        if (customId === 'wiz_step_basic') {
          const modal = new ModalBuilder()
            .setCustomId('modal_wiz_basic')
            .setTitle('Car Basic Info: Name & Image');

          modal.addComponents(
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('car_name')
                .setLabel('Car Name')
                .setStyle(TextInputStyle.Short)
                .setValue(session.data.name || '')
                .setRequired(true)
            ),
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('car_image')
                .setLabel('Car Image Link (Direct URL)')
                .setStyle(TextInputStyle.Short)
                .setValue(session.data.imageUrl || '')
                .setRequired(false)
            )
          );
          return await interaction.showModal(modal);
        }

        if (customId === 'wiz_step_addons') {
          const addons = session.data.addons;
          const modal = new ModalBuilder()
            .setCustomId('modal_wiz_addons')
            .setTitle('Step 2: Add-on Prices (Auto-Millions)');

          modal.addComponents(
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('addon_police')
                .setLabel('Police (Cop) Price (e.g. 10 or 10-15)')
                .setStyle(TextInputStyle.Short)
                .setValue(addons.police.raw || '10m')
                .setRequired(true)
            ),
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('addon_rb')
                .setLabel('Rainbow Smoke Price (e.g. 10-15)')
                .setStyle(TextInputStyle.Short)
                .setValue(addons.rainbowSmoke.raw || '10-15m')
                .setRequired(true)
            ),
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('addon_premium')
                .setLabel('Premium Price (e.g. $92,500 or 92500)')
                .setStyle(TextInputStyle.Short)
                .setValue(addons.premium.raw || '$92,500')
                .setRequired(true)
            ),
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('addon_coating')
                .setLabel('Coating Price (e.g. 30 or 25-35)')
                .setStyle(TextInputStyle.Short)
                .setValue(addons.coating.raw || '30m')
                .setRequired(true)
            )
          );
          return await interaction.showModal(modal);
        }

        // Stages 1 to 6 Modal (Asks Price + No Turbo MPH/KPH + With Turbo MPH/KPH)
        for (let stageNum = 1; stageNum <= 6; stageNum++) {
          if (customId === `wiz_step_stage${stageNum}`) {
            const st = session.data.stages[`stage${stageNum}`];
            const modal = new ModalBuilder()
              .setCustomId(`modal_wiz_stage_${stageNum}`)
              .setTitle(`Stage ${stageNum} — Price & Top Speeds`);

            modal.addComponents(
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('stage_price')
                  .setLabel(`Stage ${stageNum} Price (e.g. 400-550 or 2.5-3)`)
                  .setPlaceholder('Numbers < 10,000 automatically count as Millions!')
                  .setStyle(TextInputStyle.Short)
                  .setValue(st.priceRaw !== '0' ? st.priceRaw : '')
                  .setRequired(true)
              ),
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('no_turbo_mph')
                  .setLabel('Top Speed (No Turbo) — MPH')
                  .setPlaceholder('e.g. 217')
                  .setStyle(TextInputStyle.Short)
                  .setValue(st.noTurboMph !== 'N/A' ? st.noTurboMph : '')
                  .setRequired(true)
              ),
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('no_turbo_kph')
                  .setLabel('Top Speed (No Turbo) — KPH')
                  .setPlaceholder('e.g. 349')
                  .setStyle(TextInputStyle.Short)
                  .setValue(st.noTurboKph !== 'N/A' ? st.noTurboKph : '')
                  .setRequired(true)
              ),
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('with_turbo_mph')
                  .setLabel('Top Speed (With Turbo) — MPH')
                  .setPlaceholder('e.g. 227')
                  .setStyle(TextInputStyle.Short)
                  .setValue(st.withTurboMph !== 'N/A' ? st.withTurboMph : '')
                  .setRequired(true)
              ),
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('with_turbo_kph')
                  .setLabel('Top Speed (With Turbo) — KPH')
                  .setPlaceholder('e.g. 365')
                  .setStyle(TextInputStyle.Short)
                  .setValue(st.withTurboKph !== 'N/A' ? st.withTurboKph : '')
                  .setRequired(true)
              )
            );
            return await interaction.showModal(modal);
          }
        }

        // Stage 7 Modal (ONLY asks for Price)
        if (customId === 'wiz_step_stage7') {
          const st7 = session.data.stages.stage7;
          const modal = new ModalBuilder()
            .setCustomId('modal_wiz_stage_7')
            .setTitle('Stage 7 — Price Only');

          modal.addComponents(
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('stage7_price')
                .setLabel('Stage 7 Price (e.g. 850+ or leave 0 if none)')
                .setPlaceholder('e.g. 850+ or 800-900')
                .setStyle(TextInputStyle.Short)
                .setValue(st7.priceRaw !== '0' ? st7.priceRaw : '850+')
                .setRequired(false)
            )
          );
          return await interaction.showModal(modal);
        }
      }

      // 6. Calculator Toggle Buttons (/car-price)
      if (customId.startsWith('calc_')) {
        const session = calcSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({
            content: '⚠️ Calculator session expired. Please run `/car-price` again.',
            flags: MessageFlags.Ephemeral
          });
        }

        if (customId === 'calc_toggle_premium') session.premium = !session.premium;
        if (customId === 'calc_toggle_police') session.police = !session.police;
        if (customId === 'calc_toggle_rb') session.rainbowSmoke = !session.rainbowSmoke;
        if (customId === 'calc_toggle_coating') session.coating = !session.coating;
        if (customId === 'calc_toggle_turbo') session.turbo = !session.turbo;

        if (customId === 'calc_upgrade_max') session.upgrade = 'max';
        if (customId === 'calc_upgrade_stock') session.upgrade = 'stock';
        if (customId === 'calc_upgrade_stage7') session.upgrade = 'stage7';

        // Livery Button: If currently NO, open Modal asking for Livery Price (if left empty, stays NO)
        if (customId === 'calc_toggle_livery') {
          if (session.livery) {
            session.livery = false;
            session.liveryRaw = '0';
            session.liveryMin = 0;
            session.liveryMax = 0;
          } else {
            const modal = new ModalBuilder()
              .setCustomId('modal_calc_livery')
              .setTitle('Livery Option (Leave blank for NO)');

            const liveryInput = new TextInputBuilder()
              .setCustomId('livery_price_input')
              .setLabel('Livery Price (leave blank if NO livery)')
              .setPlaceholder('e.g. 5 or 5-10 (automatically counts as Millions)')
              .setStyle(TextInputStyle.Short)
              .setRequired(false);

            modal.addComponents(new ActionRowBuilder().addComponents(liveryInput));
            return await interaction.showModal(modal);
          }
        }

        // Generate Final Public Price Panel
        if (customId === 'calc_generate_final') {
          const finalEmbed = buildFinalPriceEmbed(session, interaction.user);
          calcSessions.delete(interaction.user.id);

          await interaction.update({
            content: '✅ **Car Price Panel Generated Below!**',
            embeds: [],
            components: []
          });

          return await interaction.followUp({
            embeds: [finalEmbed],
            ephemeral: false
          });
        }

        const updatedPanel = buildCalculatorPanel(session);
        return await interaction.update(updatedPanel);
      }
    }

    // ----------------------------------------
    // D. MODAL SUBMISSIONS
    // ----------------------------------------
    if (interaction.isModalSubmit()) {
      const { customId } = interaction;

      // 1. Wizard Step 1: Basic Info (Name & Image)
      if (customId === 'modal_wiz_basic') {
        const session = adminSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({ content: '⚠️ Session expired. Run `/admin-cars` again.', flags: MessageFlags.Ephemeral });
        }

        const name = interaction.fields.getTextInputValue('car_name').trim();
        const imageUrl = (interaction.fields.getTextInputValue('car_image') || '').trim();

        session.data.name = name;
        session.data.imageUrl = imageUrl;
        if (session.mode === 'add') session.nextStep = 'addons';

        const payload = buildWizardProgressPayload(session, 'Saved Car Name & Image Link! Click Next to set Add-on Prices.');
        return await interaction.reply({ ...payload, flags: MessageFlags.Ephemeral });
      }

      // 2. Wizard Step 2: Add-on Prices
      if (customId === 'modal_wiz_addons') {
        const session = adminSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({ content: '⚠️ Session expired. Run `/admin-cars` again.', flags: MessageFlags.Ephemeral });
        }

        session.data.addons.police = parseSmartPrice(interaction.fields.getTextInputValue('addon_police'));
        session.data.addons.rainbowSmoke = parseSmartPrice(interaction.fields.getTextInputValue('addon_rb'));
        session.data.addons.premium = parseSmartPrice(interaction.fields.getTextInputValue('addon_premium'));
        session.data.addons.coating = parseSmartPrice(interaction.fields.getTextInputValue('addon_coating'));

        if (session.nextStep === 'addons') session.nextStep = 'stage1';

        const payload = buildWizardProgressPayload(session, 'Saved Add-On Prices! Click Next for Stage 1.');
        return await interaction.update(payload);
      }

      // 3. Wizard Stages 1 - 7 Modals
      if (customId.startsWith('modal_wiz_stage_')) {
        const session = adminSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({ content: '⚠️ Session expired. Run `/admin-cars` again.', flags: MessageFlags.Ephemeral });
        }

        const stageNum = parseInt(customId.replace('modal_wiz_stage_', ''), 10);

        if (stageNum >= 1 && stageNum <= 6) {
          const parsedPrice = parseSmartPrice(interaction.fields.getTextInputValue('stage_price'));
          const noTurboMph = interaction.fields.getTextInputValue('no_turbo_mph').trim();
          const noTurboKph = interaction.fields.getTextInputValue('no_turbo_kph').trim();
          const withTurboMph = interaction.fields.getTextInputValue('with_turbo_mph').trim();
          const withTurboKph = interaction.fields.getTextInputValue('with_turbo_kph').trim();

          session.data.stages[`stage${stageNum}`] = {
            priceRaw: parsedPrice.raw,
            priceMin: parsedPrice.min,
            priceMax: parsedPrice.max,
            isPlus: parsedPrice.isPlus,
            noTurboMph,
            noTurboKph,
            withTurboMph,
            withTurboKph
          };

          session.nextStep = `stage${stageNum + 1}`;
          const payload = buildWizardProgressPayload(session, `Stage ${stageNum} Saved! Click Next for Stage ${stageNum + 1}.`);
          return await interaction.update(payload);
        }

        if (stageNum === 7) {
          const rawSt7 = interaction.fields.getTextInputValue('stage7_price') || '0';
          const parsedPrice = parseSmartPrice(rawSt7);

          session.data.stages.stage7 = {
            priceRaw: parsedPrice.raw,
            priceMin: parsedPrice.min,
            priceMax: parsedPrice.max,
            isPlus: parsedPrice.isPlus,
            noTurboMph: 'N/A',
            noTurboKph: 'N/A',
            withTurboMph: 'N/A',
            withTurboKph: 'N/A'
          };

          session.nextStep = 'finish';
          const payload = buildWizardProgressPayload(session, 'Stage 7 Price Saved! Click "💾 Save & Finish Now" to publish this car.');
          return await interaction.update(payload);
        }
      }

      // 4. Find Car to Edit Modal
      if (customId === 'modal_find_car_edit') {
        const query = interaction.fields.getTextInputValue('search_car_name').trim();
        const car = await DB.findCarByName(query);

        if (!car) {
          return interaction.reply({
            content: `❌ No car found matching **"${query}"**.`,
            flags: MessageFlags.Ephemeral
          });
        }

        const sessionObj = {
          mode: 'edit',
          originalNameLower: car.nameLower,
          nextStep: 'stage1',
          data: JSON.parse(JSON.stringify({
            name: car.name,
            imageUrl: car.imageUrl,
            addons: car.addons,
            stages: car.stages
          }))
        };

        adminSessions.set(interaction.user.id, sessionObj);
        const payload = buildWizardProgressPayload(sessionObj, `Loaded "${car.name}" for editing! Choose any stage or section below to edit.`);
        return await interaction.reply({ ...payload, flags: MessageFlags.Ephemeral });
      }

      // 5. Find Car to Delete Modal
      if (customId === 'modal_find_car_delete') {
        const query = interaction.fields.getTextInputValue('delete_car_name').trim();
        const car = await DB.findCarByName(query);

        if (!car) {
          return interaction.reply({
            content: `❌ No car found matching **"${query}"**.`,
            flags: MessageFlags.Ephemeral
          });
        }

        const confirmRow = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId(`confirm_delete_${car._id || car.nameLower}`)
            .setLabel(`🗑️ Confirm Delete: ${car.name}`)
            .setStyle(ButtonStyle.Danger)
        );

        return interaction.reply({
          content: `⚠️ Are you sure you want to permanently delete **${car.name}**?`,
          components: [confirmRow],
          flags: MessageFlags.Ephemeral
        });
      }

      // 6. Calculator Livery Price Modal
      if (customId === 'modal_calc_livery') {
        const session = calcSessions.get(interaction.user.id);
        if (!session) {
          return interaction.reply({ content: '⚠️ Calculator session expired.', flags: MessageFlags.Ephemeral });
        }

        const rawVal = (interaction.fields.getTextInputValue('livery_price_input') || '').trim();
        const parsed = parseSmartPrice(rawVal);

        if (parsed.min <= 0 && parsed.max <= 0) {
          session.livery = false;
          session.liveryRaw = '0';
          session.liveryMin = 0;
          session.liveryMax = 0;
        } else {
          session.livery = true;
          session.liveryRaw = formatPriceRange(parsed.min, parsed.max, parsed.isPlus, false);
          session.liveryMin = parsed.min;
          session.liveryMax = parsed.max;
        }

        const updatedPanel = buildCalculatorPanel(session);
        return await interaction.update(updatedPanel);
      }
    }
  } catch (err) {
    console.error('❌ Interaction Error:', err);
    if (!interaction.replied && !interaction.deferred) {
      await interaction.reply({
        content: '⚠️ An error occurred while processing that action. Please try again.',
        flags: MessageFlags.Ephemeral
      }).catch(() => {});
    }
  }
});

// ==========================================
// 9. INITIALIZE DATABASE & START BOT
// ==========================================
async function startBot() {
  if (!process.env.DISCORD_TOKEN) {
    console.error('❌ Missing DISCORD_TOKEN in your .env file!');
    process.exit(1);
  }

  try {
    await initDatabase();
    await client.login(process.env.DISCORD_TOKEN);
  } catch (error) {
    console.error('❌ Startup Error:', error);
    process.exit(1);
  }
}

startBot();