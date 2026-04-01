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

// 跨平台 Python 命令检测
function getPython() {
  for (const cmd of ['python3', 'python']) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch {}
  }
  return null;
}
const PYTHON = getPython();

// 自动安装 Python 依赖 (Pillow, wcwidth)
function ensurePythonDeps() {
  if (!PYTHON) return;
  try {
    execSync(`${PYTHON} -c "import PIL, wcwidth"`, { stdio: 'ignore' });
  } catch {
    console.log('  正在安装依赖 (Pillow, wcwidth)...');
    try {
      execSync(`${PYTHON} -m pip install Pillow wcwidth --quiet`, { stdio: 'inherit' });
    } catch {
      // pip might need --user on some systems
      try { execSync(`${PYTHON} -m pip install Pillow wcwidth --user --quiet`, { stdio: 'inherit' }); } catch {}
    }
  }
}

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

  // 复制精灵图片（包括子目录中的表情图）
  if (fs.existsSync(SPRITES_DIR)) {
    const spriteDestDir = path.join(destDir, 'sprites');
    if (!fs.existsSync(spriteDestDir)) {
      fs.mkdirSync(spriteDestDir, { recursive: true });
    }
    const entries = fs.readdirSync(SPRITES_DIR, { withFileTypes: true });
    for (const entry of entries) {
      const srcPath = path.join(SPRITES_DIR, entry.name);
      const dstPath = path.join(spriteDestDir, entry.name);
      if (entry.isFile() && entry.name.endsWith('.png')) {
        fs.copyFileSync(srcPath, dstPath);
      } else if (entry.isDirectory() && entry.name !== '6') {
        // Copy subdirectory (character expression sprites)
        if (!fs.existsSync(dstPath)) {
          fs.mkdirSync(dstPath, { recursive: true });
        }
        const subFiles = fs.readdirSync(srcPath).filter(f => f.endsWith('.png'));
        for (const sf of subFiles) {
          fs.copyFileSync(path.join(srcPath, sf), path.join(dstPath, sf));
        }
      }
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

  // ── 配置 Claude Code hooks ──
  configureCCHooks();

  console.log(`\n  ✅ 安装完成！共 ${installed} 个平台。`);
  console.log('  在任意支持的工具里输入 /pet 开始养宠物。\n');
}

// ── 配置 Claude Code settings.json hooks ──
function configureCCHooks() {
  const settingsPath = path.join(os.homedir(), '.claude', 'settings.json');
  if (!fs.existsSync(path.dirname(settingsPath))) return; // Claude Code not installed

  // Detect package root (works for both npm global install and local dev)
  const pkgRoot = path.join(__dirname, '..');
  const scriptsDir = path.join(pkgRoot, 'scripts');

  // Build cross-platform hook commands
  const pythonCmd = PYTHON || 'python3';
  const petBubbleScript = path.join(scriptsDir, 'pet_bubble.js');
  const autoExpScript = path.join(scriptsDir, 'auto_exp.py');

  let petBubbleHook, autoExpHook;
  if (process.platform === 'win32') {
    // Windows: use node for .js, python for .py
    petBubbleHook = `node "${petBubbleScript}"`;
    autoExpHook = `${pythonCmd} "${autoExpScript}"`;
  } else {
    petBubbleHook = `node "${petBubbleScript}"`;
    autoExpHook = `${pythonCmd} "${autoExpScript}"`;
  }

  // Read existing settings
  let settings = {};
  if (fs.existsSync(settingsPath)) {
    try {
      settings = JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
    } catch {
      settings = {};
    }
  }

  // Merge hooks - don't overwrite existing hooks, append if not present
  if (!settings.hooks) settings.hooks = {};

  // pet_bubble hook (runs after each assistant response)
  const hookKey = 'PostToolExecution';
  if (!settings.hooks[hookKey]) settings.hooks[hookKey] = [];
  const existingBubble = settings.hooks[hookKey].find(h =>
    (typeof h === 'string' ? h : h.command || '').includes('pet_bubble')
  );
  if (!existingBubble) {
    settings.hooks[hookKey].push({
      command: petBubbleHook,
      description: 'CodePet bubble reaction'
    });
  }

  // auto_exp hook (gains exp on tool execution)
  const existingExp = settings.hooks[hookKey].find(h =>
    (typeof h === 'string' ? h : h.command || '').includes('auto_exp')
  );
  if (!existingExp) {
    settings.hooks[hookKey].push({
      command: autoExpHook,
      description: 'CodePet auto experience gain'
    });
  }

  // Add bypassPermissions for codepet commands
  if (!settings.bypassPermissions) settings.bypassPermissions = [];
  const codepetPerms = [
    'codepet *',
    'node */codepet/bin/codepet.js *',
    'node */codepet/scripts/*',
  ];
  for (const perm of codepetPerms) {
    if (!settings.bypassPermissions.includes(perm)) {
      settings.bypassPermissions.push(perm);
    }
  }

  // Write back
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n', 'utf-8');
  console.log('  ✓ Claude Code — hooks 已配置');
}

// ── 渲染像素画 ──
function renderSprite(character, variant) {
  variant = variant || 'normal';

  if (imageMode) {
    // 图片模式：生成 PNG，输出路径
    const renderImgScript = path.join(__dirname, '..', 'scripts', 'render_to_image.py');
    if (fs.existsSync(renderImgScript)) {
      try {
        const imgPath = execSync(`${PYTHON} "${renderImgScript}" "${character}" "${variant}"`, { encoding: 'utf-8' }).trim();
        console.log(`[图片:${imgPath}]`);
      } catch (e) {}
    }
  } else {
    // 终端模式：彩色像素画
    if (!PYTHON) return; // Python 未安装，静默跳过
    const renderScript = path.join(__dirname, '..', 'scripts', 'img2terminal.py');
    let spritePath = path.join(SPRITES_DIR, character, `${variant}.png`);
    if (!fs.existsSync(spritePath)) {
      spritePath = path.join(SPRITES_DIR, `${character}.png`);
    }
    if (fs.existsSync(spritePath) && fs.existsSync(renderScript)) {
      try {
        const output = execSync(`${PYTHON} "${renderScript}" "${spritePath}" ${RENDER_WIDTH}`, { encoding: 'utf-8' });
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
  ensurePythonDeps();
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

function doAscii() {
  ensurePythonDeps();
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  if (!PYTHON) { console.log('  需要安装 Python。'); return; }
  const scene = arg || 'normal';
  const script = path.join(__dirname, '..', 'scripts', 'img2ascii.py');
  let sprite = path.join(SPRITES_DIR, pet.character, `${scene}.png`);
  if (!fs.existsSync(sprite)) sprite = path.join(SPRITES_DIR, `${pet.character}.png`);
  if (fs.existsSync(script) && fs.existsSync(sprite)) {
    try {
      const out = execSync(`${PYTHON} "${script}" "${sprite}" 22`, { encoding: 'utf-8' });
      console.log(out);
    } catch {}
  }
}

function doPopup() {
  ensurePythonDeps();
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  if (!PYTHON) { console.log('  需要安装 Python。'); return; }
  const scene = arg || 'normal';

  if (process.platform === 'darwin') {
    // macOS: 弹新 Terminal 窗口显示彩色像素风拍立得
    const script = path.join(__dirname, '..', 'scripts', 'polaroid.py');
    const escapedScript = script.replace(/'/g, "'\\''");
    execSync(`osascript -e 'tell application "Terminal" to do script "export HISTFILE=/dev/null && export BASH_SILENCE_DEPRECATION_WARNING=1 && export PS1=\\\"\\\" && clear && ${PYTHON} \\\"${escapedScript}\\\" ${pet.character} ${scene} 40 2>/dev/null && printf \\\"\\\\033[?25l\\\" && cat > /dev/null"' -e 'tell application "Terminal" to activate' &`, { shell: true, stdio: 'ignore' });
  } else if (process.platform === 'win32') {
    // Windows: 弹新 PowerShell 窗口显示彩色像素画拍立得
    const script = path.join(__dirname, '..', 'scripts', 'polaroid.py').replace(/\\/g, '\\\\');
    const psCmd = `${PYTHON} \\"${script}\\" ${pet.character} ${scene} 40 2>$null; Read-Host`;
    execSync(`start powershell -NoProfile -Command "${psCmd}"`, { shell: true, stdio: 'ignore' });
  } else {
    // Linux: 尝试终端弹窗
    const script = path.join(__dirname, '..', 'scripts', 'polaroid.py');
    if (process.env.DISPLAY) {
      try {
        execSync(`gnome-terminal -- bash -c '${PYTHON} "${script}" ${pet.character} ${scene} 40; read' 2>/dev/null &`, { shell: true, stdio: 'ignore' });
      } catch {
        try { execSync(`${PYTHON} "${script}" ${pet.character} ${scene} 40`, { stdio: 'inherit' }); } catch {}
      }
    } else {
      try { execSync(`${PYTHON} "${script}" ${pet.character} ${scene} 40`, { stdio: 'inherit' }); } catch {}
    }
  }
}

function doCard() {
  ensurePythonDeps();
  const pet = core.loadPet();
  if (!pet) { console.log('  还没有宠物。'); return; }
  const cardScript = path.join(__dirname, '..', 'scripts', 'pet_card.py');
  if (fs.existsSync(cardScript)) {
    try {
      execSync(`${PYTHON} "${cardScript}"`, { encoding: 'utf-8', stdio: 'inherit' });
      // 跨平台打开图片
      const cardPath = path.join(os.homedir(), '.codepet', 'card.png');
      const openCmd = process.platform === 'win32' ? 'start ""' : process.platform === 'darwin' ? 'open' : 'xdg-open';
      execSync(`${openCmd} "${cardPath}"`, { stdio: 'ignore', shell: true });
    } catch (e) {
      console.log('  卡片生成失败。');
    }
  }
}

function help() {
  console.log(`
  🐾 CodePet — 在编程软件里养电子宠物

  用法 (macOS/Linux 可用 "宠物"，Windows 请用 "codepet"):
    codepet setup     一键安装到所有编程工具
    codepet hatch     孵化新宠物
    codepet show      查看宠物
    codepet pat       撸宠物
    codepet feed      喂宠物
    codepet card      生成分享卡片
    codepet popup     拍照弹窗
    codepet ascii     ASCII 画
    codepet help      显示此帮助

  中文别名 (macOS/Linux):
    宠物 安装 / 孵化 / 看看 / 摸摸 / 喂它 / 卡片 / 帮助

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
  'ascii': doAscii, '画': doAscii,
  'popup': doPopup, '照片': doPopup, '拍照': doPopup,
  'help': help, '帮助': help, '怎么玩': help,
};

const handler = CMD_MAP[cmd];
if (handler) {
  handler();
} else {
  help();
}
