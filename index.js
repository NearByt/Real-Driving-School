require('dotenv').config();
const fs = require('fs');
const path = require('path');
const http = require('http');
const {
  Client,
  GatewayIntentBits,
  Partials,
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
  StringSelectMenuBuilder,
  MessageFlags
} = require('discord.js');

// ==========================================
// 1. KEEP-ALIVE WEB SERVER (FOR 24/7 HOSTING)
// ==========================================
const PORT = process.env.PORT || 3000;
http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('RDS Car Bot is online 24/7!');
}).listen(PORT, () => {
  console.log(`🌐 Keep-alive server listening on port ${PORT}`);
});

// ==========================================
// 2. CONFIGURATION & 3-IN-1 DATABASE ENGINE
// ==========================================
const TOKEN = (process.env.DISCORD_TOKEN || '').trim();
const CLIENT_ID = (process.env.CLIENT_ID || '').trim();
const OWNER_USERNAME = (process.env.OWNER_USERNAME || 'hyper_legend_1_og').trim().toLowerCase();
const FIREBASE_DB_URL = (process.env.FIREBASE_DB_URL || '').trim().replace(/\/+$/, '');
const MONGO_URI = (process.env.MONGO_URI || '').trim();
const LOCAL_DB_PATH = path.join(__dirname, 'database.json');

let dbMode = 'LOCAL';
let mongoCollection = null;

let store = {
  admins: [],
  mods: [],
  cars: {}
};

function loadLocalBackup() {
  try {
    if (fs.existsSync(LOCAL_DB_PATH)) {
      const raw = fs.readFileSync(LOCAL_DB_PATH, 'utf8');
      const parsed = JSON.parse(raw);
      store = {
        admins: Array.isArray(parsed.admins) ? parsed.admins : [],
        mods: Array.isArray(parsed.mods) ? parsed.mods : [],
        cars: parsed.cars && typeof parsed.cars === 'object' ? parsed.cars : {}
      };
    }
  } catch (err) {
    console.error('Local backup read error:', err);
  }
}

function saveLocalBackup() {
  try {
    fs.writeFileSync(LOCAL_DB_PATH, JSON.stringify(store, null, 2), 'utf8');
  } catch (err) {
    console.error('Local backup write error:', err);
  }
}

async function initDatabase() {
  loadLocalBackup();

  if (FIREBASE_DB_URL) {
    try {
      const res = await fetch(`${FIREBASE_DB_URL}/rds_bot_data.json`);
      if (!res.ok) {
        throw new Error(`Firebase HTTP ${res.status}: ${await res.text()}`);
      }
      const data = await res.json();
      if (data && typeof data === 'object') {
        store = {
          admins: Array.isArray(data.admins) ? data.admins : [],
          mods: Array.isArray(data.mods) ? data.mods : [],
          cars: data.cars && typeof data.cars === 'object' ? data.cars : {}
        };
      } else {
        await saveDatabase(true);
      }
      dbMode = 'FIREBASE';
      console.log('✅ Connected to Google Firebase Realtime Database (with local backup)!');
      return;
    } catch (err) {
      console.error('⚠️ Firebase connection failed, falling back:', err.message);
    }
  }

  if (MONGO_URI) {
    try {
      const { MongoClient } = require('mongodb');
      const mongoClient = new MongoClient(MONGO_URI);
      await mongoClient.connect();
      const db = mongoClient.db('rds_car_bot');
      mongoCollection = db.collection('bot_store');
      const doc = await mongoCollection.findOne({ _id: 'main' });
      if (doc && doc.data) {
        store = {
          admins: Array.isArray(doc.data.admins) ? doc.data.admins : [],
          mods: Array.isArray(doc.data.mods) ? doc.data.mods : [],
          cars: doc.data.cars && typeof doc.data.cars === 'object' ? doc.data.cars : {}
        };
      } else {
        await mongoCollection.updateOne({ _id: 'main' }, { $set: { data: store } }, { upsert: true });
      }
      dbMode = 'MONGODB';
      console.log('✅ Connected to MongoDB!');
      return;
    } catch (err) {
      console.error('⚠️ MongoDB connection failed, falling back to local JSON:', err.message);
    }
  }

  dbMode = 'LOCAL';
  saveLocalBackup();
  console.log('✅ Using built-in 24/7 database.json!');
}

async function saveDatabase(skipError = false) {
  saveLocalBackup();

  if (dbMode === 'FIREBASE' || (FIREBASE_DB_URL && skipError)) {
    const res = await fetch(`${FIREBASE_DB_URL}/rds_bot_data.json`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(store)
    });
    if (!res.ok) {
      const errText = await res.text();
      throw new Error(`Firebase save failed (${res.status}): ${errText}`);
    }
    return;
  }

  if (dbMode === 'MONGODB' && mongoCollection) {
    await mongoCollection.updateOne({ _id: 'main' }, { $set: { data: store } }, { upsert: true });
  }
}

// ==========================================
// 3. HELPER FUNCTIONS (ROLES, PRICES, SPEEDS)
// ==========================================
function getUserRole(user) {
  const uname = (user.username || '').toLowerCase();
  if (uname === OWNER_USERNAME) return 'OWNER';
  if (store.admins.includes(uname)) return 'ADMIN';
  if (store.mods.includes(uname)) return 'MOD';
  return 'USER';
}

function sanitizeImageUrl(raw) {
  if (!raw || typeof raw !== 'string') return '';
  const trimmed = raw.trim();
  if (!trimmed) return '';
  try {
    const parsed = new URL(trimmed);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return trimmed;
    }
    return '';
  } catch {
    return '';
  }
}

function parseSingleNumber(token) {
  if (!token) return 0;
  let str = token.toLowerCase().replace(/[$,\s+]/g, '');
  if (!str) return 0;

  let multiplier = 1;
  if (str.endsWith('b')) {
    multiplier = 1_000_000_000;
    str = str.slice(0, -1);
  } else if (str.endsWith('m')) {
    multiplier = 1_000_000;
    str = str.slice(0, -1);
  } else if (str.endsWith('k')) {
    multiplier = 1_000;
    str = str.slice(0, -1);
  } else {
    const val = parseFloat(str);
    if (!isNaN(val) && val > 0 && val < 10000) {
      multiplier = 1_000_000;
    }
  }

  const num = parseFloat(str);
  if (isNaN(num) || num < 0) return 0;
  return Math.round(num * multiplier);
}

function parsePriceInput(raw) {
  if (!raw || typeof raw !== 'string') {
    return { min: 0, max: 0, isPlus: false, raw: '' };
  }
  const cleaned = raw.trim();
  if (!cleaned || ['0', 'none', 'na', 'n/a', '-'].includes(cleaned.toLowerCase())) {
    return { min: 0, max: 0, isPlus: false, raw: cleaned };
  }

  const isPlus = cleaned.endsWith('+');
  const withoutPlus = isPlus ? cleaned.slice(0, -1).trim() : cleaned;
  const parts = withoutPlus.split(/[-~]/).map(p => p.trim()).filter(Boolean);

  if (parts.length === 0) {
    return { min: 0, max: 0, isPlus: false, raw: cleaned };
  }

  const minVal = parseSingleNumber(parts[0]);
  const maxVal = parts.length > 1 ? parseSingleNumber(parts[1]) : minVal;

  return {
    min: Math.min(minVal, maxVal),
    max: Math.max(minVal, maxVal),
    isPlus,
    raw: cleaned
  };
}

function formatMoney(num) {
  return '$' + Math.round(num || 0).toLocaleString('en-US');
}

function formatPriceRange(priceObj, addEstimated = false) {
  if (!priceObj || (priceObj.min === 0 && priceObj.max === 0)) {
    return 'N/A';
  }
  const plus = priceObj.isPlus ? '+' : '';
  const base =
    priceObj.min === priceObj.max
      ? `${formatMoney(priceObj.min)}${plus}`
      : `${formatMoney(priceObj.min)} ~ ${formatMoney(priceObj.max)}${plus}`;
  return addEstimated ? `${base} *(Estimated)*` : base;
}

function formatSpeedInput(raw) {
  if (!raw || typeof raw !== 'string') return 'N/A';
  const trimmed = raw.trim();
  if (!trimmed) return 'N/A';
  const twoNums = trimmed.match(/^(\d+(?:\.\d+)?)\s*[\/|\-,\s]\s*(\d+(?:\.\d+)?)$/);
  if (twoNums) {
    return `${twoNums[1]}mph / ${twoNums[2]}kph`;
  }
  return trimmed;
}

const RDS_DISCLAIMER_NOTES =
  '📌 **Estimated prices for every car in RDS.**\n' +
  '• **FYI:** These prices are approximate and not based on real-time pricing; they serve as a guide if a Car Dealer is absent.\n' +
  '• **Coating Prices:** Low-mid end cars add **+$30M ~ $35M** | High-end cars add **+$25M ~ $30M** *(Hard-to-find cars can exceed $30M–$40M+)*.\n' +
  '• *Subject to periodic updates.*';

// ==========================================
// 4. IN-MEMORY WIZARD & CALCULATOR SESSIONS
// ==========================================
const addWizardSessions = new Map();
const priceCalcSessions = new Map();

// ==========================================
// 5. SLASH COMMAND DEFINITIONS
// ==========================================
const commands = [
  new SlashCommandBuilder()
    .setName('admin-cars')
    .setDescription('Open the RDS Car Management Panel (Add, Edit, Delete cars)'),

  new SlashCommandBuilder()
    .setName('admin-add')
    .setDescription('Promote a user to Bot Admin (Owner only)')
    .addUserOption(opt =>
      opt.setName('user').setDescription('The user to promote to Bot Admin').setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName('mod-add')
    .setDescription('Promote a user to Bot Mod (Owner & Admins only)')
    .addUserOption(opt =>
      opt.setName('user').setDescription('The user to promote to Bot Mod').setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName('staff-list')
    .setDescription('View current Bot Owner, Admins, and Mods'),

  new SlashCommandBuilder()
    .setName('car-info')
    .setDescription('Search and view full stats, speeds, and stage prices for an RDS car')
    .addStringOption(opt =>
      opt
        .setName('car')
        .setDescription('Start typing a car name (e.g. tyc)')
        .setRequired(true)
        .setAutocomplete(true)
    ),

  new SlashCommandBuilder()
    .setName('car-price')
    .setDescription('Calculate the estimated price of an RDS car with add-ons & tune')
    .addStringOption(opt =>
      opt
        .setName('car')
        .setDescription('Start typing a car name (e.g. tyc)')
        .setRequired(true)
        .setAutocomplete(true)
    )
].map(cmd => cmd.toJSON());

// ==========================================
// 6. DISCORD CLIENT SETUP
// ==========================================
const client = new Client({
  intents: [GatewayIntentBits.Guilds],
  partials: [Partials.Channel]
});

client.once('ready', async () => {
  console.log(`✅ Logged in as ${client.user.tag}`);
  console.log(`👑 Configured Bot Owner Username: ${OWNER_USERNAME}`);
  console.log(`🗄️ Active Database Mode: ${dbMode}`);

  try {
    console.log('🔄 Registering global slash commands...');
    const rest = new REST({ version: '10' }).setToken(TOKEN);
    await rest.put(Routes.applicationCommands(CLIENT_ID), { body: commands });
    console.log('✅ Slash commands registered successfully!');
  } catch (err) {
    console.error('❌ Failed to register slash commands:', err);
  }
});

// ==========================================
// 7. BUILDERS FOR PANELS & CALCULATOR UI
// ==========================================
function buildAdminPanel(user) {
  const role = getUserRole(user);
  const carCount = Object.keys(store.cars).length;

  const embed = new EmbedBuilder()
    .setColor(0x2b6cb0)
    .setTitle('🚗 RDS Admin Car Management Panel')
    .setDescription(
      `Welcome, **${user.username}**! Your Role: **${role}**\n` +
      `Total Cars in Database: **${carCount}** *(DB Mode: ${dbMode})*\n\n` +
      `Select an action below:\n` +
      `• **➕ Add Car:** Launch step-by-step wizard (Name & Image ➡️ Add-ons ➡️ Stages 1–7).\n` +
      `• **✏️ Edit Car:** Update speeds, prices, or images of an existing car.\n` +
      `• **🗑️ Delete Car:** Permanently remove a car *(Owner & Admins only)*.\n\n` +
      `*Tip: When entering prices like \`400-550\` or \`30.3-83.5\`, the bot automatically counts them as Millions!*`
    );

  const row = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId('admin_add_car')
      .setLabel('Add Car')
      .setEmoji('➕')
      .setStyle(ButtonStyle.Success),
    new ButtonBuilder()
      .setCustomId('admin_edit_car')
      .setLabel('Edit Car')
      .setEmoji('✏️')
      .setStyle(ButtonStyle.Primary),
    new ButtonBuilder()
      .setCustomId('admin_delete_car')
      .setLabel('Delete Car')
      .setEmoji('🗑️')
      .setStyle(ButtonStyle.Danger)
  );

  return { embeds: [embed], components: [row] };
}

function buildPriceConfigurator(sessionId, session, car) {
  const embed = new EmbedBuilder()
    .setColor(0x3182ce)
    .setTitle(`💰 Price Calculator: ${car.name}`)
    .setDescription(
      'Select your options below (Green = **YES**, Grey = **NO**), then click **Calculate Final Price**:\n\n' +
      `• **Premium:** ${session.premium ? '✅ YES' : '❌ NO'}\n` +
      `• **Police:** ${session.police ? '✅ YES' : '❌ NO'}\n` +
      `• **Rainbow Smoke:** ${session.rbSmoke ? '✅ YES' : '❌ NO'}\n` +
      `• **Coating:** ${session.coating ? '✅ YES' : '❌ NO'}\n` +
      `• **Livery:** ${session.livery ? `✅ YES (${formatPriceRange(session.liveryPrice)})` : '❌ NO'}\n` +
      `• **Turbo:** ${session.turbo ? '✅ YES' : '❌ NO'}\n` +
      `• **Car Tune:** **${session.tune === 'MAX' ? 'MAX (Stage 6)' : 'STOCK (Stage 1)'}**`
    );

  const row1 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_premium`)
      .setLabel(`Premium: ${session.premium ? 'YES' : 'NO'}`)
      .setStyle(session.premium ? ButtonStyle.Success : ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_police`)
      .setLabel(`Police: ${session.police ? 'YES' : 'NO'}`)
      .setStyle(session.police ? ButtonStyle.Success : ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_rbSmoke`)
      .setLabel(`RB Smoke: ${session.rbSmoke ? 'YES' : 'NO'}`)
      .setStyle(session.rbSmoke ? ButtonStyle.Success : ButtonStyle.Secondary)
  );

  const row2 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_coating`)
      .setLabel(`Coating: ${session.coating ? 'YES' : 'NO'}`)
      .setStyle(session.coating ? ButtonStyle.Success : ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_livery`)
      .setLabel(`Livery: ${session.livery ? 'YES' : 'NO'}`)
      .setStyle(session.livery ? ButtonStyle.Success : ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId(`pcalc_toggle_${sessionId}_turbo`)
      .setLabel(`Turbo: ${session.turbo ? 'YES' : 'NO'}`)
      .setStyle(session.turbo ? ButtonStyle.Success : ButtonStyle.Secondary)
  );

  const row3 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId(`pcalc_tune_${sessionId}`)
      .setLabel(`Tune: ${session.tune === 'MAX' ? 'MAX (Default)' : 'STOCK'}`)
      .setStyle(session.tune === 'MAX' ? ButtonStyle.Primary : ButtonStyle.Secondary)
  );

  const row4 = new ActionRowBuilder().addComponents(
    new ButtonBuilder()
      .setCustomId(`pcalc_finish_${sessionId}`)
      .setLabel('Calculate Final Price')
      .setEmoji('💰')
      .setStyle(ButtonStyle.Success)
  );

  return { embeds: [embed], components: [row1, row2, row3, row4] };
}

function buildFinalPriceEmbed(car, session) {
  const isMax = session.tune === 'MAX';
  const stageObj = isMax
    ? (car.stages && (car.stages['6'] || car.stages['1'])) || {}
    : (car.stages && car.stages['1']) || {};

  const basePrice = stageObj.price || { min: 0, max: 0, isPlus: false };
  const topSpeed = session.turbo
    ? stageObj.withTurbo || 'N/A'
    : stageObj.noTurbo || 'N/A';

  let totalMin = basePrice.min || 0;
  let totalMax = basePrice.max || 0;
  let isPlus = Boolean(basePrice.isPlus);

  const addonLines = [];
  const addons = car.addons || {};

  if (session.premium) {
    const p = addons.premium || { min: 0, max: 0 };
    totalMin += p.min;
    totalMax += p.max;
    addonLines.push(`• **Premium:** ${formatPriceRange(p)}`);
  }
  if (session.police) {
    const p = addons.police || { min: 0, max: 0 };
    totalMin += p.min;
    totalMax += p.max;
    addonLines.push(`• **Police:** ${formatPriceRange(p)}`);
  }
  if (session.rbSmoke) {
    const p = addons.rainbowSmoke || { min: 0, max: 0 };
    totalMin += p.min;
    totalMax += p.max;
    addonLines.push(`• **Rainbow Smoke:** ${formatPriceRange(p)}`);
  }
  if (session.coating) {
    const p = addons.coating || { min: 0, max: 0 };
    totalMin += p.min;
    totalMax += p.max;
    addonLines.push(`• **Coating:** ${formatPriceRange(p)}`);
  }
  if (session.livery) {
    const p = session.liveryPrice || { min: 0, max: 0 };
    totalMin += p.min;
    totalMax += p.max;
    addonLines.push(`• **Livery:** ${formatPriceRange(p)}`);
  }
  if (session.turbo) {
    addonLines.push(`• **Turbo:** Installed *(Included in Speed)*`);
  }

  const totalRangeStr = formatPriceRange({ min: totalMin, max: totalMax, isPlus }, true);

  const embed = new EmbedBuilder()
    .setColor(0x2f855a)
    .setTitle(`🚘 ${car.name}`)
    .addFields(
      {
        name: `📊 Car Info (${isMax ? 'Max - Stage 6' : 'Stock - Stage 1'})`,
        value:
          `**Top Speed (${session.turbo ? 'With Turbo' : 'No Turbo'}):** ${topSpeed}\n` +
          `**Base Car Price:** ${formatPriceRange(basePrice, true)}`,
        inline: false
      },
      {
        name: '🧩 Selected Add-ons & Values',
        value: addonLines.length > 0 ? addonLines.join('\n') : '*No extra add-ons selected*',
        inline: false
      },
      {
        name: '💵 Total Estimated Value',
        value: `**${totalRangeStr}**\n\n${RDS_DISCLAIMER_NOTES}`,
        inline: false
      }
    );

  const validImg = sanitizeImageUrl(car.image);
  if (validImg) {
    embed.setImage(validImg);
  }

  return embed;
}

function buildCarInfoEmbed(car) {
  const embed = new EmbedBuilder()
    .setColor(0x1a365d)
    .setTitle(`🚗 ${car.name} — Car Info & Estimated Prices`);

  const stages = car.stages || {};
  for (let s = 1; s <= 6; s++) {
    const st = stages[String(s)];
    if (st && (st.price?.min > 0 || st.noTurbo !== 'N/A' || st.withTurbo !== 'N/A')) {
      embed.addFields({
        name: `Stage ${s}`,
        value:
          `**Price:** ${formatPriceRange(st.price, true)}\n` +
          `**Top Speed (No Turbo):** ${st.noTurbo || 'N/A'}\n` +
          `**Top Speed (With Turbo):** ${st.withTurbo || 'N/A'}`,
        inline: true
      });
    }
  }

  if (stages['7'] && stages['7'].price && stages['7'].price.min > 0) {
    embed.addFields({
      name: 'Stage 7',
      value: `**Price:** ${formatPriceRange(stages['7'].price, true)}`,
      inline: true
    });
  }

  const addons = car.addons || {};
  embed.addFields(
    {
      name: '💎 Add-on Values',
      value:
        `• **Premium:** ${formatPriceRange(addons.premium)}\n` +
        `• **Police:** ${formatPriceRange(addons.police)}\n` +
        `• **Rainbow Smoke:** ${formatPriceRange(addons.rainbowSmoke)}\n` +
        `• **Coating:** ${formatPriceRange(addons.coating)}`,
      inline: false
    },
    {
      name: 'ℹ️ Notes',
      value: RDS_DISCLAIMER_NOTES,
      inline: false
    }
  );

  const validImg = sanitizeImageUrl(car.image);
  if (validImg) {
    embed.setImage(validImg);
  }

  return embed;
}

// ==========================================
// 8. INTERACTION HANDLER
// ==========================================
client.on('interactionCreate', async interaction => {
  try {
    // ------------------------------------------
    // A. AUTOCOMPLETE FOR /car-info & /car-price
    // ------------------------------------------
    if (interaction.isAutocomplete()) {
      const focused = (interaction.options.getFocused() || '').toLowerCase();
      const matches = Object.entries(store.cars)
        .filter(([, car]) => car && car.name && car.name.toLowerCase().includes(focused))
        .slice(0, 25)
        .map(([id, car]) => ({ name: car.name, value: id }));

      await interaction.respond(matches);
      return;
    }

    // ------------------------------------------
    // B. SLASH COMMANDS
    // ------------------------------------------
    if (interaction.isChatInputCommand()) {
      const { commandName } = interaction;

      if (commandName === 'admin-add') {
        if (getUserRole(interaction.user) !== 'OWNER') {
          await interaction.reply({
            content: '❌ Only the Bot Owner can use `/admin-add`.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const target = interaction.options.getUser('user', true);
        const uname = target.username.toLowerCase();
        if (!store.admins.includes(uname)) {
          store.admins.push(uname);
          await saveDatabase();
        }
        await interaction.reply({
          content: `✅ **${target.username}** has been promoted to **Bot Admin**! They can now use \`/mod-add\` and \`/admin-cars\` (Add, Edit, Delete).`,
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (commandName === 'mod-add') {
        const role = getUserRole(interaction.user);
        if (role !== 'OWNER' && role !== 'ADMIN') {
          await interaction.reply({
            content: '❌ Only the Bot Owner or Bot Admins can use `/mod-add`.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const target = interaction.options.getUser('user', true);
        const uname = target.username.toLowerCase();
        if (!store.mods.includes(uname)) {
          store.mods.push(uname);
          await saveDatabase();
        }
        await interaction.reply({
          content: `✅ **${target.username}** has been promoted to **Bot Mod**! They can now use \`/admin-cars\` to Add or Edit cars.`,
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (commandName === 'staff-list') {
        const adminsList = store.admins.length ? store.admins.map(a => `• ${a}`).join('\n') : '*None*';
        const modsList = store.mods.length ? store.mods.map(m => `• ${m}`).join('\n') : '*None*';
        const embed = new EmbedBuilder()
          .setColor(0x2b6cb0)
          .setTitle('🛡️ RDS Bot Staff List')
          .addFields(
            { name: '👑 Owner', value: `• ${OWNER_USERNAME}`, inline: false },
            { name: '⭐ Admins (Add, Edit, Delete, Mod-Add)', value: adminsList, inline: false },
            { name: '🔧 Mods (Add, Edit)', value: modsList, inline: false }
          );
        await interaction.reply({ embeds: [embed], flags: MessageFlags.Ephemeral });
        return;
      }

      if (commandName === 'admin-cars') {
        const role = getUserRole(interaction.user);
        if (role === 'USER') {
          await interaction.reply({
            content: '❌ You do not have permission to use `/admin-cars`.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        await interaction.reply({
          ...buildAdminPanel(interaction.user),
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (commandName === 'car-info') {
        const query = interaction.options.getString('car', true);
        const car =
          store.cars[query] ||
          Object.values(store.cars).find(c => c.name.toLowerCase() === query.toLowerCase()) ||
          Object.values(store.cars).find(c => c.name.toLowerCase().includes(query.toLowerCase()));

        if (!car) {
          await interaction.reply({
            content: `❌ Car **"${query}"** was not found in the database.`,
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        // Public embed visible to everyone in the channel
        await interaction.reply({ embeds: [buildCarInfoEmbed(car)] });
        return;
      }

      if (commandName === 'car-price') {
        const query = interaction.options.getString('car', true);
        let carEntry = store.cars[query] ? [query, store.cars[query]] : null;
        if (!carEntry) {
          carEntry =
            Object.entries(store.cars).find(([, c]) => c.name.toLowerCase() === query.toLowerCase()) ||
            Object.entries(store.cars).find(([, c]) => c.name.toLowerCase().includes(query.toLowerCase()));
        }

        if (!carEntry) {
          await interaction.reply({
            content: `❌ Car **"${query}"** was not found in the database.`,
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        const [carId, car] = carEntry;
        const sessionId = `${interaction.user.id}_${Date.now()}`;
        const session = {
          userId: interaction.user.id,
          carId,
          premium: false,
          police: false,
          rbSmoke: false,
          coating: false,
          livery: false,
          liveryPrice: { min: 0, max: 0, isPlus: false },
          turbo: false,
          tune: 'MAX'
        };
        priceCalcSessions.set(sessionId, session);

        await interaction.reply({
          ...buildPriceConfigurator(sessionId, session, car),
          flags: MessageFlags.Ephemeral
        });
        return;
      }
    }

    // ------------------------------------------
    // C. BUTTON INTERACTIONS
    // ------------------------------------------
    if (interaction.isButton()) {
      const id = interaction.customId;

      // 1. Add Car Wizard Start
      if (id === 'admin_add_car') {
        const role = getUserRole(interaction.user);
        if (role === 'USER') {
          await interaction.reply({ content: '❌ Permission denied.', flags: MessageFlags.Ephemeral });
          return;
        }

        const modal = new ModalBuilder()
          .setCustomId('modal_add_step1')
          .setTitle('Add Car - Step 1: Basic Info');

        const nameInput = new TextInputBuilder()
          .setCustomId('car_name')
          .setLabel('Car Name')
          .setPlaceholder('e.g. Koenigsegg Jesko')
          .setStyle(TextInputStyle.Short)
          .setRequired(true);

        const imgInput = new TextInputBuilder()
          .setCustomId('car_image')
          .setLabel('Car Image Link (Optional, https://...)')
          .setPlaceholder('https://example.com/car.png')
          .setStyle(TextInputStyle.Short)
          .setRequired(false);

        modal.addComponents(
          new ActionRowBuilder().addComponents(nameInput),
          new ActionRowBuilder().addComponents(imgInput)
        );

        await interaction.showModal(modal);
        return;
      }

      // 2. Add Car Wizard -> Open Add-ons Modal
      if (id === 'wizard_open_addons') {
        const modal = new ModalBuilder()
          .setCustomId('modal_add_addons')
          .setTitle('Add Car - Step 2: Add-on Prices');

        modal.addComponents(
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_police')
              .setLabel('Police Price (e.g. 10 for 10M)')
              .setPlaceholder('e.g. 10')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_rbsmoke')
              .setLabel('Rainbow Smoke Price (e.g. 10-15)')
              .setPlaceholder('e.g. 10-15')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_premium')
              .setLabel('Premium Price (e.g. 92500 or 30)')
              .setPlaceholder('e.g. 92500')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_coating')
              .setLabel('Coating Price (e.g. 30 for 30M)')
              .setPlaceholder('e.g. 30')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          )
        );

        await interaction.showModal(modal);
        return;
      }

      // 3. Add Car Wizard -> Open Stage 1-6 Modal
      if (id.startsWith('wizard_open_stage_')) {
        const stageNum = id.replace('wizard_open_stage_', '');
        if (stageNum === '7') {
          const modal = new ModalBuilder()
            .setCustomId('modal_add_stage_7')
            .setTitle('Add Car - Stage 7 (Price Only)');

          modal.addComponents(
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('stage_price')
                .setLabel('Stage 7 Price (e.g. 850+ or 850,000,000+)')
                .setPlaceholder('e.g. 850+')
                .setStyle(TextInputStyle.Short)
                .setRequired(false)
            )
          );

          await interaction.showModal(modal);
          return;
        }

        const modal = new ModalBuilder()
          .setCustomId(`modal_add_stage_${stageNum}`)
          .setTitle(`Add Car - Stage ${stageNum}`);

        modal.addComponents(
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('stage_price')
              .setLabel(`Stage ${stageNum} Price (e.g. 2.5-3)`)
              .setPlaceholder('e.g. 2.5-3')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('speed_no_turbo')
              .setLabel('Top Speed No Turbo (mph / kph)')
              .setPlaceholder('e.g. 217mph / 349kph')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('speed_with_turbo')
              .setLabel('Top Speed With Turbo (mph / kph)')
              .setPlaceholder('e.g. 227mph / 365kph')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          )
        );

        await interaction.showModal(modal);
        return;
      }

      // 4. Add Car Wizard -> Finish & Save Early
      if (id === 'wizard_finish_now') {
        const session = addWizardSessions.get(interaction.user.id);
        if (!session) {
          await interaction.reply({
            content: '❌ Your Add Car session expired. Please run `/admin-cars` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const carId = `car_${Date.now()}`;
        store.cars[carId] = session;
        await saveDatabase();
        addWizardSessions.delete(interaction.user.id);

        await interaction.reply({
          content: `✅ **${session.name}** has been saved to the database!`,
          embeds: [buildCarInfoEmbed(session)],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 5. Edit Car Button
      if (id === 'admin_edit_car') {
        const role = getUserRole(interaction.user);
        if (role === 'USER') {
          await interaction.reply({ content: '❌ Permission denied.', flags: MessageFlags.Ephemeral });
          return;
        }
        const entries = Object.entries(store.cars);
        if (entries.length === 0) {
          await interaction.reply({
            content: '❌ There are **0 cars** in the database right now! Click **➕ Add Car** first.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        const select = new StringSelectMenuBuilder()
          .setCustomId('select_edit_car')
          .setPlaceholder('Choose a car to edit...')
          .addOptions(
            entries.slice(0, 25).map(([carId, car]) => ({
              label: car.name.slice(0, 100),
              value: carId
            }))
          );

        await interaction.reply({
          content: '✏️ Select which car you want to edit:',
          components: [new ActionRowBuilder().addComponents(select)],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 6. Edit Car Section Buttons
      if (id.startsWith('edit_basic_')) {
        const carId = id.replace('edit_basic_', '');
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        const modal = new ModalBuilder()
          .setCustomId(`modal_edit_basic_${carId}`)
          .setTitle('Edit Car - Basic Info');

        modal.addComponents(
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('car_name')
              .setLabel('Car Name')
              .setValue(car.name || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(true)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('car_image')
              .setLabel('Car Image Link (Optional, https://...)')
              .setValue(car.image || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          )
        );
        await interaction.showModal(modal);
        return;
      }

      if (id.startsWith('edit_addons_')) {
        const carId = id.replace('edit_addons_', '');
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        const addons = car.addons || {};
        const modal = new ModalBuilder()
          .setCustomId(`modal_edit_addons_${carId}`)
          .setTitle('Edit Car - Add-on Prices');

        modal.addComponents(
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_police')
              .setLabel('Police Price')
              .setValue(addons.police?.raw || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_rbsmoke')
              .setLabel('Rainbow Smoke Price')
              .setValue(addons.rainbowSmoke?.raw || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_premium')
              .setLabel('Premium Price')
              .setValue(addons.premium?.raw || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          ),
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('price_coating')
              .setLabel('Coating Price')
              .setValue(addons.coating?.raw || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          )
        );
        await interaction.showModal(modal);
        return;
      }

      if (id.startsWith('edit_stage_')) {
        const rest = id.replace('edit_stage_', '');
        const lastUnderscore = rest.lastIndexOf('_');
        const stageNum = rest.slice(lastUnderscore + 1);
        const carId = rest.slice(0, lastUnderscore);
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        const st = (car.stages && car.stages[stageNum]) || {};
        const modal = new ModalBuilder()
          .setCustomId(`modal_edit_stage_${carId}_${stageNum}`)
          .setTitle(`Edit Stage ${stageNum}`);

        modal.addComponents(
          new ActionRowBuilder().addComponents(
            new TextInputBuilder()
              .setCustomId('stage_price')
              .setLabel(`Stage ${stageNum} Price`)
              .setValue(st.price?.raw || '')
              .setStyle(TextInputStyle.Short)
              .setRequired(false)
          )
        );

        if (stageNum !== '7') {
          modal.addComponents(
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('speed_no_turbo')
                .setLabel('Top Speed No Turbo')
                .setValue(st.noTurbo && st.noTurbo !== 'N/A' ? st.noTurbo : '')
                .setStyle(TextInputStyle.Short)
                .setRequired(false)
            ),
            new ActionRowBuilder().addComponents(
              new TextInputBuilder()
                .setCustomId('speed_with_turbo')
                .setLabel('Top Speed With Turbo')
                .setValue(st.withTurbo && st.withTurbo !== 'N/A' ? st.withTurbo : '')
                .setStyle(TextInputStyle.Short)
                .setRequired(false)
            )
          );
        }

        await interaction.showModal(modal);
        return;
      }

      // 7. Delete Car Button
      if (id === 'admin_delete_car') {
        const role = getUserRole(interaction.user);
        if (role !== 'OWNER' && role !== 'ADMIN') {
          await interaction.reply({
            content: '❌ Only the Bot Owner or Bot Admins can delete cars.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const entries = Object.entries(store.cars);
        if (entries.length === 0) {
          await interaction.reply({
            content: '❌ There are **0 cars** in the database to delete.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        const select = new StringSelectMenuBuilder()
          .setCustomId('select_delete_car')
          .setPlaceholder('Choose a car to permanently delete...')
          .addOptions(
            entries.slice(0, 25).map(([carId, car]) => ({
              label: car.name.slice(0, 100),
              value: carId
            }))
          );

        await interaction.reply({
          content: '🗑️ Select which car you want to delete:',
          components: [new ActionRowBuilder().addComponents(select)],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (id.startsWith('confirm_delete_')) {
        const carId = id.replace('confirm_delete_', '');
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car already deleted.', flags: MessageFlags.Ephemeral });
          return;
        }
        const deletedName = car.name;
        delete store.cars[carId];
        await saveDatabase();
        await interaction.update({
          content: `🗑️ **${deletedName}** has been permanently deleted from the database.`,
          embeds: [],
          components: []
        });
        return;
      }

      if (id === 'cancel_delete') {
        await interaction.update({
          content: '✅ Deletion cancelled.',
          embeds: [],
          components: []
        });
        return;
      }

      // 8. /car-price Configurator Buttons
      if (id.startsWith('pcalc_toggle_')) {
        const rest = id.replace('pcalc_toggle_', '');
        const lastUnderscore = rest.lastIndexOf('_');
        const field = rest.slice(lastUnderscore + 1);
        const sessionId = rest.slice(0, lastUnderscore);

        const session = priceCalcSessions.get(sessionId);
        if (!session) {
          await interaction.reply({
            content: '❌ This price calculator session expired. Run `/car-price` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const car = store.cars[session.carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car no longer exists.', flags: MessageFlags.Ephemeral });
          return;
        }

        if (field === 'livery') {
          if (!session.livery) {
            const modal = new ModalBuilder()
              .setCustomId(`modal_livery_${sessionId}`)
              .setTitle('Enter Livery Value');

            modal.addComponents(
              new ActionRowBuilder().addComponents(
                new TextInputBuilder()
                  .setCustomId('livery_price')
                  .setLabel('Livery Price (e.g. 5 for 5M)')
                  .setPlaceholder('e.g. 5')
                  .setStyle(TextInputStyle.Short)
                  .setRequired(true)
              )
            );
            await interaction.showModal(modal);
            return;
          } else {
            session.livery = false;
            session.liveryPrice = { min: 0, max: 0, isPlus: false };
            await interaction.update(buildPriceConfigurator(sessionId, session, car));
            return;
          }
        }

        session[field] = !session[field];
        await interaction.update(buildPriceConfigurator(sessionId, session, car));
        return;
      }

      if (id.startsWith('pcalc_tune_')) {
        const sessionId = id.replace('pcalc_tune_', '');
        const session = priceCalcSessions.get(sessionId);
        if (!session) {
          await interaction.reply({
            content: '❌ This price calculator session expired. Run `/car-price` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const car = store.cars[session.carId];
        session.tune = session.tune === 'MAX' ? 'STOCK' : 'MAX';
        await interaction.update(buildPriceConfigurator(sessionId, session, car));
        return;
      }

      if (id.startsWith('pcalc_finish_')) {
        const sessionId = id.replace('pcalc_finish_', '');
        const session = priceCalcSessions.get(sessionId);
        if (!session) {
          await interaction.reply({
            content: '❌ This price calculator session expired. Run `/car-price` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const car = store.cars[session.carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car no longer exists.', flags: MessageFlags.Ephemeral });
          return;
        }

        const finalEmbed = buildFinalPriceEmbed(car, session);
        priceCalcSessions.delete(sessionId);

        // Post the final generated price panel PUBLICLY so everyone in the channel can see it
        await interaction.reply({
          content: `Requested by <@${interaction.user.id}>`,
          embeds: [finalEmbed]
        });
        return;
      }
    }

    // ------------------------------------------
    // D. SELECT MENU INTERACTIONS
    // ------------------------------------------
    if (interaction.isStringSelectMenu()) {
      const id = interaction.customId;

      if (id === 'select_edit_car') {
        const carId = interaction.values[0];
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }

        const row1 = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId(`edit_basic_${carId}`)
            .setLabel('Name & Image')
            .setStyle(ButtonStyle.Primary),
          new ButtonBuilder()
            .setCustomId(`edit_addons_${carId}`)
            .setLabel('Add-on Prices')
            .setStyle(ButtonStyle.Primary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_1`)
            .setLabel('Stage 1')
            .setStyle(ButtonStyle.Secondary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_2`)
            .setLabel('Stage 2')
            .setStyle(ButtonStyle.Secondary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_3`)
            .setLabel('Stage 3')
            .setStyle(ButtonStyle.Secondary)
        );

        const row2 = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_4`)
            .setLabel('Stage 4')
            .setStyle(ButtonStyle.Secondary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_5`)
            .setLabel('Stage 5')
            .setStyle(ButtonStyle.Secondary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_6`)
            .setLabel('Stage 6')
            .setStyle(ButtonStyle.Secondary),
          new ButtonBuilder()
            .setCustomId(`edit_stage_${carId}_7`)
            .setLabel('Stage 7')
            .setStyle(ButtonStyle.Secondary)
        );

        await interaction.update({
          content: `✏️ Editing **${car.name}** — Choose which section to update:`,
          components: [row1, row2]
        });
        return;
      }

      if (id === 'select_delete_car') {
        const carId = interaction.values[0];
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId(`confirm_delete_${carId}`)
            .setLabel('Confirm Delete')
            .setEmoji('🗑️')
            .setStyle(ButtonStyle.Danger),
          new ButtonBuilder()
            .setCustomId('cancel_delete')
            .setLabel('Cancel')
            .setStyle(ButtonStyle.Secondary)
        );

        await interaction.update({
          content: `⚠️ Are you sure you want to permanently delete **${car.name}**?`,
          components: [row]
        });
        return;
      }
    }

    // ------------------------------------------
    // E. MODAL SUBMISSIONS
    // ------------------------------------------
    if (interaction.isModalSubmit()) {
      const id = interaction.customId;

      // 1. Add Car Step 1 Modal
      if (id === 'modal_add_step1') {
        const carName = interaction.fields.getTextInputValue('car_name').trim();
        const rawImage = interaction.fields.getTextInputValue('car_image').trim();
        const validImage = sanitizeImageUrl(rawImage);

        const session = {
          name: carName,
          image: validImage,
          addons: {
            police: { min: 0, max: 0, isPlus: false, raw: '' },
            rainbowSmoke: { min: 0, max: 0, isPlus: false, raw: '' },
            premium: { min: 0, max: 0, isPlus: false, raw: '' },
            coating: { min: 0, max: 0, isPlus: false, raw: '' }
          },
          stages: {}
        };
        addWizardSessions.set(interaction.user.id, session);

        const embed = new EmbedBuilder()
          .setColor(0x2f855a)
          .setTitle(`✅ Step 1 Complete: ${carName}`)
          .setDescription(
            `**Car Name:** ${carName}\n` +
            `**Image URL:** ${validImage ? validImage : '*None / Skipped*'}\n\n` +
            `Click **Next ➡️** below to enter Add-on prices (Police, Rainbow Smoke, Premium, Coating).`
          );

        if (validImage) {
          embed.setThumbnail(validImage);
        }

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId('wizard_open_addons')
            .setLabel('Next')
            .setEmoji('➡️')
            .setStyle(ButtonStyle.Primary)
        );

        await interaction.reply({
          embeds: [embed],
          components: [row],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 2. Add Car Step 2 Modal (Add-ons)
      if (id === 'modal_add_addons') {
        const session = addWizardSessions.get(interaction.user.id);
        if (!session) {
          await interaction.reply({
            content: '❌ Session expired. Please run `/admin-cars` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        session.addons = {
          police: parsePriceInput(interaction.fields.getTextInputValue('price_police')),
          rainbowSmoke: parsePriceInput(interaction.fields.getTextInputValue('price_rbsmoke')),
          premium: parsePriceInput(interaction.fields.getTextInputValue('price_premium')),
          coating: parsePriceInput(interaction.fields.getTextInputValue('price_coating'))
        };

        const embed = new EmbedBuilder()
          .setColor(0x2f855a)
          .setTitle(`✅ Step 2 Complete: ${session.name} Add-ons`)
          .setDescription(
            `• **Police:** ${formatPriceRange(session.addons.police)}\n` +
            `• **Rainbow Smoke:** ${formatPriceRange(session.addons.rainbowSmoke)}\n` +
            `• **Premium:** ${formatPriceRange(session.addons.premium)}\n` +
            `• **Coating:** ${formatPriceRange(session.addons.coating)}\n\n` +
            `Click **Next: Stage 1 ➡️** to enter Stage speeds & prices.`
          );

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId('wizard_open_stage_1')
            .setLabel('Next: Stage 1')
            .setEmoji('➡️')
            .setStyle(ButtonStyle.Primary),
          new ButtonBuilder()
            .setCustomId('wizard_finish_now')
            .setLabel('Save Car Now')
            .setEmoji('✅')
            .setStyle(ButtonStyle.Success)
        );

        await interaction.reply({
          embeds: [embed],
          components: [row],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 3. Add Car Stage 1-6 Modals
      if (id.startsWith('modal_add_stage_') && id !== 'modal_add_stage_7') {
        const stageNum = parseInt(id.replace('modal_add_stage_', ''), 10);
        const session = addWizardSessions.get(interaction.user.id);
        if (!session) {
          await interaction.reply({
            content: '❌ Session expired. Please run `/admin-cars` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        const price = parsePriceInput(interaction.fields.getTextInputValue('stage_price'));
        const noTurbo = formatSpeedInput(interaction.fields.getTextInputValue('speed_no_turbo'));
        const withTurbo = formatSpeedInput(interaction.fields.getTextInputValue('speed_with_turbo'));

        session.stages[String(stageNum)] = { price, noTurbo, withTurbo };

        const nextStage = stageNum + 1;
        const embed = new EmbedBuilder()
          .setColor(0x2f855a)
          .setTitle(`✅ Stage ${stageNum} Saved for ${session.name}`)
          .setDescription(
            `**Price:** ${formatPriceRange(price, true)}\n` +
            `**Top Speed (No Turbo):** ${noTurbo}\n` +
            `**Top Speed (With Turbo):** ${withTurbo}\n\n` +
            `Click below to continue to **Stage ${nextStage}** or save now.`
          );

        const row = new ActionRowBuilder().addComponents(
          new ButtonBuilder()
            .setCustomId(`wizard_open_stage_${nextStage}`)
            .setLabel(`Next: Stage ${nextStage}`)
            .setEmoji('➡️')
            .setStyle(ButtonStyle.Primary),
          new ButtonBuilder()
            .setCustomId('wizard_finish_now')
            .setLabel('Save Car Now')
            .setEmoji('✅')
            .setStyle(ButtonStyle.Success)
        );

        await interaction.reply({
          embeds: [embed],
          components: [row],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 4. Add Car Stage 7 Modal (Final Step)
      if (id === 'modal_add_stage_7') {
        const session = addWizardSessions.get(interaction.user.id);
        if (!session) {
          await interaction.reply({
            content: '❌ Session expired. Please run `/admin-cars` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }

        const price = parsePriceInput(interaction.fields.getTextInputValue('stage_price'));
        session.stages['7'] = { price };

        const carId = `car_${Date.now()}`;
        store.cars[carId] = session;
        await saveDatabase();
        addWizardSessions.delete(interaction.user.id);

        await interaction.reply({
          content: `🎉 **${session.name}** has been added to the database!`,
          embeds: [buildCarInfoEmbed(session)],
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 5. Edit Car Modals
      if (id.startsWith('modal_edit_basic_')) {
        const carId = id.replace('modal_edit_basic_', '');
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        car.name = interaction.fields.getTextInputValue('car_name').trim();
        car.image = sanitizeImageUrl(interaction.fields.getTextInputValue('car_image'));
        await saveDatabase();
        await interaction.reply({
          content: `✅ Updated basic info for **${car.name}**!`,
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (id.startsWith('modal_edit_addons_')) {
        const carId = id.replace('modal_edit_addons_', '');
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        car.addons = {
          police: parsePriceInput(interaction.fields.getTextInputValue('price_police')),
          rainbowSmoke: parsePriceInput(interaction.fields.getTextInputValue('price_rbsmoke')),
          premium: parsePriceInput(interaction.fields.getTextInputValue('price_premium')),
          coating: parsePriceInput(interaction.fields.getTextInputValue('price_coating'))
        };
        await saveDatabase();
        await interaction.reply({
          content: `✅ Updated add-on prices for **${car.name}**!`,
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      if (id.startsWith('modal_edit_stage_')) {
        const rest = id.replace('modal_edit_stage_', '');
        const lastUnderscore = rest.lastIndexOf('_');
        const stageNum = rest.slice(lastUnderscore + 1);
        const carId = rest.slice(0, lastUnderscore);
        const car = store.cars[carId];
        if (!car) {
          await interaction.reply({ content: '❌ Car not found.', flags: MessageFlags.Ephemeral });
          return;
        }
        if (!car.stages) car.stages = {};
        const price = parsePriceInput(interaction.fields.getTextInputValue('stage_price'));
        if (stageNum === '7') {
          car.stages['7'] = { price };
        } else {
          const noTurbo = formatSpeedInput(interaction.fields.getTextInputValue('speed_no_turbo'));
          const withTurbo = formatSpeedInput(interaction.fields.getTextInputValue('speed_with_turbo'));
          car.stages[stageNum] = { price, noTurbo, withTurbo };
        }
        await saveDatabase();
        await interaction.reply({
          content: `✅ Updated **Stage ${stageNum}** for **${car.name}**!`,
          flags: MessageFlags.Ephemeral
        });
        return;
      }

      // 6. Livery Modal inside /car-price
      if (id.startsWith('modal_livery_')) {
        const sessionId = id.replace('modal_livery_', '');
        const session = priceCalcSessions.get(sessionId);
        if (!session) {
          await interaction.reply({
            content: '❌ Calculator session expired. Run `/car-price` again.',
            flags: MessageFlags.Ephemeral
          });
          return;
        }
        const car = store.cars[session.carId];
        session.livery = true;
        session.liveryPrice = parsePriceInput(interaction.fields.getTextInputValue('livery_price'));

        await interaction.reply({
          ...buildPriceConfigurator(sessionId, session, car),
          flags: MessageFlags.Ephemeral
        });
        return;
      }
    }
  } catch (err) {
    console.error('❌ Interaction Error:', err);
    const msg = `⚠️ Error: ${err.message || 'An unexpected error occurred.'}`;
    try {
      if (interaction.replied || interaction.deferred) {
        await interaction.followUp({ content: msg, flags: MessageFlags.Ephemeral });
      } else if (interaction.isRepliable()) {
        await interaction.reply({ content: msg, flags: MessageFlags.Ephemeral });
      }
    } catch (replyErr) {
      console.error('Failed to send error message:', replyErr);
    }
  }
});

// ==========================================
// 9. START BOT
// ==========================================
(async () => {
  await initDatabase();
  if (!TOKEN || !CLIENT_ID) {
    console.error('❌ Missing DISCORD_TOKEN or CLIENT_ID in environment variables!');
    process.exit(1);
  }
  await client.login(TOKEN);
})();
