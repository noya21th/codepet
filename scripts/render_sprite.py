#!/usr/bin/env python3
"""CodePet 像素精灵渲染器 v2 — 基于真实形象"""

import sys

# ── 调色板（从真实图片取色）──
C = {
    '.': None,
    # 香蕉/植物
    'Y': (215, 195, 55),    # 香蕉黄
    'y': (185, 165, 45),    # 香蕉暗黄
    'G': (95, 120, 45),     # 蒂绿
    # 灰猫（比比拉布/巴巴博一/咕咕嘎嘎）
    'S': (185, 180, 175),   # 银灰猫毛
    's': (155, 150, 145),   # 深银灰
    'A': (205, 200, 195),   # 亮灰
    'a': (130, 125, 120),   # 暗灰
    # 水豚（八嘎呀路/我的刀盾）
    'B': (195, 145, 75),    # 金棕
    'b': (165, 120, 60),    # 深棕
    'L': (225, 200, 155),   # 浅棕/肚
    'l': (240, 220, 180),   # 亮浅棕
    'M': (210, 170, 110),   # 中棕
    # 巴巴博一（猫球）
    'C': (215, 200, 180),   # 奶油色身体
    'c': (195, 175, 155),   # 深奶油
    # 歪比巴卜（卡通人）
    'F': (225, 185, 145),   # 肤色
    'f': (200, 160, 120),   # 深肤色
    'H': (165, 105, 55),    # 胡子棕
    'h': (135, 80, 40),     # 深胡子
    'K': (165, 170, 175),   # 帽灰
    'k': (140, 145, 150),   # 帽深灰
    'T': (242, 242, 238),   # 白衣
    't': (220, 220, 216),   # 衣影
    # 咕咕嘎嘎（黑发）
    'D': (65, 65, 70),      # 黑发
    'd': (90, 90, 95),      # 深灰发
    # 通用
    'W': (240, 235, 225),   # 白
    'w': (250, 248, 242),   # 亮白
    'X': (30, 30, 30),      # 黑（眼）
    'x': (60, 55, 50),      # 深灰（眼）
    'P': (205, 155, 145),   # 粉鼻
    'p': (185, 130, 120),   # 深粉
    'R': (195, 105, 100),   # 红嘴
    'J': (80, 95, 130),     # 牛仔蓝
    'j': (60, 75, 105),     # 深蓝
    'n': (170, 130, 90),    # 鼻棕
    'E': (50, 80, 50),      # 深绿
}

SPRITES = {}

# ═══════════════════════════════════════
# 1. 比比拉布（香蕉猫）
#    灰猫脸从香蕉里探出，绿蒂，灰爪
#    20w × 26h
# ═══════════════════════════════════════
SPRITES['bibilabu'] = {
'normal': [
    ".........EE.........",
    "........EGGE........",
    ".......EGGGE........",
    "........YYY.........",
    ".......YYYYY........",
    "......YYYYYY........",
    ".....YYsSSsYY.......",
    ".....YsSSSSsY.......",
    "....YYSXSSXSyY......",
    "....YYSSPSSsyY......",
    "....YYsSSSSYYY......",
    ".....YYYYYYYY.......",
    ".....YYYYYYYY.......",
    ".....yYYYYYYy.......",
    ".....yyyYYYYy.......",
    ".....yyyYYYy........",
    "......yyYYy.........",
    "......yyyYy.........",
    ".......yyyy.........",
    "......yyy...........",
    ".......SS.SS........",
    "......SS...SS.......",
],
'happy': [
    ".........EE.........",
    "........EGGE........",
    ".......EGGGE........",
    "........YYY.........",
    ".......YYYYY........",
    "......YYYYYY........",
    ".....YYsSSsYY.......",
    ".....YsSSSSsY.......",
    "....YYSaSSaSyY......",
    "....YYSSPSSsyY......",
    "....YYsSSSSYYY......",
    ".....YYYYYYYY.......",
    ".....YYYYYYYY.......",
    ".....yYYYYYYy.......",
    ".....yyyYYYYy.......",
    ".....yyyYYYy........",
    "......yyYYy.........",
    "......yyyYy.........",
    ".......yyyy.........",
    "......yyy...........",
    ".......SS.SS........",
    "......SS...SS.......",
],
'sleep': [
    ".........EE.........",
    "........EGGE........",
    ".......EGGGE........",
    "........YYY.........",
    ".......YYYYY........",
    "......YYYYYY........",
    ".....YYsSSsYY.......",
    ".....YsSSSSsY.......",
    "....YYSsSssSyY......",
    "....YYSSPSSsyY......",
    "....YYsSSSSYYY......",
    ".....YYYYYYYY.......",
    ".....YYYYYYYY.......",
    ".....yYYYYYYy.......",
    ".....yyyYYYYy.......",
    ".....yyyYYYy........",
    "......yyYYy.........",
    "......yyyYy.........",
    ".......yyyy.........",
    "......yyy...........",
    ".......SS.SS........",
    "......SS...SS.......",
],
}

# ═══════════════════════════════════════
# 2. 八嘎呀路（坐姿水豚）
#    金棕色，3/4侧面坐，闭眼忧郁，浅肚
#    20w × 22h
# ═══════════════════════════════════════
SPRITES['bagayalu'] = {
'normal': [
    "..........bb........",
    ".........bBBb.......",
    "........bBBBBb......",
    ".......bBBBBBBb.....",
    "......bBBBBBBBBb....",
    ".....bBbBBbBBBBBb...",
    ".....bBBnnBBBBBBb...",
    ".....bBBBBBBBBBBb...",
    "....bBBBBBBBBBBBb...",
    "...bBBBBBBBBBBBBb...",
    "..bBBBBBBBBBBBBBb...",
    "..bBBBLLLLLBBBBb....",
    "..bBBLLLLLLLBBBb....",
    "..bBBLLLLLLLBBb.....",
    "...bBBLLLLLBBb......",
    "...bBBBBBBBBBb......",
    "....bbBBBBBbb.......",
    "....bBb..bBBb.......",
    "....bb....bbb.......",
],
'happy': [
    "..........bb........",
    ".........bBBb.......",
    "........bBBBBb......",
    ".......bBBBBBBb.....",
    "......bBBBBBBBBb....",
    ".....bBMBBMBBBBBb...",
    ".....bBBnnBBBBBBb...",
    ".....bBBLLBBBBBBb...",
    "....bBBBBBBBBBBBb...",
    "...bBBBBBBBBBBBBb...",
    "..bBBBBBBBBBBBBBb...",
    "..bBBBLLLLLBBBBb....",
    "..bBBLLLLLLLBBBb....",
    "..bBBLLLLLLLBBb.....",
    "...bBBLLLLLBBb......",
    "...bBBBBBBBBBb......",
    "....bbBBBBBbb.......",
    "....bBb..bBBb.......",
    "....bb....bbb.......",
],
'sleep': [
    "..........bb........",
    ".........bBBb.......",
    "........bBBBBb......",
    ".......bBBBBBBb.....",
    "......bBBBBBBBBb....",
    ".....bBbBBbBBBBBb...",
    ".....bBBnnBBBBBBb...",
    ".....bBBBBBBBBBBb...",
    "....bBBBBBBBBBBBb...",
    "...bBBBBBBBBBBBBb...",
    "..bBBBBBBBBBBBBBb...",
    "..bBBBLLLLLBBBBb....",
    "..bBBLLLLLLLBBBb....",
    "..bBBLLLLLLLBBb.....",
    "...bBBLLLLLBBb......",
    "...bBBBBBBBBBb......",
    "....bbBBBBBbb.......",
    "....bBb..bBBb.......",
    "....bb....bbb.......",
],
}

# ═══════════════════════════════════════
# 3. 我的刀盾（趴姿水豚）
#    完全趴平像面包，侧面，微笑
#    22w × 12h
# ═══════════════════════════════════════
SPRITES['wodedaodun'] = {
'normal': [
    ".......bbbbb........",
    "....bbbBBBBBbbb.....",
    "...bBBBBBBBBBBBbb...",
    "..bBbBbBBBBBBBBBBb..",
    "..bBBnBBBBBBBBBBBBb.",
    "..bBBBLLBBBBBBBBBBb.",
    "...bBBBBBBBBBBBBBb..",
    "...bbLBBBBBBBBLbb...",
    "....bb.........bb...",
],
'happy': [
    ".......bbbbb........",
    "....bbbBBBBBbbb.....",
    "...bBBBBBBBBBBBbb...",
    "..bBMBMBBBBBBBBBBb..",
    "..bBBnBBBBBBBBBBBBb.",
    "..bBBBLLBBBBBBBBBBb.",
    "...bBBBBBBBBBBBBBb..",
    "...bbLBBBBBBBBLbb...",
    "....bb.........bb...",
],
'sleep': [
    ".......bbbbb........",
    "....bbbBBBBBbbb.....",
    "...bBBBBBBBBBBBbb...",
    "..bBbBbBBBBBBBBBBb..",
    "..bBBnBBBBBBBBBBBBb.",
    "..bBBBLLBBBBBBBBBBb.",
    "...bBBBBBBBBBBBBBb..",
    "...bbLBBBBBBBBLbb...",
    "....bb.........bb...",
],
}

# ═══════════════════════════════════════
# 4. 巴巴博一（圆猫球）
#    极度圆，巨大黑眼，粉鼻，灰+奶油色
#    20w × 20h
# ═══════════════════════════════════════
SPRITES['bababoyi'] = {
'normal': [
    ".......ssss.........",
    "......sSSSSs........",
    ".....sSSSSSSSs......",
    "....sSSSSSSSSSs.....",
    "...sSSSSSSSSSSSs....",
    "..sSxXxSSSSxXxSSs...",
    "..sSXXxSSSSxXXSSs...",
    "..sSSSSSSSSSSSSSSs..",
    "..sSSSSSPPSSSSSSSs..",
    "..sCCCCCCCCCCCCCs...",
    "..CCCCCCCCCCCCCCCC..",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    "..CCCCCCCCCCCCCCCC..",
    "..cCCCCCCCCCCCCCc...",
    "...ccCCCCCCCCcc.....",
    "....cccccccccc......",
    ".....ss....ss.......",
],
'happy': [
    ".......ssss.........",
    "......sSSSSs........",
    ".....sSSSSSSSs......",
    "....sSSSSSSSSSs.....",
    "...sSSSSSSSSSSSs....",
    "..sSaxaSSSSaxaSSs...",
    "..sSaaaSSSsaaaSs....",
    "..sSSSSSSSSSSSSSSs..",
    "..sSSSSSPPSSSSSSSs..",
    "..sCCCCCCCCCCCCCs...",
    "..CCCCCCCCCCCCCCCC..",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    "..CCCCCCCCCCCCCCCC..",
    "..cCCCCCCCCCCCCCc...",
    "...ccCCCCCCCCcc.....",
    "....cccccccccc......",
    ".....ss....ss.......",
],
'sleep': [
    ".......ssss.........",
    "......sSSSSs........",
    ".....sSSSSSSSs......",
    "....sSSSSSSSSSs.....",
    "...sSSSSSSSSSSSs....",
    "..sSSsSSSSSsSSSSSs..",
    "..sSssSSSSssSSSSSs..",
    "..sSSSSSSSSSSSSSSs..",
    "..sSSSSSPPSSSSSSSs..",
    "..sCCCCCCCCCCCCCs...",
    "..CCCCCCCCCCCCCCCC..",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
    "..CCCCCCCCCCCCCCCC..",
    "..cCCCCCCCCCCCCCc...",
    "...ccCCCCCCCCcc.....",
    "....cccccccccc......",
    ".....ss....ss.......",
],
}

# ═══════════════════════════════════════
# 5. 歪比巴卜（大胡子壮汉）
#    卡通风，灰帽，肤色脸，棕胡子，白Polo衫
#    18w × 26h
# ═══════════════════════════════════════
SPRITES['waibibabu'] = {
'normal': [
    ".......kkkk.........",
    "......kKKKKk........",
    ".....kKKKKKKk.......",
    ".....KKKKKKKKK......",
    "....FFFFFFFFFFf.....",
    "....FxFFFFxFFFF.....",
    "....FFFFFFFFFFFf....",
    "....FFFnnFFFFFf.....",
    "....fHHHHHHHHf......",
    ".....fHHHHHHf.......",
    "......ffffff........",
    ".....TTTTTTTTT......",
    "....TTTTtTTTTTT.....",
    "...FTTTTtTTTTTF.....",
    "...FFTTTtTTTTFF.....",
    "...FFFTTtTTFFF......",
    "....FFTTtTTFF.......",
    ".....TTTTTTT........",
    ".....TTTTTTT........",
    "......TTTTT.........",
    "......JJ.JJ.........",
    ".....JJJ.JJJ........",
    ".....JJ...JJ........",
    "....jjj...jjj.......",
],
'happy': [
    ".......kkkk.........",
    "......kKKKKk........",
    ".....kKKKKKKk.......",
    ".....KKKKKKKKK......",
    "....FFFFFFFFFFf.....",
    "....FaFFFFaFFFF.....",
    "....FFFFFFFFFFFf....",
    "....FFFnnFFFFFf.....",
    "....fHHHLHHHHf......",
    ".....fHHHHHHf.......",
    "......ffffff........",
    ".....TTTTTTTTT......",
    "....TTTTtTTTTTT.....",
    "...FTTTTtTTTTTF.....",
    "...FFTTTtTTTTFF.....",
    "...FFFTTtTTFFF......",
    "....FFTTtTTFF.......",
    ".....TTTTTTT........",
    ".....TTTTTTT........",
    "......TTTTT.........",
    "......JJ.JJ.........",
    ".....JJJ.JJJ........",
    ".....JJ...JJ........",
    "....jjj...jjj.......",
],
'sleep': [
    ".......kkkk.........",
    "......kKKKKk........",
    ".....kKKKKKKk.......",
    ".....KKKKKKKKK......",
    "....FFFFFFFFFFf.....",
    "....FfFFFFfFFFF.....",
    "....FFFFFFFFFFFf....",
    "....FFFnnFFFFFf.....",
    "....fHHHHHHHHf......",
    ".....fHHHHHHf.......",
    "......ffffff........",
    ".....TTTTTTTTT......",
    "....TTTTtTTTTTT.....",
    "...FTTTTtTTTTTF.....",
    "...FFTTTtTTTTFF.....",
    "...FFFTTtTTFFF......",
    "....FFTTtTTFF.......",
    ".....TTTTTTT........",
    ".....TTTTTTT........",
    "......TTTTT.........",
    "......JJ.JJ.........",
    ".....JJJ.JJJ........",
    ".....JJ...JJ........",
    "....jjj...jjj.......",
],
}

# ═══════════════════════════════════════
# 6. 咕咕嘎嘎（黑刘海圆脸猫）
#    厚黑灰色刘海，白/灰圆脸，小嘴
#    20w × 18h
# ═══════════════════════════════════════
SPRITES['gugugaga'] = {
'normal': [
    "......ddddddd.......",
    ".....dDDDDDDDd......",
    "....dDDDDDDDDDd.....",
    "...dDDDDDDDDDDDd....",
    "..dDDDDDDDDDDDDDd...",
    "..dDDDDDDDDDDDDDd...",
    "..dDxDDDDDDxDDDDd...",
    "..SSSSSSSSSSSSSSss..",
    "..SSSSSSSSSSSSSSSs..",
    "..SSSSSSSSSSSSSSss..",
    "..sSSSSSRSSSSSSSs...",
    "...sSSSSSSSSSSSs....",
    "...sSSSSSSSSSSs.....",
    "....sSWWWWWWSs......",
    "....sWWWWWWWWs......",
    ".....sWWWWWWs.......",
    "......ssssss........",
    ".......ss.ss........",
],
'happy': [
    "......ddddddd.......",
    ".....dDDDDDDDd......",
    "....dDDDDDDDDDd.....",
    "...dDDDDDDDDDDDd....",
    "..dDDDDDDDDDDDDDd...",
    "..dDDDDDDDDDDDDDd...",
    "..dDaDDDDDDaDDDDd...",
    "..SSSSSSSSSSSSSSss..",
    "..SSSSSSSSSSSSSSSs..",
    "..SSSSSSSSSSSSSSss..",
    "..sSSSSSLSSSSSSSs...",
    "...sSSSSSSSSSSSs....",
    "...sSSSSSSSSSSs.....",
    "....sSWWWWWWSs......",
    "....sWWWWWWWWs......",
    ".....sWWWWWWs.......",
    "......ssssss........",
    ".......ss.ss........",
],
'sleep': [
    "......ddddddd.......",
    ".....dDDDDDDDd......",
    "....dDDDDDDDDDd.....",
    "...dDDDDDDDDDDDd....",
    "..dDDDDDDDDDDDDDd...",
    "..dDDDDDDDDDDDDDd...",
    "..dDsDDDDDDsDDDDd...",
    "..SSSSSSSSSSSSSSss..",
    "..SSSSSSSSSSSSSSSs..",
    "..SSSSSSSSSSSSSSss..",
    "..sSSSSSSSSSSSSSs...",
    "...sSSSSSSSSSSSs....",
    "...sSSSSSSSSSSs.....",
    "....sSWWWWWWSs......",
    "....sWWWWWWWWs......",
    ".....sWWWWWWs.......",
    "......ssssss........",
    ".......ss.ss........",
],
}

# ── 渲染引擎 ──

def fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"
BOLD = "\033[1m"

def render_pixel_pair(top_char, bot_char):
    top_color = C.get(top_char)
    bot_color = C.get(bot_char)
    if top_color and bot_color:
        if top_color == bot_color:
            return f"{fg(*top_color)}█{RESET}"
        else:
            return f"{fg(*top_color)}{bg(*bot_color)}▀{RESET}"
    elif top_color:
        return f"{fg(*top_color)}▀{RESET}"
    elif bot_color:
        return f"{fg(*bot_color)}▄{RESET}"
    else:
        return " "

def render_sprite(name, state='normal', indent=4):
    data = SPRITES.get(name, {}).get(state)
    if not data:
        print(f"未找到: {name}/{state}")
        return
    rows = list(data)
    if len(rows) % 2 == 1:
        max_len = max(len(r) for r in rows)
        rows.append('.' * max_len)
    max_len = max(len(r) for r in rows)
    rows = [r.ljust(max_len, '.') for r in rows]
    for i in range(0, len(rows), 2):
        top_row = rows[i]
        bot_row = rows[i + 1]
        line = ""
        for j in range(max_len):
            tc = top_row[j] if j < len(top_row) else '.'
            bc = bot_row[j] if j < len(bot_row) else '.'
            line += render_pixel_pair(tc, bc)
        print(f"{' ' * indent}{line}")

def render_card(name, state='normal'):
    """渲染单个角色带标题"""
    names_zh = {
        'bibilabu': '比比拉布（香蕉猫）',
        'bagayalu': '八嘎呀路（坐姿水豚）',
        'wodedaodun': '我的刀盾（趴姿水豚）',
        'bababoyi': '巴巴博一（圆猫球）',
        'waibibabu': '歪比巴卜（大胡子壮汉）',
        'gugugaga': '咕咕嘎嘎（黑刘海猫）',
    }
    states_zh = {'normal': '普通', 'happy': '开心', 'sleep': '睡觉'}
    title = names_zh.get(name, name)
    st = states_zh.get(state, state)
    print(f"\n  {BOLD}{title}{RESET} · {st}")
    render_sprite(name, state)

def render_all():
    print()
    print("  ═══════════════════════════════════")
    print(f"    🐾 {BOLD}CodePet 像素角色画廊{RESET}")
    print("  ═══════════════════════════════════")
    for name in ['bibilabu', 'bagayalu', 'wodedaodun', 'bababoyi', 'waibibabu', 'gugugaga']:
        for state in ['normal', 'happy', 'sleep']:
            render_card(name, state)
        print("  ───────────────────────────────────")
    print()

# ── 入口 ──
if __name__ == '__main__':
    name_map = {
        '比比拉布': 'bibilabu', '八嘎呀路': 'bagayalu',
        '我的刀盾': 'wodedaodun', '巴巴博一': 'bababoyi',
        '歪比巴卜': 'waibibabu', '咕咕嘎嘎': 'gugugaga',
    }
    if len(sys.argv) < 2 or sys.argv[1] == 'all':
        render_all()
    else:
        name = name_map.get(sys.argv[1], sys.argv[1])
        state = sys.argv[2] if len(sys.argv) > 2 else 'normal'
        render_card(name, state)
