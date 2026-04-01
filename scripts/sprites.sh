#!/bin/bash
# CodePet 彩色角色精灵渲染器
# 用法: sprites.sh [角色名] [状态]
# 角色: bibilabu / bagayalu / wodedaodun / bababoyi / waibibabu / gugugaga / all
# 状态: normal / happy / sleep (默认 normal)

# ── 调色板（基于原图取色）──
Y=$'\033[38;2;230;190;50m'      # 香蕉黄
YD=$'\033[38;2;200;160;30m'     # 香蕉暗黄
YL=$'\033[38;2;245;220;100m'    # 香蕉亮黄
WF=$'\033[38;2;240;220;190m'    # 猫脸米白
BH=$'\033[38;2;170;120;70m'     # 猫发棕
CB=$'\033[38;2;185;125;65m'     # 水豚棕
CD=$'\033[38;2;145;95;45m'      # 水豚深棕
CL=$'\033[38;2;215;185;145m'    # 水豚浅棕
OB=$'\033[38;2;215;185;135m'    # 猫头鹰米色
OD=$'\033[38;2;115;75;35m'      # 猫头鹰眼圈深棕
OG=$'\033[38;2;130;130;135m'    # 猫头鹰耳灰
WT=$'\033[38;2;235;235;235m'    # 白T恤
JN=$'\033[38;2;75;95;135m'      # 牛仔裤蓝
PG=$'\033[38;2;75;75;85m'       # 企鹅灰
PB=$'\033[38;2;45;45;50m'       # 企鹅刘海黑
PW=$'\033[38;2;235;230;215m'    # 企鹅白肚
PK=$'\033[38;2;215;135;135m'    # 粉嘴/腮红
BK=$'\033[38;2;35;35;35m'       # 黑
R=$'\033[0m'                     # 重置
B=$'\033[1m'                     # 粗体

CHARACTER=${1:-all}
STATE=${2:-normal}

render_bibilabu() {
    local state=${1:-normal}
    local eyes_l="·" eyes_r="·" mouth="ω" extra="" tail=""
    case $state in
        happy)  eyes_l="^" eyes_r="^" mouth="▽" tail="~" ;;
        sleep)  eyes_l="-" eyes_r="-" mouth="ω" extra=" zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}比比拉布${R}（香蕉猫）\n\n"
    printf "       ${YL}_(${R} ${YL})_${R}\n"
    printf "      ${Y}/ ${BH}|${R} ${BH}|${Y} \\${R}\n"
    printf "     ${Y}/${R}  ${WF}${eyes_l} ${eyes_r}${R}  ${Y}\\${R}\n"
    printf "     ${Y}|${R}  ${PK} ${mouth} ${R}  ${Y}|${R}\n"
    printf "     ${Y}|${YD}------${Y}|${R}\n"
    printf "     ${YD}| |  | |${R}\n"
    printf "     ${YD}| |  | |${R}\n"
    printf "      ${YD}\\ \\/ /${R}\n"
    printf "       ${YD}\\__/${R}${tail}\n"
    printf "      ${WF} _|  |_${R}${extra}\n"
    printf "\n"
}

render_bagayalu() {
    local state=${1:-normal}
    local eyes_l="·" eyes_r="·" extra=""
    case $state in
        happy)  eyes_l="^" eyes_r="^" ;;
        sleep)  eyes_l="-" eyes_r="-" extra=" zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}八嘎呀路${R}（坐姿水豚）\n\n"
    printf "          ${CD}__${R}\n"
    printf "        ${CB}/${CD}(${CB}  ${CD})${CB}\\${R}\n"
    printf "       ${CB}/        \\${R}\n"
    printf "      ${CB}/ ${BK}${eyes_l}${R}    ${BK}${eyes_r}${R} ${CB}\\${R}\n"
    printf "     ${CB}|    ${CD}nn${CB}    |${R}\n"
    printf "     ${CB}|  ${CL}\`----'${CB}  |${R}\n"
    printf "      ${CB}\\  ${CL}____${CB}  /${R}\n"
    printf "       ${CB}\\${CD}|    |${CB}/${R}\n"
    printf "        ${CD}_|  |_${R}${extra}\n"
    printf "\n"
}

render_wodedaodun() {
    local state=${1:-normal}
    local eyes_l="·" eyes_r="·" extra=""
    case $state in
        happy)  eyes_l="^" eyes_r="^" extra="  ♪" ;;
        sleep)  eyes_l="-" eyes_r="-" extra="  zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}我的刀盾${R}（趴姿水豚）\n\n"
    printf "         ${CD}__${CB}______${R}\n"
    printf "        ${CB}/${BK}${eyes_l} ${eyes_r}${CB}      \\${R}${extra}\n"
    printf "       ${CB}| ${CD}nn${CB}        |${R}\n"
    printf "        ${CB}\\${CL}__________${CB}/${R}\n"
    printf "        ${CD}_||      ||_${R}\n"
    printf "\n"
}

render_bababoyi() {
    local state=${1:-normal}
    local eyes_l="◉" eyes_r="◉" extra=""
    case $state in
        happy)  eyes_l="★" eyes_r="★" ;;
        sleep)  eyes_l="-" eyes_r="-" extra=" zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}巴巴博一${R}（猫头鹰）\n\n"
    printf "         ${OG}/\\${R}      ${OG}/\\${R}\n"
    printf "        ${OB}/            \\${R}\n"
    printf "       ${OB}/${R} ${OD}(${BK}${eyes_l}${OD})${R}    ${OD}(${BK}${eyes_r}${OD})${R} ${OB}\\${R}\n"
    printf "      ${OB}|${R}      ${CD}<>${R}      ${OB}|${R}\n"
    printf "      ${OB}|${R}  ${CL}\\________/${R}  ${OB}|${R}\n"
    printf "       ${OB}\\${R}  ${CL}________${R}  ${OB}/${R}\n"
    printf "        ${OB}\\__________/${R}\n"
    printf "          ${CD}_||  ||_${R}${extra}\n"
    printf "\n"
}

render_waibibabu() {
    local state=${1:-normal}
    local eyes_l="·" eyes_r="·" mouth=":----:" extra=""
    case $state in
        happy)  eyes_l="^" eyes_r="^" mouth=":▽▽▽:" ;;
        sleep)  eyes_l="-" eyes_r="-" extra=" zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}歪比巴卜${R}（水豚大叔）\n\n"
    printf "          ${CB} ____${R}\n"
    printf "         ${CB}/ ${BK}${eyes_l}  ${eyes_r}${CB} \\${R}\n"
    printf "        ${CB}| ${CD}${mouth}${CB} |${R}\n"
    printf "         ${CB}\\${CD}____${CB}/${R}\n"
    printf "       ${WT} /|‾‾‾‾‾‾|\\${R}\n"
    printf "      ${WT}/ |${R}  ${CB}><${R}  ${WT}| \\${R}\n"
    printf "      ${WT}| |______| |${R}\n"
    printf "         ${JN}| |  | |${R}\n"
    printf "         ${JN}|_|  |_|${R}${extra}\n"
    printf "\n"
}

render_gugugaga() {
    local state=${1:-normal}
    local eyes_l="·" eyes_r="·" beak="▼" extra=""
    case $state in
        happy)  eyes_l="^" eyes_r="^" beak="▽" ;;
        sleep)  eyes_l="-" eyes_r="-" extra=" zzZ" ;;
    esac

    printf "\n"
    printf "  ${B}咕咕嘎嘎${R}（企鹅）\n\n"
    printf "          ${PB}_____${R}\n"
    printf "        ${PB}/ ||||| \\${R}\n"
    printf "       ${PB}/ ||||||| \\${R}\n"
    printf "      ${PG}|${R} ${BK}${eyes_l}${R}       ${BK}${eyes_r}${R} ${PG}|${R}\n"
    printf "      ${PG}|${R}    ${PK}${beak}${R}     ${PG}|${R}\n"
    printf "       ${PG}\\${R}  ${PW}____${R}  ${PG}/${R}\n"
    printf "        ${PG}\\${PW}______${PG}/${R}\n"
    printf "         ${PG}_|  |_${R}${extra}\n"
    printf "\n"
}

# ── 主入口 ──
case $CHARACTER in
    bibilabu|比比拉布)   render_bibilabu "$STATE" ;;
    bagayalu|八嘎呀路)   render_bagayalu "$STATE" ;;
    wodedaodun|我的刀盾) render_wodedaodun "$STATE" ;;
    bababoyi|巴巴博一)   render_bababoyi "$STATE" ;;
    waibibabu|歪比巴卜)  render_waibibabu "$STATE" ;;
    gugugaga|咕咕嘎嘎)   render_gugugaga "$STATE" ;;
    all)
        echo ""
        echo "═══════════════════════════════════════"
        echo "      🐾 CodePet 角色画廊（彩色版）"
        echo "═══════════════════════════════════════"
        for char in bibilabu bagayalu wodedaodun bababoyi waibibabu gugugaga; do
            for s in normal happy sleep; do
                render_${char} "$s"
            done
            echo "───────────────────────────────────────"
        done
        ;;
    *)
        echo "用法: $0 [角色] [状态]"
        echo "角色: bibilabu/bagayalu/wodedaodun/bababoyi/waibibabu/gugugaga/all"
        echo "状态: normal/happy/sleep"
        ;;
esac
