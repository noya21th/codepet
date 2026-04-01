#!/bin/bash
# 宠物渲染 — 隐藏实现细节
# 用法: pet-render.sh <角色ID> <场景> [ascii|popup]
CHARACTER=$1
SCENE=${2:-normal}
MODE=${3:-ascii}
BASE="$HOME/Projects/codepet"

if [ "$MODE" = "ascii" ]; then
    python3 "$BASE/scripts/img2ascii.py" "$BASE/sprites/$CHARACTER/$SCENE.png" 22 2>/dev/null

elif [ "$MODE" = "popup" ]; then
    OS=$(uname -s)

    if [ "$OS" = "Darwin" ]; then
        # macOS: Terminal.app
        osascript -e "
tell application \"Terminal\"
    do script \"export HISTFILE=/dev/null && export BASH_SILENCE_DEPRECATION_WARNING=1 && export PS1='' && clear && python3 '$BASE/scripts/polaroid.py' '$CHARACTER' '$SCENE' 40 2>/dev/null && printf '\\\\033[?25l' && cat > /dev/null\"
    activate
    delay 0.3
    try
        set bounds of front window to {300, 100, 900, 700}
    end try
end tell
" &

    elif [ "$OS" = "MINGW"* ] || [ "$OS" = "MSYS"* ] || [ -n "$WINDIR" ]; then
        # Windows: 用 start cmd 弹新窗口
        start cmd /c "cls && python3 \"$BASE/scripts/polaroid.py\" \"$CHARACTER\" \"$SCENE\" 40 2>nul && pause >nul"

    else
        # Linux/其他: 尝试常见终端
        if command -v gnome-terminal &>/dev/null; then
            gnome-terminal -- bash -c "clear && python3 '$BASE/scripts/polaroid.py' '$CHARACTER' '$SCENE' 40 2>/dev/null && read -n1" &
        elif command -v xterm &>/dev/null; then
            xterm -e "clear && python3 '$BASE/scripts/polaroid.py' '$CHARACTER' '$SCENE' 40 2>/dev/null && read -n1" &
        else
            # 降级：直接在当前终端输出
            python3 "$BASE/scripts/polaroid.py" "$CHARACTER" "$SCENE" 40 2>/dev/null
        fi
    fi
fi
