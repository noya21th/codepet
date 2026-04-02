// Auto-records daily stats
const fs = require('fs');
const path = require('path');
const os = require('os');

const DIARY_FILE = path.join(os.homedir(), '.codepet', 'diary.json');

function loadDiary() {
  try {
    return JSON.parse(fs.readFileSync(DIARY_FILE, 'utf-8'));
  } catch {
    return { entries: [] };
  }
}

function saveDiary(diary) {
  fs.writeFileSync(DIARY_FILE, JSON.stringify(diary, null, 2), 'utf-8');
}

function recordToday(pet) {
  const diary = loadDiary();
  const today = new Date().toISOString().slice(0, 10);

  // Check if already recorded today
  let entry = diary.entries.find(e => e.date === today);
  if (!entry) {
    entry = { date: today, exp: 0, pats: 0, feeds: 0, level: pet.level };
    diary.entries.push(entry);
  }

  entry.exp = pet.exp;
  entry.pats = pet.patCount;
  entry.feeds = pet.feedCount;
  entry.level = pet.level;

  // Keep only last 30 days
  if (diary.entries.length > 30) {
    diary.entries = diary.entries.slice(-30);
  }

  saveDiary(diary);
  return entry;
}

function getRecentDiary(days = 7) {
  const diary = loadDiary();
  return diary.entries.slice(-days);
}

module.exports = { recordToday, getRecentDiary, loadDiary };
