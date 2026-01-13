#!/bin/bash

###############################################
# OpenCode 一键启动脚本 - Mac 优化版
#
# 使用方法：
#   ./START_AUTO.sh          # 正常模式
#   ./START_AUTO.sh --meta   # 元任务模式（让AI改进系统）
#   ./START_AUTO.sh --resume # 恢复上次进度
#   ./START_AUTO.sh --status # 查看当前状态
###############################################

set -e

# 配置
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 打印banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║     🤖 OpenCode 自动化处理系统 - 完全托管模式             ║"
    echo "║                                                           ║"
    echo "║     📖 自动处理小说 → 分析 → 游戏化                       ║"
    echo "║     🔄 自动恢复 5小时额度限制                             ║"
    echo "║     🧠 AI 自我学习和改进                                  ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查环境
check_environment() {
    echo -e "${BLUE}🔍 检查运行环境...${NC}"

    # 检查 opencode 命令
    if ! command -v opencode &> /dev/null; then
        echo -e "${RED}❌ 错误：找不到 opencode 命令${NC}"
        echo -e "${YELLOW}请确保 opencode 已正确安装并配置${NC}"
        echo -e "${YELLOW}安装方法：https://github.com/anthropics/claude-code${NC}"
        exit 1
    fi

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ 错误：找不到 python3${NC}"
        exit 1
    fi

    # 检查必要文件
    local required_files=(
        "novel/斗破苍穹.txt"
        "tools/progress.json"
        "smart_task_generator.py"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo -e "${YELLOW}⚠️  警告：找不到 $file${NC}"
        fi
    done

    echo -e "${GREEN}✅ 环境检查完成${NC}"
    echo ""
}

# 显示当前状态
show_status() {
    echo -e "${CYAN}📊 当前状态${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ -f "tools/progress.json" ]; then
        local current=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])")
        local total=1694
        local percent=$(python3 -c "print(f'{$current/$total*100:.1f}')")

        echo -e "  当前章节: ${GREEN}第 $current 章${NC}"
        echo -e "  总章节数: $total 章"
        echo -e "  完成进度: ${GREEN}${percent}%${NC}"
        echo -e "  剩余章节: $((total - current)) 章"

        # 进度条
        local filled=$((current * 50 / total))
        local empty=$((50 - filled))
        printf "  ["
        printf "${GREEN}%0.s█${NC}" $(seq 1 $filled)
        printf "%0.s░" $(seq 1 $empty)
        printf "]\n"
    else
        echo -e "  ${YELLOW}无进度信息${NC}"
    fi

    echo ""

    if [ -f "auto_runner_state.json" ]; then
        echo -e "${CYAN}📈 运行统计${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        python3 << 'EOF'
import json
try:
    with open('auto_runner_state.json') as f:
        state = json.load(f)
    print(f"  运行次数: {state.get('run_count', 0)} 次")
    print(f"  已处理章节: {state.get('total_chapters_processed', 0)} 章")
    print(f"  额度限制次数: {state.get('quota_exhausted_count', 0)} 次")
    if state.get('last_run_time'):
        print(f"  最后运行: {state['last_run_time']}")
except:
    print("  无统计数据")
EOF
        echo ""
    fi

    if [ -f "task_learning.json" ]; then
        echo -e "${CYAN}🧠 学习记录${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        python3 << 'EOF'
import json
try:
    with open('task_learning.json') as f:
        learning = json.load(f)
    print(f"  记录的错误: {len(learning.get('common_errors', []))} 条")
    print(f"  成功模式: {len(learning.get('successful_patterns', []))} 条")
    print(f"  改进建议: {len(learning.get('script_improvements', []))} 条")
    print(f"  最佳实践: {len(learning.get('best_practices', []))} 条")
except:
    print("  无学习记录")
EOF
        echo ""
    fi
}

# 生成任务文件
generate_task() {
    local mode=$1

    echo -e "${BLUE}📝 生成任务指令...${NC}"

    if [ "$mode" = "meta" ]; then
        python3 smart_task_generator.py meta > CURRENT_AUTO_TASK.md
        echo -e "${GREEN}✅ 元任务已生成（让 AI 改进系统）${NC}"
    else
        python3 smart_task_generator.py > CURRENT_AUTO_TASK.md
        echo -e "${GREEN}✅ 任务已生成${NC}"
    fi

    echo ""
    echo -e "${CYAN}📄 任务预览：${NC}"
    head -n 10 CURRENT_AUTO_TASK.md
    echo -e "${CYAN}...${NC}"
    echo ""
}

# 启动 OpenCode
start_opencode() {
    echo -e "${GREEN}🚀 启动 OpenCode...${NC}"
    echo -e "${YELLOW}💡 提示：OpenCode 将自动执行任务，无需手动输入${NC}"
    echo ""

    # 创建临时输入文件
    local input_file=$(mktemp)

    cat > "$input_file" << 'EOF'
你好！请按照 CURRENT_AUTO_TASK.md 文件中的指令完成任务。

任务文件路径：/home/user/novel-game-framework/CURRENT_AUTO_TASK.md

请：
1. 仔细阅读任务文件
2. 按步骤执行所有指令
3. 遇到问题时记录到 task_learning.json
4. 完成后提交 Git

如果你发现系统可以改进的地方，请大胆修改脚本和提示词！

现在开始执行。
EOF

    # 启动 opencode
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}             OpenCode 会话开始${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 运行 opencode（Mac 版本使用 cat 输入）
    cat "$input_file" | opencode

    # 清理
    rm -f "$input_file"

    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}             OpenCode 会话结束${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 检查是否需要等待额度
check_quota() {
    # 检查最近的日志是否有额度限制错误
    if [ -d "logs" ]; then
        local latest_log=$(ls -t logs/opencode_session_*.log 2>/dev/null | head -n 1)
        if [ -n "$latest_log" ] && grep -qi "rate limit\|quota\|429" "$latest_log"; then
            echo -e "${YELLOW}⚠️  检测到可能的额度限制${NC}"
            return 1
        fi
    fi
    return 0
}

# 等待额度恢复
wait_quota() {
    local wait_hours=5
    local wait_seconds=$((wait_hours * 3600))

    echo -e "${YELLOW}⏳ 等待 5 小时额度恢复...${NC}"
    echo -e "${CYAN}开始时间: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${CYAN}恢复时间: $(date -v+5H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -d '+5 hours' '+%Y-%m-%d %H:%M:%S' 2>/dev/null)${NC}"
    echo ""

    # 在 Mac 上使用 caffeinate 防止休眠
    if command -v caffeinate &> /dev/null; then
        echo -e "${BLUE}💊 已启用 caffeinate 防止系统休眠${NC}"
        caffeinate -i -w $$ &
        local caffeinate_pid=$!
    fi

    local end_time=$(($(date +%s) + wait_seconds))

    while [ $(date +%s) -lt $end_time ]; do
        local remaining=$((end_time - $(date +%s)))
        local hours=$((remaining / 3600))
        local minutes=$(((remaining % 3600) / 60))
        local seconds=$((remaining % 60))

        printf "\r${YELLOW}⏰ 剩余: %02d:%02d:%02d ${NC}" $hours $minutes $seconds
        sleep 1
    done

    echo ""
    echo -e "${GREEN}✅ 等待结束，准备继续${NC}"
    echo ""

    # 停止 caffeinate
    if [ -n "$caffeinate_pid" ]; then
        kill $caffeinate_pid 2>/dev/null || true
    fi
}

# 主函数
main() {
    local mode="normal"
    local auto_continue=true

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --meta)
                mode="meta"
                shift
                ;;
            --status)
                print_banner
                show_status
                exit 0
                ;;
            --once)
                auto_continue=false
                shift
                ;;
            --help)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --meta      元任务模式（让 AI 改进系统）"
                echo "  --status    查看当前状态"
                echo "  --once      只运行一次，不自动继续"
                echo "  --help      显示此帮助信息"
                exit 0
                ;;
            *)
                echo "未知参数: $1"
                echo "使用 --help 查看帮助"
                exit 1
                ;;
        esac
    done

    # 显示 banner
    print_banner

    # 检查环境
    check_environment

    # 显示状态
    show_status

    # 主循环
    local run_count=0

    while true; do
        run_count=$((run_count + 1))

        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${CYAN}               第 ${run_count} 次运行${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        # 生成任务
        generate_task "$mode"

        # 启动 OpenCode
        start_opencode

        # 检查是否需要等待额度
        if ! check_quota; then
            if [ "$auto_continue" = true ]; then
                wait_quota
            else
                echo -e "${YELLOW}检测到额度限制，退出（使用不带 --once 参数可自动等待）${NC}"
                exit 0
            fi
        fi

        # 检查是否完成
        if [ -f "tools/progress.json" ]; then
            local current=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])")
            if [ "$current" -ge 1694 ]; then
                echo -e "${GREEN}🎉 所有章节已处理完成！${NC}"
                break
            fi
        fi

        # 是否继续
        if [ "$auto_continue" = false ]; then
            echo -e "${YELLOW}单次运行模式，退出${NC}"
            break
        fi

        # 短暂休息
        echo -e "${BLUE}😴 休息 30 秒后继续...${NC}"
        sleep 30
        echo ""
    done

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}              运行完成${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}总运行次数: ${run_count}${NC}"
    echo ""
    show_status
}

# 信号处理
trap 'echo ""; echo -e "${YELLOW}⚠️  收到中断信号，正在安全退出...${NC}"; exit 0' INT TERM

# 启动
main "$@"
