# 🐾 CodePet — 在编程软件里养电子宠物 | Raise a Virtual Pet in Your Code Editor

> 每个程序员都值得一只编程搭子。
> Every programmer deserves a coding companion.

CodePet 是一只住在你编程软件里的电子宠物。它不帮你写代码，不给你建议——它只是陪着你。报错时它吐槽你，成功时它替你高兴，摸摸它会开心，喂它会涨经验。

CodePet is a virtual pet that lives inside your code editor. It doesn't write code or give advice — it just keeps you company. It roasts you when your code breaks, cheers when it works, gets happy when you pet it, and gains XP when you feed it.

---

## 🚀 安装教程 | Installation Guide

### 第 0 步：确认你有 Node.js | Step 0: Make sure you have Node.js

打开终端，输入 / Open your terminal and run:

```bash
node -v
```

如果显示版本号（如 `v18.17.0`），跳到第 1 步。
If you see a version number (e.g. `v18.17.0`), skip to Step 1.

如果提示"找不到命令" / If you get "command not found":
- 打开 / Visit https://nodejs.org
- 下载 **LTS 版本**（左边绿色按钮）/ Download the **LTS version** (green button on the left)
- 双击安装，一路"下一步" / Install it, click "Next" all the way through
- **重新打开终端** / **Restart your terminal**, then try `node -v` again

### 第 1 步：安装 CodePet | Step 1: Install CodePet

```bash
npm i -g codepet
```

> 💡 Mac 权限错误？加 `sudo` / Permission error on Mac? Add `sudo`:
> ```bash
> sudo npm i -g codepet
> ```

### 第 2 步：一键部署 | Step 2: Auto-deploy to your editors

```bash
codepet setup
```

自动检测你装了哪些编程工具，一键部署。
Automatically detects your installed editors and deploys to all of them.

### 第 3 步：孵化宠物 | Step 3: Hatch your pet

```bash
codepet hatch
```

Mac/Linux 也可以用中文 / Chinese alias on Mac/Linux:

```bash
宠物 孵化
```

按提示操作 / Follow the prompts:
1. 给宠物起名 / Name your pet
2. 签署承诺——不离不弃 / Sign a pledge — never abandon it
3. 破壳！🐣 / It hatches!

### 第 4 步：开始玩 | Step 4: Start playing

- **Claude Code**: 输入 `/pet` 或直接说"摸摸" / Type `/pet` or just say "pat it"
- **Cursor / VS Code**: 输入 `/pet` / Type `/pet`
- **终端 / Terminal**: 用 `codepet` 或 `宠物` 命令 / Use `codepet` or `宠物` commands

---

## 🎮 所有命令 | All Commands

### 终端命令 | Terminal Commands

| 命令 Command | 中文别名 Chinese Alias | 说明 Description |
|------|--------|----------|
| `codepet setup` | `宠物 安装` | 一键安装到所有编程工具 / Auto-deploy to all editors |
| `codepet hatch` | `宠物 孵化` | 孵化新宠物 / Hatch a new pet |
| `codepet show` | `宠物 看看` | 查看宠物状态 / View pet status |
| `codepet pat` | `宠物 摸摸` | 撸宠物 +5 经验 / Pet it, +5 XP |
| `codepet feed` | `宠物 喂它` | 喂宠物 +8 经验 / Feed it, +8 XP |
| `codepet card` | `宠物 卡片` | 生成分享卡片 / Generate share card (PNG) |
| `codepet share` | `宠物 分享` | 生成二维码分享卡 / Generate QR share card |
| `codepet xhs` | `宠物 小红书` | 小红书/朋友圈分享图 / Xiaohongshu/social share image |
| `codepet vs [file]` | `宠物 对比` | 宠物 PK 对比 / Compare pets side-by-side |
| `codepet popup` | `宠物 拍照` | 弹窗彩色大图 / Pop up color portrait |
| `codepet ascii` | `宠物 画` | ASCII 像素画 / ASCII pixel art |
| `codepet live` | `宠物 桌宠` | 常驻桌宠窗口 / Persistent desktop pet window |
| `codepet achievements` | `宠物 成就` | 查看成就 / View achievements |
| `codepet fortune` | `宠物 运势` | 今日运势 / Daily fortune |
| `codepet diary` | `宠物 日记` | 宠物日记（7天）/ Pet diary (last 7 days) |
| `codepet surprise off` | `宠物 惊喜 关` | 关闭惊喜弹窗 / Disable surprise popups |
| `codepet surprise low` | `宠物 惊喜 偶尔` | 偶尔出现（2%）/ Occasional popups (2%) |
| `codepet surprise high` | `宠物 惊喜 经常` | 经常出现（10%）/ Frequent popups (10%) |
| `codepet check` | `宠物 检测` | 环境检测 / Environment check |
| `codepet help` | `宠物 帮助` | 显示帮助 / Show help |

> 💡 中文别名仅支持 Mac/Linux。Windows 请用英文命令。
> 💡 Chinese aliases only work on Mac/Linux. Use English commands on Windows.

### 在编程工具里（自然语言）| In Your Editor (Natural Language)

不需要记命令，直接说人话 / No need to memorize commands, just talk naturally:

| 你说的 What you say | 宠物做的 What happens |
|--------|----------|
| "看看宠物" / "how's my pet" | 展示状态 / Show status |
| "摸摸" "rua" / "pet it" "pat" | 撸它 +5 XP |
| "喂它" "来根香蕉" / "feed it" | 喂食 +8 XP |
| "拍照" "咔嚓" / "take a photo" | 弹出彩色大图 / Color portrait popup |
| "卡片" "晒一下" / "share card" | 生成分享卡片 / Generate share card |
| "成就" / "achievements" | 查看成就 / View achievements |
| "运势" "算一卦" / "fortune" | 今日运势 / Daily fortune |
| "日记" / "diary" | 最近 7 天记录 / Last 7 days |
| "闭嘴" "安静" / "shh" "quiet" | 宠物静音 / Mute pet |
| "醒醒" "出来" / "wake up" | 取消静音 / Unmute pet |
| "改名叫XX" / "rename to XX" | 改名 / Rename pet |

---

## 🐾 6 个角色 | 6 Characters

| 角色 Character | 一句话 Tagline | 概率 Rate |
|------|--------|----------|
| **比比拉布** Bibilabu | 穿着香蕉皮，又萌又无奈 / Wearing a banana peel, cute but helpless | 28% |
| **八嘎呀路** Bagayalu | 佛系到极致，什么都不急 / Ultimate zen, never in a rush | 28% |
| **巴巴博一** Bababoyi | 圆滚滚大眼睛，看起来很有智慧 / Big round eyes, looks wise | 20% |
| **歪比巴卜** Waibibabu | 白 T 恤抱胸，社会大哥范 / Arms crossed, street boss vibes | 12% |
| **咕咕嘎嘎** Gugugaga | 黑刘海，软萌但嘴毒 / Black bangs, soft but savage | 8% |
| **我的刀盾** Wodedaodun | 永远在打瞌睡 / Always napping (rarest!) | 4% |

同一个用户永远孵化出同一只宠物——确定性抽卡，不看脸。
Same user always hatches the same pet — deterministic gacha, no luck involved.

---

## ⭐ 稀有度 | Rarity

| 稀有度 Rarity | 概率 Rate | 星级 Stars |
|--------|------|------|
| 普通 Common | 60% | ★ |
| 优秀 Uncommon | 25% | ★★ |
| 稀有 Rare | 10% | ★★★ |
| 史诗 Epic | 4% | ★★★★ |
| 传奇 Legendary | 1% | ★★★★★ |

1% 概率出 Shiny 闪光版（名字后带 ✧）
1% chance of a Shiny variant (✧ after the name)

---

## 📊 5 项属性 | 5 Stats

| 属性 Stat | 含义 Meaning |
|------|------|
| 调试力 Debug | 发现 bug 的直觉 / Instinct for finding bugs |
| 耐心值 Patience | 容忍你反复报错的能力 / Tolerance for your repeated errors |
| 混沌值 Chaos | 说话的不可预测程度 / Unpredictability of speech |
| 智慧值 Wisdom | 给出有用建议的概率 / Chance of giving useful advice |
| 毒舌值 Sass | 阴阳怪气的程度 / Level of sarcasm |

每只宠物有一个巅峰属性和一个短板属性，不同角色有属性倾向。
Each pet has one peak stat and one weak stat. Different characters have stat tendencies.

---

## 🎯 特性 | Features

| 特性 Feature | 说明 Description |
|------|------|
| 确定性孵化 Deterministic Hatch | 同一用户永远同一只 / Same user, same pet, always |
| 6 级养成 6-Level Growth | 撸它喂它涨经验 / Pet & feed to gain XP and level up |
| 性格系统 Personality | 每个角色独立性格和口头禅 / Unique personality & catchphrases |
| 心情衰减 Mood Decay | 长时间不管会焦虑 / Gets anxious if neglected |
| 惊喜弹窗 Surprise Popups | 编程时宠物突然冒出来 / Pet randomly appears while coding |
| 拍立得照片 Polaroid Photo | 弹窗彩色像素大图 / Pop-up color pixel portrait |
| 分享卡片 Share Cards | PNG 卡片晒朋友圈/小红书 / PNG cards for social media |
| PK 对比 Pet VS | 和别人比属性 / Compare stats with others |
| 成就系统 Achievements | 隐藏成就等你解锁 / Hidden achievements to unlock |
| 今日运势 Daily Fortune | 每天算一卦 / Daily fortune telling |
| 宠物日记 Pet Diary | 自动记录互动 / Auto-records daily interactions |

---

## 🖥️ 支持平台 | Supported Platforms

| 平台 Platform | 安装方式 How to install |
|------|----------|
| Claude Code | `codepet setup` 自动部署 / auto-deploy |
| Codex (OpenAI) | `codepet setup` 自动部署 / auto-deploy |
| OpenClaw | `codepet setup` 自动部署 / auto-deploy |
| Cursor | 输入 `/pet` / Type `/pet` in editor |
| VS Code | 输入 `/pet` / Type `/pet` in editor |
| Kiro | 输入 `/pet` / Type `/pet` in editor |
| CodeBuddy | 输入 `/pet` / Type `/pet` in editor |
| Antigravity | 输入 `/pet` / Type `/pet` in editor |
| OpenCode | 输入 `/pet` / Type `/pet` in editor |

---

## ❓ 常见问题 | FAQ

### Q：Mac 上 `npm i -g` 报权限错误？ | Permission error on Mac?

```bash
sudo npm i -g codepet
```

输入电脑密码（不会显示），回车。
Enter your password (it won't show), then press Enter.

### Q：Windows 上"宠物"命令用不了？ | "宠物" command doesn't work on Windows?

Windows 不支持中文命令名，请用英文 / Use English commands instead:

```bash
codepet hatch    # 代替 instead of: 宠物 孵化
codepet show     # 代替 instead of: 宠物 看看
codepet pat      # 代替 instead of: 宠物 摸摸
```

### Q：拍照/卡片功能报错？ | Photo/card features not working?

需要 Python 3 + Pillow / Requires Python 3 + Pillow:

```bash
# 检查 Python / Check Python
python3 --version

# 没装？去 / Not installed? Visit https://python.org

# 安装依赖（一般 setup 会自动装）
# Install deps (usually auto-installed by setup)
pip3 install Pillow wcwidth
```

### Q：想换一只宠物？ | Want a different pet?

```bash
codepet hatch    # 会提示是否覆盖 / Will ask to confirm overwrite
```

注意：同一用户结果是确定的，换了也是同一只。
Note: Same user always gets the same pet — it's deterministic.

### Q：怎么更新？ | How to update?

```bash
npm i -g codepet@latest
codepet setup
```

### Q：数据存在哪？ | Where is pet data stored?

`~/.codepet/pet.json`

主目录下的 `.codepet` 文件夹。
In the `.codepet` folder under your home directory.

---

## 🏗️ 项目结构 | Project Structure

```
codepet/
├── bin/                  # CLI 入口 / CLI entry point
│   └── codepet.js        # 主命令 / Main command (codepet / 宠物)
├── core/                 # 核心逻辑 / Core logic
│   ├── index.js           # 孵化、属性、经验 / Hatch, stats, XP
│   ├── achievements.js    # 成就系统 / Achievement system
│   ├── fortune.js         # 运势 / Fortune system
│   └── diary.js           # 日记 / Diary system
├── scripts/              # 渲染与图片 / Rendering & images
│   ├── img2terminal.py    # 终端彩色渲染 / Terminal color rendering
│   ├── img2ascii.py       # ASCII 像素画 / ASCII pixel art
│   ├── polaroid.py        # 拍立得 / Polaroid effect
│   ├── pet_card.py        # 宠物卡片 / Pet card
│   ├── share_card.py      # 分享卡片 / Share card
│   ├── xhs_template.py    # 小红书模板 / Xiaohongshu template
│   ├── vs_compare.py      # PK 对比 / VS comparison
│   └── live_pet.py        # 桌宠动画 / Desktop pet animation
├── sprites/              # 角色图片 / Character sprites
├── adapters/             # 平台适配 / Platform adapters
│   └── skill/SKILL.md    # Claude Code / Codex Skill
└── README.md
```

---

## 📜 License

MIT

## 品牌 | Brand

**Ai小蓝鲸** 🐋
