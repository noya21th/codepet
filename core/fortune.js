// Daily fortune - same result for same day + same pet
const FORTUNES = [
  { level: '大吉', icon: '🌟', advice: '今天写的代码一定没 bug！' },
  { level: '吉', icon: '✨', advice: '适合重构，一切会变得更好。' },
  { level: '中吉', icon: '🌤️', advice: '稳扎稳打，别急着提交。' },
  { level: '小吉', icon: '🌥️', advice: '记得写注释，未来的你会感谢现在。' },
  { level: '末吉', icon: '☁️', advice: '小心拼写错误，魔鬼在细节里。' },
  { level: '凶', icon: '🌧️', advice: '今天可能会遇到诡异的 bug，深呼吸。' },
  { level: '大凶', icon: '⛈️', advice: '别碰数据库！先备份！' },
];

function getDailyFortune(pet) {
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const seed = hashStr(today + (pet.name || '') + (pet.seed || ''));
  const idx = Math.abs(seed) % FORTUNES.length;
  return FORTUNES[idx];
}

function hashStr(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash |= 0;
  }
  return hash;
}

module.exports = { getDailyFortune, FORTUNES };
