#!/usr/bin/env node
/**
 * codepet CLI — 一键安装与管理
 *
 * npx codepet setup     → 自动检测环境，安装到对应平台
 * npx codepet show      → 终端显示宠物
 * npx codepet hatch     → 孵化
 * npx codepet pat       → 撸
 * npx codepet feed      → 喂
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');
const core = require('../core');

const SPRITES_DIR = path.join(__dirname, '..', 'sprites');
const SKILL_SRC = path.join(__dirname, '..', 'adapters', 'skill', 'SKILL.md');

const cmd = process.argv[2] || 'help';
const arg = process.argv[3];
// --图片 模式：生成 PNG 让 CC 用 Read 工具显示
const imageMode = process.argv.includes('--图片') || process.argv.includes('--image');
const RENDER_WIDTH = 30;

// ── 平台检测 ──
function detectPlatforms() {
  const found = [];

  // Claude Code
  const ccSkillDir = path.join(os.homedir(), '.claude', 'skills');
  if (fs.existsSync(path.join(os.homedir(), '.claude'))) {
    found.push({ id: 'claude-code', name: 'Claude Code', dir: ccSkillDir });
  }

  // Codex (OpenAI)
  const codexDir = path.join(os.homedir(), '.codex');
  if (fs.existsSync(codexDir)) {
    found.push({ id: 'codex', name: 'Codex', dir: path.join(codexDir, 'skills') });
  }

  // Cursor
  const cursorDir = path.join(os.homedir(), '.cursor');
  if (fs.existsSync(cursorDir)) {
    found.push({ id: 'cursor', name: 'Cursor', dir: null });
  }

  // VS Code
  const vscodeDir = path.join(os.homedir(), '.vscode');
  if (fs.existsSync(vscodeDir)) {
    found.push({ id: 'vscode', name: 'VS Code', dir: null });
  }

  // Kiro
  const kiroDir = path.join(os.homedir(), '.kiro');
  if (fs.existsSync(kiroDir)) {
    found.push({ id: 'kiro', name: 'Kiro', dir: null });
  }

  // OpenClaw
  const openclawDir = path.join(os.homedir(), '.openclaw');
  if (fs.existsSync(openclawDir)) {
    found.push({ id: 'openclaw', name: 'OpenClaw', dir: path.join(openclawDir, 'skills') });
  }

  // CodeBuddy
  const codebuddyDir = path.join(os.homedir(), '.codebuddy');
  if (fs.existsSync(codebuddyDir)) {
    found.push({ id: 'codebuddy', name: 'CodeBuddy', dir: path.join(codebuddyDir, 'skills') });
  }

  // Antigravity
  const antigravityDir = path.join(os.homedir(), '.antigravity');
  if (fs.existsSync(antigravityDir)) {
    found.push({ id: 'antigravity', name: 'Antigravity', dir: path.join(antigravityDir, 'skills') });
  }

  // OpenCode
  const opencodeDir = path.join(os.homedir(), '.opencode');
  if (fs.existsSync(opencodeDir)) {
    found.push({ id: 'opencode', name: 'OpenCode', dir: path.join(opencodeDir, 'skills') });
  }

  return found;
}

// ── 安装 Skill 文件到目标目录 ──
function installSkill(targetDir, platformName) {
  const destDir = path.join(targetDir, 'codepet');
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }

  // 复制 SKILL.md
  const skillSrc = SKILL_SRC;
  if (fs.existsSync(skillSrc)) {
    fs.copyFileSync(skillSrc, path.join(destDir, 'SKILL.md'));
  }

  // 复制精灵图片
  if (fs.existsSync(SPRITES_DIR)) {
    const spriteDestDir = path.join(destDir, 'sprites');
    if (!fs.existsSync(spriteDestDir)) {
      fs.mkdirSync(spriteDestDir, { recursive: true });
    }
    const files = fs.readdirSync(SPRITES_DIR).filter(f => f.endsWith('.png'));
    for (const file of files) {
      fs.copyFileSync(
        path.join(SPRITES_DIR, file),
        path.join(spriteDestDir, file)
      );
    }
  }

  console.log(`  ✓ ${platformName} — 已安装到 ${destDir}`);
  return true;
}

// ── 命令处理 ──

function setup() {
  console.log('\n  🐾 CodePet 安装向导\n');
  console.log('  正在检测已安装的编程工具...\n');

  const platforms = detectPlatforms();

  if (platforms.length === 0) {
    console.log('  未检测到支持的编程工具。');
    console.log('  支持: Claude Code, Codex, Cursor, VS Code, Kiro,');
    console.log('        CodeBuddy, OpenClaw, Antigravity, OpenCode\n');
    return;
  }

  console.log(`  检测到 ${platforms.length} 个平台:\n`);

  let installed = 0;
  const vscodeFamily = [];

  for (const p of platforms) {
    if (p.dir) {
      // Skill 类平台 → 复制 SKILL.md
      installSkill(p.dir, p.name);
      installed++;
    } else {
      // VS Code 系 → 记录，后面统一提示
      vscodeFamily.push(p.name);
    }
  }

  if (vscodeFamily.length > 0) {
    console.log(`\n  📦 ${vscodeFamily.join(' / ')} 请通过扩展商店安装:`);
    console.log('     搜索 "CodePet" 或运行:');
    console.log('     code --install-extension codepet.codepet\n');
  }

  // 确保宠物数据目录存在
  core.ensureDir ? null : null;
  const petDir = path.join(os.homedir(), '.codepet');
  if (!fs.existsSync(petDir)) {
    fs.mkdirSync(petDir, { recursive: true });
  }

  // 复制渲染脚本
  const renderSrc = path.join(__dirname, '..', 'scripts', 'img2terminal.py');
  const renderDst = path.join(petDir, 'render.py');
  if (fs.existsSync(renderSrc)) {
    fs.copyFileSync(renderSrc, renderDst);
  }

  console.log(`\n  ✅ 安装完成！共 ${installed} 个平台。`);
  console.log('  在任意支持的工具里输入 /pet 开始养宠物。\n');
}

// ── 渲染像素画 ──
function renderSprite(character, variant) {
  variant = variant || 'normal';

  if (imageMode) {
    // 图片模式：生成 PNG，输出路径
    const renderImgScript = path.join(__dirname, '..', 'scripts', 'render_to_image.py');
    if (fs.existsSync(renderImgScript)) {
      try {
        const imgPath = execSync(`python3 "${renderImgScript}" "${character}" "${variant}"`, { encoding: 'utf-8' }).trim();
        console.log(`[图片:${imgPath}]`);
      } catch (e) {}
    }
  } else {
    // 终端模式：彩色像素画
    const renderScript = path.join(__dirname, '..', 'scripts', 'img2terminal.py');
    let spritePath = path.join(SPRITES_DIR, character, `${variant}.png`);
    if (!fs.existsSync(spritePath)) {
      spritePath = path.join(SPRITES_DIR, `${character}.png`);
    }
    if (fs.existsSync(spritePath) && fs.existsSync(renderScript)) {
      try {
        const output = execSync(`python3 "${renderScript}" "${spritePath}" ${RENDER_WIDTH}`, { encoding: 'utf-8' });
        console.log(output);
      } catch (e) {}
    }
  }
}

function showStats(pet) {
  const stars = '★'.repeat(pet.stars) + '☆'.repeat(5 - pet.stars);
  const title = core.getLevelTitle(pet.level);
  const nextExp = core.getExpForNextLevel(pet.level);

  console.log(`  ${pet.name}${pet.shiny ? ' ✧' : ''}`);
  console.log(`  ${stars} ${pet.rarity}`);
  console.log(`  Lv.${pet.level} ${title} · 经验 ${pet.exp}${nextExp ? '/' + nextExp : '/MAX'}`);
  if (pet.hat) console.log(`  帽子: ${pet.hat}`);
  if (pet.accessory) console.log(`  配饰: ${pet.accessory}`);
  console.log();
  for (const [stat, val] of Object.entries(pet.stats)) {
    const bar = '█'.repeat(Math.floor(val / 10)) + '░'.repeat(10 - Math.floor(val / 10));
    console.log(`  ${stat} ${bar} ${val}`);
  }
  console.log();
}

function show() {
  const pet = core.loadPet();
  if (!pet) {
    console.log('\n  还没有宠物。运行 宠物 孵化\n');
    return;
  }
  renderSprite(pet.character, 'normal');
  showStats(pet);
}

function doHatch() {
  const readline = require('readline');

  if (core.hasPet()) {
    const existing = core.loadPet();
    console.log(`\n  ⚠️  你已经有 ${existing.name} 了。重新孵化会覆盖它。`);
    console.log('  如果确定，运行: 宠物 再见我依然爱你\n');
    if (!process.argv.includes('--force') && cmd !== '再见我依然爱你') return;
  }

  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

  const ask = (q) => new Promise(resolve => rl.question(q, resolve));

  (async () => {
    console.log('\n  ─────────────────────────────────');
    console.log('  🥚 CodePet 孵化仪式');
    console.log('  ─────────────────────────────────\n');
    console.log('  有一颗蛋正在等你。');
    console.log('  它从你打下第一行代码的那天起，就一直在这里。\n');

    // 第一步：给宠物起名
    const petNickname = await ask('  给它起个名字吧 > ');
    if (!petNickname.trim()) {
      console.log('  它需要一个名字。下次再来吧。\n');
      rl.close();
      return;
    }

    // 第二步：承诺
    console.log(`\n  「${petNickname}」……好名字。\n`);
    console.log('  在它破壳之前，你需要签一份承诺：');
    console.log('  ┌──────────────────────────────────┐');
    console.log('  │                                  │');
    console.log('  │  无论 bug 多难修，               │');
    console.log('  │  无论 deadline 多紧，            │');
    console.log('  │  无论代码跑不跑得通，            │');
    console.log(`  │  我都不会删除${petNickname}、不会抛弃它。 │`);
    console.log('  │                                  │');
    console.log('  │  签名：_______________           │');
    console.log('  │                                  │');
    console.log('  └──────────────────────────────────┘\n');

    const promise = await ask('  输入「我承诺」签署 > ');
    if (!promise.includes('承诺') && !promise.includes('好') && !promise.includes('y') && !promise.includes('是') && !promise.includes('签')) {
      console.log('\n  蛋安静地等着，不着急。你什么时候准备好了，再来。\n');
      rl.close();
      return;
    }

    // 第三步：孵化动画
    console.log('\n  ......');
    console.log('  🥚 蛋感受到了你的承诺。它在微微颤动...');
    console.log('  🥚💫 裂了！有什么要出来了！');
    console.log('\n  ✨✨✨✨✨✨✨✨✨✨✨✨✨✨\n');

    // 执行孵化
    const userId = petNickname;
    const pet = core.hatch(userId);
    pet.nickname = petNickname;  // 用户起的名字
    core.savePet(pet);

    // 展示宠物
    renderSprite(pet.character, 'happy');

    console.log(`  ✨ ${petNickname}（${pet.name}）来了。`);
    console.log(`  ${'★'.repeat(pet.stars)} ${pet.rarity}\n`);

    showStats(pet);

    console.log(`  ${petNickname} 看着你，好像认识你很久了。`);
    console.log(`  从现在起，它就是你的编程搭子了。`);
    console.log('  不离不弃。\n');

    rl.close();
  })();
}

function doPat() {
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  const { leveledUp } = core.pat(pet);
  console.log(`\n     ♥   ♥`);
  console.log(`   ♥  ♥ ♥  ♥`);
  console.log(`     ♥   ♥\n`);
  renderSprite(pet.character, 'pet');
  console.log(`  ${pet.name} 开心得不得了！(+3 经验)`);
  if (leveledUp) console.log(`  🎉 升级到 Lv.${pet.level}！`);
  console.log(`  经验: ${pet.exp}/${core.getExpForNextLevel(pet.level) || 'MAX'}\n`);
}

function doFeed() {
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  const { leveledUp } = core.feed(pet);
  renderSprite(pet.character, 'eat');
  console.log(`  ${pet.name} 吃得很开心！(+8 经验)`);
  if (leveledUp) console.log(`  🎉 升级到 Lv.${pet.level}！`);
  console.log(`  经验: ${pet.exp}/${core.getExpForNextLevel(pet.level) || 'MAX'}\n`);
}

function doCard() {
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  const cardScript = path.join(__dirname, '..', 'scripts', 'pet_card.py');
  if (fs.existsSync(cardScript)) {
    try {
      execSync(`python3 "${cardScript}"`, { encoding: 'utf-8', stdio: 'inherit' });
      // 确保弹出 Preview
      const cardPath = path.join(os.homedir(), '.codepet', 'card.png');
      execSync(`open "${cardPath}"`, { stdio: 'ignore' });
    } catch (e) {
      console.log('  卡片生成失败。');
    }
  }
}

function help() {
  console.log(`
  🐾 CodePet — 在编程软件里养电子宠物

  用法:
    宠物 安装        一键安装到所有编程工具
    宠物 孵化        孵化新宠物
    宠物 看看        查看宠物
    宠物 摸摸        撸宠物
    宠物 喂它        喂宠物
    宠物 卡片        生成分享卡片
    宠物 帮助        显示此帮助

  支持平台:
    Claude Code · Codex · Cursor · VS Code · Kiro
    CodeBuddy · OpenClaw · Antigravity · OpenCode
  `);
}

// ── 入口（中英文都支持）──
const CMD_MAP = {
  'setup': setup, '安装': setup,
  'show': show, '看看': show, '看': show, '状态': show,
  'hatch': doHatch, '孵化': doHatch, '再见我依然爱你': doHatch,
  'pat': doPat, '摸摸': doPat, '撸': doPat, 'rua': doPat,
  'feed': doFeed, '喂': doFeed, '喂它': doFeed, '投食': doFeed,
  'card': doCard, '卡片': doCard, '宠物卡': doCard, '晒': doCard,
  'help': help, '帮助': help, '怎么玩': help,
};

const handler = CMD_MAP[cmd];
if (handler) {
  handler();
} else {
  help();
}
