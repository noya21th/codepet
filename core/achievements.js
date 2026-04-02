// Achievement definitions and checking logic
const ACHIEVEMENTS = [
  { id: 'first_pat', name: '第一次摸摸', desc: '第一次撸了宠物', condition: (pet) => pet.patCount >= 1, icon: '🤚' },
  { id: 'first_feed', name: '第一顿饭', desc: '第一次喂了宠物', condition: (pet) => pet.feedCount >= 1, icon: '🍽️' },
  { id: 'lv2', name: '好奇的探索者', desc: '宠物升到 Lv.2', condition: (pet) => pet.level >= 2, icon: '⭐' },
  { id: 'lv3', name: '靠谱的伙伴', desc: '宠物升到 Lv.3', condition: (pet) => pet.level >= 3, icon: '🌟' },
  { id: 'lv5', name: '编程大师', desc: '宠物升到 Lv.5', condition: (pet) => pet.level >= 5, icon: '👑' },
  { id: 'lv6', name: '传说中的存在', desc: '宠物升到 Lv.6', condition: (pet) => pet.level >= 6, icon: '🏆' },
  { id: 'pat10', name: '撸猫达人', desc: '撸了宠物 10 次', condition: (pet) => pet.patCount >= 10, icon: '💕' },
  { id: 'pat100', name: '摸摸狂魔', desc: '撸了宠物 100 次', condition: (pet) => pet.patCount >= 100, icon: '💗' },
  { id: 'feed10', name: '称职的铲屎官', desc: '喂了宠物 10 次', condition: (pet) => pet.feedCount >= 10, icon: '🥄' },
  { id: 'feed50', name: '美食家的宠物', desc: '喂了宠物 50 次', condition: (pet) => pet.feedCount >= 50, icon: '🍱' },
  { id: 'exp100', name: '百分努力', desc: '累计 100 经验', condition: (pet) => pet.exp >= 100, icon: '💯' },
  { id: 'exp500', name: '半千里程碑', desc: '累计 500 经验', condition: (pet) => pet.exp >= 500, icon: '🎯' },
  { id: 'exp1000', name: '千锤百炼', desc: '累计 1000 经验', condition: (pet) => pet.exp >= 1000, icon: '🔥' },
  { id: 'day7', name: '一周不离不弃', desc: '孵化满 7 天', condition: (pet) => { const d = (Date.now() - new Date(pet.hatchedAt).getTime()) / 86400000; return d >= 7; }, icon: '📅' },
  { id: 'day30', name: '月老级铲屎官', desc: '孵化满 30 天', condition: (pet) => { const d = (Date.now() - new Date(pet.hatchedAt).getTime()) / 86400000; return d >= 30; }, icon: '🌙' },
  { id: 'rare', name: '欧皇', desc: '拥有稀有及以上宠物', condition: (pet) => pet.stars >= 3, icon: '🍀' },
  { id: 'epic', name: '非酋变欧', desc: '拥有史诗宠物', condition: (pet) => pet.stars >= 4, icon: '💎' },
  { id: 'legendary', name: '天选之人', desc: '拥有传奇宠物', condition: (pet) => pet.stars >= 5, icon: '👼' },
];

function checkAchievements(pet) {
  if (!pet.achievements) pet.achievements = [];
  const newOnes = [];
  for (const a of ACHIEVEMENTS) {
    if (!pet.achievements.includes(a.id) && a.condition(pet)) {
      pet.achievements.push(a.id);
      newOnes.push(a);
    }
  }
  return newOnes;
}

function getAllAchievements(pet) {
  const unlocked = pet.achievements || [];
  return ACHIEVEMENTS.map(a => ({
    ...a,
    unlocked: unlocked.includes(a.id),
  }));
}

module.exports = { ACHIEVEMENTS, checkAchievements, getAllAchievements };
