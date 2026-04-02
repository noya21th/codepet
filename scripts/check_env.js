#!/usr/bin/env node
/**
 * 环境检测 — 检查 Node.js, Python, pip, Pillow 是否安装
 * 给出平台对应的安装命令
 */
const { execSync } = require('child_process');
const os = require('os');

const isWin = process.platform === 'win32';
const isMac = process.platform === 'darwin';

function check(name, cmd) {
  try {
    const ver = execSync(cmd, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] }).trim().split('\n')[0];
    return { ok: true, version: ver };
  } catch {
    return { ok: false };
  }
}

console.log('\n  🔍 CodePet 环境检测\n');

// Node.js
const node = check('Node.js', 'node --version');
console.log(`  ${node.ok ? '✅' : '❌'} Node.js ${node.ok ? node.version : '— 未安装'}`);

// npm
const npm = check('npm', 'npm --version');
console.log(`  ${npm.ok ? '✅' : '❌'} npm ${npm.ok ? 'v' + npm.version : '— 未安装'}`);

// Python
const py3 = check('Python3', 'python3 --version');
const py = check('Python', 'python --version');
const python = py3.ok ? py3 : py;
console.log(`  ${python.ok ? '✅' : '❌'} Python ${python.ok ? python.version : '— 未安装'}`);

// Pillow
const pyCmd = py3.ok ? 'python3' : (py.ok ? 'python' : null);
let pillow = { ok: false };
if (pyCmd) {
  pillow = check('Pillow', `${pyCmd} -c "import PIL; print(PIL.__version__)"`);
}
console.log(`  ${pillow.ok ? '✅' : '❌'} Pillow ${pillow.ok ? 'v' + pillow.version : '— 未安装'}`);

// wcwidth
let wcw = { ok: false };
if (pyCmd) {
  wcw = check('wcwidth', `${pyCmd} -c "import wcwidth; print(wcwidth.__version__)"`);
}
console.log(`  ${wcw.ok ? '✅' : '❌'} wcwidth ${wcw.ok ? 'v' + wcw.version : '— 未安装'}`);

console.log();

// Missing items
const missing = [];
if (!node.ok) missing.push('Node.js');
if (!python.ok) missing.push('Python');
if (python.ok && !pillow.ok) missing.push('Pillow');
if (python.ok && !wcw.ok) missing.push('wcwidth');

if (missing.length === 0) {
  console.log('  ✅ 环境完备，可以使用所有功能！\n');
} else {
  console.log('  ⚠️  缺少以下组件:\n');

  for (const m of missing) {
    if (m === 'Node.js') {
      console.log('  Node.js:');
      if (isMac) console.log('    brew install node');
      else if (isWin) console.log('    winget install OpenJS.NodeJS.LTS');
      else console.log('    sudo apt install nodejs npm');
      console.log('    或访问 https://nodejs.org\n');
    }
    if (m === 'Python') {
      console.log('  Python:');
      if (isMac) console.log('    brew install python');
      else if (isWin) console.log('    winget install Python.Python.3.12');
      else console.log('    sudo apt install python3 python3-pip');
      console.log('    或访问 https://python.org\n');
    }
    if (m === 'Pillow') {
      console.log('  Pillow:');
      console.log(`    ${pyCmd} -m pip install Pillow\n`);
    }
    if (m === 'wcwidth') {
      console.log('  wcwidth:');
      console.log(`    ${pyCmd} -m pip install wcwidth\n`);
    }
  }
}
