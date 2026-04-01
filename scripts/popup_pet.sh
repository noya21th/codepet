#!/bin/bash
# 弹出新终端窗口显示拍立得宠物 — 后台运行不阻塞
CHARACTER=${1:-bagayalu}
SCENE=${2:-normal}
POLAROID="$HOME/Projects/codepet/scripts/polaroid.py"

# 预计算窗口尺寸
SIZES=$(python3 "$POLAROID" "$CHARACTER" "$SCENE" 40 2>&1 1>/dev/null | grep "ROWS:")
ROWS=$(echo "$SIZES" | sed 's/ROWS:\([0-9]*\).*/\1/')
COLS=$(echo "$SIZES" | sed 's/.*COLS:\([0-9]*\)/\1/')
ROWS=${ROWS:-35}
COLS=${COLS:-55}
ROWS=$((ROWS + 4))
COLS=$((COLS + 8))

# 后台启动，不阻塞调用者
osascript << EOF &
tell application "Terminal"
    activate
    do script "export HISTFILE=/dev/null && export BASH_SILENCE_DEPRECATION_WARNING=1 && export PS1='' && clear && python3 '$POLAROID' '$CHARACTER' '$SCENE' 40 2>/dev/null && printf '\\033[?25l' && cat > /dev/null"
    delay 0.3
    set number of rows of front window to $ROWS
    set number of columns of front window to $COLS
    set bounds of front window to {400, 150, $((400 + COLS * 8)), $((150 + ROWS * 16))}
end tell
EOF

# 立即返回
exit 0
