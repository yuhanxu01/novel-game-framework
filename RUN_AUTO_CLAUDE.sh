#!/bin/bash

###############################################
# Claude Code 完全自动化脚本 - 无需人工干预
#
# 特性：
# - ✅ 100% 自动运行，使用 Claude Code CLI
# - ✅ 自动检测并处理卡死情况
# - ✅ 自动恢复 5 小时额度限制
# - ✅ 实时日志记录
# - ✅ 进度监控和自动重启
#
# 使用方法：
#   ./RUN_AUTO_CLAUDE.sh          # 正常模式
#   ./RUN_AUTO_CLAUDE.sh --meta   # 元任务模式
#   ./RUN_AUTO_CLAUDE.sh --status # 查看状态
###############################################

set -e

# 配置
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 自动化配置
MAX_RUN_TIME=1800          # 单次 claude 最大运行时间（30分钟）
CHECK_INTERVAL=60          # 进度检查间隔（秒）
MAX_IDLE_TIME=600          # 最大空闲时间（10分钟）
LOG_DIR="logs"
STATE_FILE="auto_state.json"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 创建日志目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    local level=$1
    shift
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
    echo -e "$msg" | tee -a "$LOG_DIR/auto_runner.log"
}

# 打印banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║     🤖 Claude Code 完全自动化系统 - 无需人工干预          ║"
    echo "║                                                           ║"
    echo "║     ✅ 100% 自动运行                                      ║"
    echo "║     🔄 自动检测卡死并重启                                 ║"
    echo "║     ⏰ 自动等待额度恢复                                   ║"
    echo "║     📊 实时进度监控                                       ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 检查环境
check_environment() {
    log "INFO" "🔍 检查运行环境..."

    # 检查 claude 命令
    if ! command -v claude &> /dev/null; then
        log "ERROR" "❌ 找不到 claude 命令"
        echo -e "${YELLOW}请先安装 Claude Code CLI：${NC}"
        echo "  npm install -g @anthropic-ai/claude-code"
        exit 1
    fi

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log "ERROR" "❌ 找不到 python3"
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
            log "WARN" "⚠️  找不到 $file"
        fi
    done

    log "INFO" "✅ 环境检查完成"
    echo ""
}

# 显示当前状态
show_status() {
    echo -e "${CYAN}📊 当前状态${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    if [ -f "tools/progress.json" ]; then
        local current=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])" 2>/dev/null || echo "0")
        local total=1694
        local percent=$(python3 -c "print(f'{int($current)/$total*100:.1f}')")

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

    # 显示运行统计
    if [ -f "$STATE_FILE" ]; then
        echo -e "${CYAN}📈 运行统计${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        python3 << 'EOF'
import json
try:
    with open('auto_state.json') as f:
        state = json.load(f)
    print(f"  总运行次数: {state.get('total_runs', 0)} 次")
    print(f"  成功完成: {state.get('successful_runs', 0)} 次")
    print(f"  卡死重启: {state.get('recovered_from_deadlock', 0)} 次")
    print(f"  额度限制: {state.get('quota_limit_hits', 0)} 次")
    print(f"  最后运行: {state.get('last_run_time', 'N/A')}")
except Exception as e:
    print(f"  读取统计失败: {e}")
EOF
        echo ""
    fi
}

# 保存状态
save_state() {
    local key=$1
    local value=$2

    python3 << EOF
import json
from datetime import datetime

try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
except:
    state = {}

state['$key'] = $value
state['last_update'] = datetime.now().isoformat()

with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
EOF
}

# 更新运行统计
update_stats() {
    local event=$1  # start, success, deadlock, quota

    python3 << EOF
import json
from datetime import datetime

try:
    with open('$STATE_FILE', 'r') as f:
        state = json.load(f)
except:
    state = {
        'total_runs': 0,
        'successful_runs': 0,
        'recovered_from_deadlock': 0,
        'quota_limit_hits': 0,
        'last_run_time': None
    }

if '$event' == 'start':
    state['total_runs'] = state.get('total_runs', 0) + 1
    state['last_run_time'] = datetime.now().isoformat()
elif '$event' == 'success':
    state['successful_runs'] = state.get('successful_runs', 0) + 1
elif '$event' == 'deadlock':
    state['recovered_from_deadlock'] = state.get('recovered_from_deadlock', 0) + 1
elif '$event' == 'quota':
    state['quota_limit_hits'] = state.get('quota_limit_hits', 0) + 1

with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
EOF
}

# 生成任务文件
generate_task() {
    local mode=$1

    log "INFO" "📝 生成任务指令..."

    if [ "$mode" = "meta" ]; then
        python3 smart_task_generator.py meta > CURRENT_TASK.md
        log "INFO" "✅ 元任务已生成"
    else
        python3 smart_task_generator.py > CURRENT_TASK.md
        log "INFO" "✅ 任务已生成"
    fi

    echo ""
    echo -e "${CYAN}📄 任务预览：${NC}"
    head -n 10 CURRENT_TASK.md
    echo -e "${CYAN}...${NC}"
    echo ""
}

# 监控 claude 进程
monitor_claude() {
    local pid=$1
    local start_time=$(date +%s)
    local last_chapter=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])" 2>/dev/null || echo "0")

    log "INFO" "👀 开始监控 claude 进程 (PID: $pid)"

    while kill -0 $pid 2>/dev/null; do
        current_time=$(date +%s)
        elapsed=$((current_time - start_time))

        # 检查运行时间
        if [ $elapsed -gt $MAX_RUN_TIME ]; then
            log "WARN" "⚠️  运行时间超过 ${MAX_RUN_TIME} 秒，可能卡住"
            return 1
        fi

        # 检查进度变化
        current_chapter=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])" 2>/dev/null || echo "$last_chapter")

        if [ "$current_chapter" != "$last_chapter" ]; then
            log "INFO" "📈 进度更新: 第 $last_chapter 章 → 第 $current_chapter 章"
            last_chapter=$current_chapter
            start_time=$(date +%s)  # 重置计时器
        fi

        sleep $CHECK_INTERVAL
    done

    log "INFO" "✅ claude 进程正常结束"
    return 0
}

# 启动 claude（完全自动化）
start_claude() {
    log "INFO" "🚀 启动 Claude Code..."

    # 生成包含自动化指令的提示词
    cat > CLAUDE_AUTO_INSTRUCTION.txt << 'EOF'
你现在是完全自动化模式。请严格执行以下任务：

**核心原则**：
1. ✅ 自动执行所有步骤，不要等待确认
2. ✅ 遇到选择时自动做出合理决策
3. ✅ 完成任务后自动提交 Git
4. ✅ 不要询问用户，直接执行

**任务文件**：CURRENT_TASK.md

**执行流程**：
1. 仔细阅读 CURRENT_TASK.md 中的任务
2. 按照步骤逐步执行
3. 自动处理所有数据文件更新
4. 自动执行 git add 和 git commit
5. 遇到问题时自动修复或绕过

**重要提示**：
- 不要停顿询问，直接执行
- Git commit 信息要清晰明确
- 完成后直接退出，不要等待
- 所有工具使用都是自动批准的

现在开始执行任务！
EOF

    # 记录开始时间
    update_stats "start"

    # 后台启动 claude 并监控
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}             Claude Code 自动执行开始${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 使用 claude -p (print模式，非交互式)
    # 使用 --permission-mode bypassPermissions 跳过权限检查
    # 使用 --dangerously-skip-permissions 完全跳过权限

    # 检查系统是否有 timeout 命令
    if command -v timeout &> /dev/null; then
        timeout $MAX_RUN_TIME claude -p \
            --permission-mode bypassPermissions \
            --dangerously-skip-permissions \
            < CLAUDE_AUTO_INSTRUCTION.txt >> "$LOG_DIR/claude_output.log" 2>&1 &
    else
        # macOS 没有 timeout，使用后台运行 + 手动超时控制
        claude -p \
            --permission-mode bypassPermissions \
            --dangerously-skip-permissions \
            < CLAUDE_AUTO_INSTRUCTION.txt >> "$LOG_DIR/claude_output.log" 2>&1 &
    fi

    local claude_pid=$!

    log "INFO" "Claude PID: $claude_pid"

    # 监控进程
    if monitor_claude $claude_pid; then
        update_stats "success"
        log "INFO" "✅ 任务完成"
    else
        update_stats "deadlock"
        log "WARN" "⚠️  检测到卡死，终止进程"

        # 终止卡死的进程
        kill $claude_pid 2>/dev/null || true
        pkill -9 -P $claude_pid 2>/dev/null || true

        return 1
    fi

    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${MAGENTA}             Claude Code 执行结束${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 清理
    rm -f CLAUDE_AUTO_INSTRUCTION.txt
}

# 检查是否触发额度限制
check_quota_limit() {
    if [ -f "$LOG_DIR/claude_output.log" ]; then
        # 更准确的检测：只检测真正的额度限制错误
        if grep -qi "rate limit exceeded\|quota exceeded\|429\|usage limit\| hourly.*limit" "$LOG_DIR/claude_output.log"; then
            log "WARN" "⚠️  检测到额度限制"
            update_stats "quota"
            return 1
        fi
    fi
    return 0
}

# 等待额度恢复
wait_quota_recovery() {
    local wait_hours=5
    local wait_seconds=$((wait_hours * 3600))

    log "INFO" "⏳ 等待 ${wait_hours} 小时额度恢复..."
    log "INFO" "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    log "INFO" "恢复时间: $(date -v+5H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || date -d '+5 hours' '+%Y-%m-%d %H:%M:%S' 2>/dev/null)"
    echo ""

    # Mac 防休眠
    if command -v caffeinate &> /dev/null; then
        log "INFO" "💊 已启用 caffeinate 防止休眠"
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
    log "INFO" "✅ 等待结束，继续执行"

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
                echo "  --once      只运行一次"
                echo "  --help      显示帮助"
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
    local consecutive_failures=0
    local max_failures=3

    while true; do
        run_count=$((run_count + 1))

        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${CYAN}               第 ${run_count} 次运行${NC}"
        echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        # 生成任务
        generate_task "$mode"

        # 启动 claude
        if start_claude; then
            consecutive_failures=0
        else
            consecutive_failures=$((consecutive_failures + 1))
            log "WARN" "⚠️  本次运行异常 (连续失败: $consecutive_failures/$max_failures)"

            if [ $consecutive_failures -ge $max_failures ]; then
                log "ERROR" "❌ 连续失败 ${max_failures} 次，停止运行"
                exit 1
            fi
        fi

        # 检查额度限制（函数返回1表示检测到额度限制）
        if ! check_quota_limit; then
            if [ "$auto_continue" = true ]; then
                wait_quota_recovery
            else
                log "INFO" "检测到额度限制，退出"
                exit 0
            fi
        fi

        # 检查是否完成
        if [ -f "tools/progress.json" ]; then
            local current=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])" 2>/dev/null || echo "0")
            if [ "$current" -ge 1694 ]; then
                log "INFO" "🎉 所有章节已处理完成！"
                break
            fi
        fi

        # 是否继续
        if [ "$auto_continue" = false ]; then
            log "INFO" "单次运行模式，退出"
            break
        fi

        # 休息
        log "INFO" "😴 休息 30 秒后继续..."
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
trap 'echo ""; log "INFO" "⚠️  收到中断信号，安全退出..."; exit 0' INT TERM

# 启动
main "$@"
