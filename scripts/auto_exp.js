#!/usr/bin/env node
/**
 * auto_exp.js — PostToolUse hook for Write|Edit events
 *
 * 从 stdin 读取 JSON（Claude hook 传入的 tool_input），
 * 为宠物增加经验值：
 *   - 普通代码写入 +5 exp
 *   - 包含错误修复关键词 +10 exp
 * 同时更新 lastInteraction 时间戳。
 *
 * Hook 配置示例（settings.json）：
 * {
 *   "hooks": {
 *     "PostToolUse": [
 *       {
 *         "matcher": "Write|Edit",
 *         "command": "cat /dev/stdin | node auto_exp.js"
 *       }
 *     ]
 *   }
 * }
 */

const { loadPet, addExp, savePet } = require('../core/index.js');

// 错误修复关键词
const FIX_KEYWORDS = [
  'fix', 'bug', 'error', 'patch', 'hotfix', 'repair', 'resolve',
  'crash', 'issue', 'broken', 'typo', 'workaround', 'correc',
  '修复', '修正', '错误', 'debug',
];

function readStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.setEncoding('utf-8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    // 如果 stdin 不是管道（无数据），500ms 后超时
    if (process.stdin.isTTY) {
      resolve('');
    }
    setTimeout(() => resolve(data), 500);
  });
}

async function main() {
  const pet = loadPet();
  if (!pet) process.exit(0);

  const raw = await readStdin();

  let toolInput = {};
  try {
    const parsed = JSON.parse(raw);
    // hook JSON 可能在 tool_input 字段或顶层
    toolInput = parsed.tool_input || parsed;
  } catch {
    // JSON 解析失败，仍然给基础经验
  }

  // 判断是否为错误修复
  const content = [
    toolInput.new_string || '',
    toolInput.content || '',
    toolInput.old_string || '',
    toolInput.file_path || '',
  ].join(' ').toLowerCase();

  const isFix = FIX_KEYWORDS.some((kw) => content.includes(kw));
  const expAmount = isFix ? 10 : 5;

  // 更新 lastInteraction
  pet.lastInteraction = new Date().toISOString();

  // 如果宠物在 sleep 或 worry，互动后恢复清醒
  if (pet.mood === 'sleep' || pet.mood === 'worry') {
    pet.mood = '清醒';
  }

  // 加经验（addExp 内部会 savePet）
  const result = addExp(pet, expAmount);

  // 升级时输出提示到 stderr
  if (result.leveledUp) {
    const name = pet.nickname || pet.name;
    console.error(`\n🎉 ${name} 升级了！现在是 Lv.${result.newLevel}！`);
  }
}

main().catch(() => process.exit(0));
