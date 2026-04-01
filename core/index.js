/**
 * CodePet 核心逻辑 — 所有平台共用
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');

const PET_DIR = path.join(os.homedir(), '.codepet');
const PET_FILE = path.join(PET_DIR, 'pet.json');

// ── 6 大角色 ──
const CHARACTERS = [
  { id: 'bibilabu',    name: '比比拉布', weight: 28 },
  { id: 'bagayalu',    name: '八嘎呀路', weight: 28 },
  { id: 'bababoyi',    name: '巴巴博一', weight: 20 },
  { id: 'waibibabu',   name: '歪比巴卜', weight: 12 },
  { id: 'gugugaga',    name: '咕咕嘎嘎', weight: 8 },
  { id: 'wodedaodun',  name: '我的刀盾', weight: 4 },
];

const RARITIES = [
  { name: '普通', prob: 60, stars: 1 },
  { name: '优秀', prob: 25, stars: 2 },
  { name: '稀有', prob: 10, stars: 3 },
  { name: '史诗', prob: 4,  stars: 4 },
  { name: '传奇', prob: 1,  stars: 5 },
];

const EYES = ['·', '✦', '×', '◉', '@', '°'];

const HATS = [
  null, '小皇冠', '高礼帽', '螺旋桨帽', '光环', '法师帽', '毛线帽', '头顶小鸭',
];

const ACCESSORIES = ['围巾', '墨镜', '蝴蝶结', '小花', '耳机'];

const STATS = ['调试力', '耐心值', '混沌值', '智慧值', '毒舌值'];

const LEVELS = [
  { level: 1, exp: 0,    title: '刚孵化的小家伙' },
  { level: 2, exp: 50,   title: '好奇的探索者' },
  { level: 3, exp: 150,  title: '靠谱的伙伴' },
  { level: 4, exp: 350,  title: '老练的搭子' },
  { level: 5, exp: 600,  title: '编程大师的宠物' },
  { level: 6, exp: 1000, title: '传说中的存在' },
];

// ── 确定性随机（Mulberry32 PRNG）──
function mulberry32(seed) {
  let t = seed | 0;
  return function () {
    t = (t + 0x6D2B79F5) | 0;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return Math.abs(hash);
}

// ── 孵化 ──
function hatch(userId) {
  const seed = hashString(userId + 'codepet-2026');
  const rng = mulberry32(seed);

  // 选角色（加权随机）
  const totalWeight = CHARACTERS.reduce((s, c) => s + c.weight, 0);
  let roll = rng() * totalWeight;
  let character = CHARACTERS[0];
  for (const c of CHARACTERS) {
    roll -= c.weight;
    if (roll <= 0) { character = c; break; }
  }

  // 选稀有度
  roll = rng() * 100;
  let rarity = RARITIES[0];
  for (const r of RARITIES) {
    roll -= r.prob;
    if (roll <= 0) { rarity = r; break; }
  }

  // 眼睛
  const eye = EYES[Math.floor(rng() * EYES.length)];

  // 帽子（优秀及以上）
  let hat = null;
  if (rarity.stars >= 2) {
    const hatsForRarity = HATS.filter(h => h !== null);
    hat = hatsForRarity[Math.floor(rng() * hatsForRarity.length)];
  }

  // 配饰（稀有及以上）
  let accessory = null;
  if (rarity.stars >= 3) {
    accessory = ACCESSORIES[Math.floor(rng() * ACCESSORIES.length)];
  }

  // 闪光（1%）
  const shiny = rng() < 0.01;

  // 属性（1 巅峰 + 1 短板 + 3 随机）
  const statValues = {};
  const baseMin = 10 + rarity.stars * 10;
  const shuffled = [...STATS].sort(() => rng() - 0.5);
  shuffled.forEach((stat, i) => {
    if (i === 0) statValues[stat] = Math.floor(80 + rng() * 20);      // 巅峰
    else if (i === 1) statValues[stat] = Math.floor(5 + rng() * 25);  // 短板
    else statValues[stat] = Math.floor(baseMin + rng() * (80 - baseMin));
  });

  const pet = {
    version: 2,
    seed: userId,
    name: character.name,
    character: character.id,
    rarity: rarity.name,
    stars: rarity.stars,
    eye,
    hat,
    accessory,
    shiny,
    stats: statValues,
    level: 1,
    exp: 0,
    feedCount: 0,
    patCount: 0,
    mood: '清醒',
    hatchedAt: new Date().toISOString(),
    muted: false,
  };

  return pet;
}

// ── 存读 ──
function ensureDir() {
  if (!fs.existsSync(PET_DIR)) {
    fs.mkdirSync(PET_DIR, { recursive: true });
  }
}

function savePet(pet) {
  ensureDir();
  fs.writeFileSync(PET_FILE, JSON.stringify(pet, null, 2), 'utf-8');
}

function loadPet() {
  if (!fs.existsSync(PET_FILE)) return null;
  return JSON.parse(fs.readFileSync(PET_FILE, 'utf-8'));
}

function hasPet() {
  return fs.existsSync(PET_FILE);
}

// ── 经验与升级 ──
function addExp(pet, amount) {
  pet.exp += amount;
  const oldLevel = pet.level;
  for (const l of LEVELS) {
    if (pet.exp >= l.exp) pet.level = l.level;
  }
  const leveledUp = pet.level > oldLevel;
  savePet(pet);
  return { leveledUp, newLevel: pet.level };
}

function getLevelTitle(level) {
  const l = LEVELS.find(x => x.level === level);
  return l ? l.title : '';
}

function getExpForNextLevel(level) {
  const next = LEVELS.find(x => x.level === level + 1);
  return next ? next.exp : null;
}

// ── 互动 ──
function pat(pet) {
  pet.patCount++;
  return addExp(pet, 3);
}

function feed(pet) {
  pet.feedCount++;
  return addExp(pet, 8);
}

module.exports = {
  CHARACTERS, RARITIES, EYES, HATS, ACCESSORIES, STATS, LEVELS,
  PET_DIR, PET_FILE,
  hatch, savePet, loadPet, hasPet,
  addExp, getLevelTitle, getExpForNextLevel,
  pat, feed,
};
