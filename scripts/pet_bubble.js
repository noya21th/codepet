#!/usr/bin/env node
/**
 * 宠物冒泡 — 被 hooks 调用，30% 概率输出一句宠物的话
 * 输出到 stderr 让 Claude 看到（作为 hook 反馈）
 *
 * 增强：根据 lastInteraction 自动更新 mood（sleep / worry），
 *       台词根据 mood 上下文选择。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const PET_FILE = path.join(os.homedir(), '.codepet', 'pet.json');

if (!fs.existsSync(PET_FILE)) process.exit(0);

let pet;
try {
  pet = JSON.parse(fs.readFileSync(PET_FILE, 'utf-8'));
} catch {
  process.exit(0);
}
if (pet.muted) process.exit(0);

// ── 根据 lastInteraction 更新 mood ──
const now = Date.now();
const last = pet.lastInteraction ? new Date(pet.lastInteraction).getTime() : now;
const hoursAgo = (now - last) / (1000 * 60 * 60);

let moodChanged = false;
if (hoursAgo > 6 && pet.mood !== 'worry') {
  pet.mood = 'worry';
  moodChanged = true;
} else if (hoursAgo > 2 && hoursAgo <= 6 && pet.mood !== 'sleep') {
  pet.mood = 'sleep';
  moodChanged = true;
}

// 如果刚回来（< 2h），恢复清醒
if (hoursAgo <= 2 && (pet.mood === 'sleep' || pet.mood === 'worry')) {
  pet.mood = '清醒';
  moodChanged = true;
}

// 更新 lastInteraction（每次冒泡脚本被调用 = 有互动）
pet.lastInteraction = new Date().toISOString();

if (moodChanged || !pet.lastInteraction) {
  try {
    fs.writeFileSync(PET_FILE, JSON.stringify(pet, null, 2), 'utf-8');
  } catch {
    // 写入失败不影响冒泡
  }
}

// 30% 概率冒泡
if (Math.random() > 0.3) process.exit(0);

// ── 心情专属台词 ──
const SLEEP_LINES = {
  bibilabu:   ['zzZ……香蕉皮盖好了……', '（梦见了一根巨大的香蕉）', '别吵……让我再睡五分钟……'],
  bagayalu:   ['zzZ……', '（安静地打盹中）', '……水……到渠成……zzZ'],
  wodedaodun: ['zzZ……zzZ……zzZ……', '（翻了个身继续睡）', '（呼噜声）……少个分号……'],
  bababoyi:   ['（闭着大眼睛睡觉）', 'zzZ……咕……', '（眼皮在抖，估计在做梦）'],
  waibibabu:  ['哥先眯一会儿……', 'zzZ……年轻人别急……zzZ', '（打鼾中）……先写测试……'],
  gugugaga:   ['嘎……zzZ……', '（蜷成一团睡着了）', '……嘎嘎……zzZ'],
};

const WORRY_LINES = {
  bibilabu:   ['你去哪了？我的香蕉皮都干了……', '是不是不要我了……', '（焦虑地搓香蕉皮）'],
  bagayalu:   ['……你还在吗？', '等了好久……没事，我不急。（其实很急）', '水到渠成……但水呢？'],
  wodedaodun: ['醒了好久了……你怎么还不来？', '是不是出什么事了？', '（担心地看着门口）'],
  bababoyi:   ['（大眼睛里有泪光）', '咕……？你回来了吗……', '一直在等你……'],
  waibibabu:  ['哥等你好久了，知道吗？', '以为你把哥忘了……', '回来就好……回来就好。'],
  gugugaga:   ['嘎……嘎嘎？（你在哪里）', '（不安地来回踱步）', '嘎！（终于回来了！）'],
};

// ── 普通台词（清醒） ──
const NORMAL_LINES = {
  bibilabu: [
    '我穿这身不是因为我想穿。',
    '香蕉直觉告诉我，你写得不错。',
    '没事，我穿成这样都没放弃生活。',
    '今天穿香蕉皮，明天穿西瓜皮。',
  ],
  bagayalu: [
    '没事。再来一次就好。',
    '你急什么？',
    '嗯……我虽然不动，但我看到了。',
    '水到渠成。',
  ],
  wodedaodun: [
    'zzZ……啊？还在写？',
    '（梦话）……少个分号……zzZ',
    '躺平不代表不思考。',
    '你的代码比我还困。',
  ],
  bababoyi: [
    '（一动不动地盯着你写代码）',
    '咕？',
    '我的大眼睛不是摆设。',
    '从架构层面来看——算了。',
  ],
  waibibabu: [
    '这代码谁写的？哦，你写的。',
    '慌什么。哥在呢。',
    '年轻人，听哥一句，先写测试。',
    '哥以前也写过这种 bug。',
  ],
  gugugaga: [
    '嘎？你认真的？',
    '嘎嘎嘎嘎嘎！',
    '……嘎。（继续吧）',
    '我的刘海下面藏着 debug 之眼。',
  ],
};

// ── 根据 mood 选台词库 ──
let linesMap;
if (pet.mood === 'sleep') {
  linesMap = SLEEP_LINES;
} else if (pet.mood === 'worry') {
  linesMap = WORRY_LINES;
} else {
  linesMap = NORMAL_LINES;
}

const lines = linesMap[pet.character] || linesMap.gugugaga;
const line = lines[Math.floor(Math.random() * lines.length)];
const name = pet.nickname || pet.name;

// ── 极小概率弹出宠物照片（可在 pet.json 里设 popupChance 调整，默认 2%）──
const surpriseOn = pet.surpriseEnabled !== false;
const popupChance = surpriseOn ? (pet.popupChance !== undefined ? pet.popupChance : 0.02) : 0;
if (popupChance > 0 && Math.random() < popupChance) {
  const scenes = ['normal', 'happy', 'eat', 'pet', 'sleep'];
  const scene = scenes[Math.floor(Math.random() * scenes.length)];
  try {
    const { spawn } = require('child_process');
    const codepetBin = path.join(__dirname, '..', 'bin', 'codepet.js');
    spawn('node', [codepetBin, 'popup', scene], { detached: true, stdio: 'ignore' }).unref();
  } catch {}
  process.exit(0); // 弹了照片就不再说话
}

// ── 特殊事件 ──

// 升级提醒
if (pet.level > 1) {
  const LEVELS = [0, 50, 150, 350, 600, 1000];
  const prevExp = pet.exp - 5;
  for (let i = 1; i < LEVELS.length; i++) {
    if (prevExp < LEVELS[i] && pet.exp >= LEVELS[i]) {
      console.error(`\n🎉 ${name} 升级到 Lv.${pet.level} 了！说"拍照"给它留个纪念吧。`);
      process.exit(0);
    }
  }
}

// 久别重逢
if (moodChanged && pet.mood === '清醒') {
  const wasMood = hoursAgo > 6 ? 'worry' : (hoursAgo > 2 ? 'sleep' : null);
  if (wasMood === 'worry') {
    console.error(`\n💕 ${name} 等你好久了！说"摸摸"安慰一下它吧。`);
    process.exit(0);
  }
}

// 输出气泡到 stderr（hook 反馈格式）
console.error(`\n┌${'─'.repeat(name.length * 2 + line.length + 6)}┐`);
console.error(`│ 💬 ${name}：${line} │`);
console.error(`└${'─'.repeat(name.length * 2 + line.length + 6)}┘`);
