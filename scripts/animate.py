#!/usr/bin/env python3
"""CodePet 终端动画 — 眨眼、动嘴、摆手"""

import os, sys, time, copy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from img2terminal import render_image
from PIL import Image, ImageDraw

SPRITE_DIR = os.path.join(SCRIPT_DIR, "..", "sprites")
RESET = "\033[0m"
BOLD = "\033[1m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# ── 每个角色的关键区域（基于裁切后的图片坐标）──
# 格式: { 'eyes': (x1,y1,x2,y2), 'mouth': (x1,y1,x2,y2), 'arm': (x1,y1,x2,y2) }
# 用 None 表示没有该部位动画

REGIONS = {
    'bibilabu': {
        'eyes': (105, 90, 160, 110),     # 猫眼睛区域
        'mouth': (115, 110, 150, 130),   # 猫嘴区域
    },
    'bagayalu': {
        'eyes': (100, 100, 200, 130),    # 水豚眼
        'mouth': (120, 140, 200, 175),   # 水豚嘴
    },
    'wodedaodun': {
        'eyes': (60, 80, 140, 110),      # 柴犬眼
        'mouth': (80, 115, 150, 145),    # 柴犬嘴
    },
    'bababoyi': {
        'eyes': (60, 80, 220, 130),      # 猫球大眼
        'mouth': (110, 130, 170, 155),   # 猫球嘴
    },
    'waibibabu': {
        'eyes': (100, 75, 190, 100),     # 壮汉眼
        'mouth': (95, 115, 195, 155),    # 壮汉嘴/胡子
        'arm':  (50, 170, 250, 250),     # 壮汉手臂
    },
    'gugugaga': {
        'eyes': (80, 120, 210, 155),     # 刘海猫眼
        'mouth': (120, 160, 185, 185),   # 刘海猫嘴
    },
}

def make_blink_frame(img, eye_region):
    """眨眼：用眼睛区域的平均肤色画一条横线盖住眼睛"""
    frame = img.copy()
    x1, y1, x2, y2 = eye_region
    # 取眼睛周围的肤色（眼睛上方几像素）
    sample_y = max(0, y1 - 5)
    colors = []
    for x in range(x1, min(x2, frame.width)):
        px = frame.getpixel((x, sample_y))
        if len(px) >= 3:
            colors.append(px[:3])
    if not colors:
        return frame
    avg = tuple(sum(c[i] for c in colors) // len(colors) for i in range(3))

    draw = ImageDraw.Draw(frame)
    # 画一条略粗的线代表闭眼
    mid_y = (y1 + y2) // 2
    for dy in range(-1, 2):
        draw.line([(x1 + 3, mid_y + dy), (x2 - 3, mid_y + dy)], fill=avg + (255,), width=1)
    return frame

def make_mouth_open(img, mouth_region):
    """张嘴：把嘴巴区域往下移 2px，露出深色缝隙"""
    frame = img.copy()
    x1, y1, x2, y2 = mouth_region
    # 拷贝嘴巴区域
    mouth = frame.crop((x1, y1, x2, y2))
    # 用嘴巴上方的颜色填充原位置（模拟张开）
    sample_y = max(0, y1 - 2)
    for x in range(x1, min(x2, frame.width)):
        px = frame.getpixel((x, sample_y))
        for y in range(y1, min(y1 + 3, y2)):
            frame.putpixel((x, y), px)
    # 嘴巴下移
    frame.paste(mouth, (x1, y1 + 2))
    return frame

def make_arm_move(img, arm_region):
    """摆手：把手臂区域往左/右移 3px"""
    frame = img.copy()
    x1, y1, x2, y2 = arm_region
    arm = frame.crop((x1, y1, x2, y2))
    # 用背景色填原位
    bg_color = (255, 255, 255, 0)
    draw = ImageDraw.Draw(frame)
    draw.rectangle([x1, y1, x2, y2], fill=bg_color)
    # 手臂左移
    frame.paste(arm, (x1 - 3, y1))
    return frame

def generate_character_frames(name, img):
    """为每个角色生成动画序列"""
    regions = REGIONS.get(name, {})
    frames = [img]  # 帧0: 原图

    eye_r = regions.get('eyes')
    mouth_r = regions.get('mouth')
    arm_r = regions.get('arm')

    if name == 'waibibabu':
        # 歪比巴卜: 原图 → 摆手 → 原图 → 眨眼张嘴
        if arm_r:
            frames.append(make_arm_move(img, arm_r))
        frames.append(img.copy())
        if eye_r and mouth_r:
            f = make_blink_frame(img, eye_r)
            f = make_mouth_open(f, mouth_r)
            frames.append(f)
    elif name == 'bababoyi':
        # 巴巴博一: 原图 → 原图 → 原图 → 眨眼（猫头鹰眨眼慢）
        frames.append(img.copy())
        frames.append(img.copy())
        if eye_r:
            frames.append(make_blink_frame(img, eye_r))
    elif name == 'wodedaodun':
        # 我的刀盾: 基本不动，偶尔张嘴（打哈欠）
        frames.append(img.copy())
        frames.append(img.copy())
        if mouth_r:
            frames.append(make_mouth_open(img, mouth_r))
    else:
        # 其他角色: 原图 → 原图 → 眨眼 → 张嘴
        frames.append(img.copy())
        if eye_r:
            frames.append(make_blink_frame(img, eye_r))
        if mouth_r:
            frames.append(make_mouth_open(img, mouth_r))

    return frames

def animate(name, width=45, fps=2, duration=0):
    img_path = os.path.join(SPRITE_DIR, f"{name}.png")
    if not os.path.exists(img_path):
        print(f"图片不存在: {img_path}")
        return

    names_zh = {
        'bibilabu': '比比拉布', 'bagayalu': '八嘎呀路',
        'wodedaodun': '我的刀盾', 'bababoyi': '巴巴博一',
        'waibibabu': '歪比巴卜', 'gugugaga': '咕咕嘎嘎',
    }

    img = Image.open(img_path).convert("RGBA")

    # 生成动画帧（图片级别）
    img_frames = generate_character_frames(name, img)

    # 预渲染所有帧为终端字符串
    rendered = []
    for f in img_frames:
        rendered.append(render_image(f, width))

    delay = 1.0 / fps
    frame_count = len(rendered)
    zh = names_zh.get(name, name)
    line_count = len(rendered[0].splitlines())

    print(HIDE_CURSOR, end="")
    print(f"\n  {BOLD}{zh}{RESET}（Ctrl+C 退出）\n")

    try:
        i = 0
        while True:
            frame = rendered[i % frame_count]
            for line in frame.splitlines():
                print(f"    {line}")
            sys.stdout.flush()
            time.sleep(delay)
            print(f"\033[{line_count}A", end="")
            i += 1
            if duration > 0 and i > duration * fps:
                break
    except KeyboardInterrupt:
        pass
    finally:
        for line in rendered[0].splitlines():
            print(f"    {line}")
        print(SHOW_CURSOR)
        print()

if __name__ == "__main__":
    name_map = {
        '比比拉布': 'bibilabu', '八嘎呀路': 'bagayalu',
        '我的刀盾': 'wodedaodun', '巴巴博一': 'bababoyi',
        '歪比巴卜': 'waibibabu', '咕咕嘎嘎': 'gugugaga',
    }

    if len(sys.argv) < 2:
        print("用法: python3 animate.py <角色名> [宽度] [fps]")
        print("例: python3 animate.py 歪比巴卜 45 2")
        sys.exit(1)

    name = name_map.get(sys.argv[1], sys.argv[1])
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 45
    fps = float(sys.argv[3]) if len(sys.argv) > 3 else 1.5

    animate(name, width, fps)
