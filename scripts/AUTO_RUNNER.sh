#!/bin/bash

#############################################
# OpenCode 自动化运行器 - 完全托管模式
# 功能：
# 1. 自动生成任务指令
# 2. 启动 OpenCode 执行
# 3. 监控进度和错误
# 4. 自动处理5小时额度限制
# 5. 持续运行直到所有章节完成
#############################################

set -e

# 配置
PROJECT_DIR="/home/user/novel-game-framework"
LOG_DIR="$PROJECT_DIR/logs"
STATE_FILE="$PROJECT_DIR/auto_runner_state.json"
TASK_FILE="$PROJECT_DIR/CURRENT_AUTO_TASK.md"
PROGRESS_FILE="$PROJECT_DIR/tools/progress.json"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 创建必要的目录
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_DIR/auto_runner.log"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}" | tee -a "$LOG_DIR/auto_runner.log"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}" | tee -a "$LOG_DIR/auto_runner.log"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}" | tee -a "$LOG_DIR/auto_runner.log"
}

log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️  $1${NC}" | tee -a "$LOG_DIR/auto_runner.log"
}

# 初始化状态文件
init_state() {
    if [ ! -f "$STATE_FILE" ]; then
        cat > "$STATE_FILE" << 'EOF'
{
    "run_count": 0,
    "total_chapters_processed": 0,
    "last_run_time": null,
    "quota_exhausted_count": 0,
    "last_quota_exhausted_time": null,
    "script_improvements": []
}
EOF
        log_success "状态文件已初始化"
    fi
}

# 更新状态
update_state() {
    local key=$1
    local value=$2
    python3 << EOF
import json
with open('$STATE_FILE', 'r') as f:
    state = json.load(f)
state['$key'] = $value
with open('$STATE_FILE', 'w') as f:
    json.dump(state, f, indent=2)
EOF
}

# 获取当前进度
get_current_chapter() {
    python3 << 'EOF'
import json
try:
    with open('/home/user/novel-game-framework/tools/progress.json', 'r') as f:
        data = json.load(f)
        print(data.get('current_chapter', 30))
except:
    print(30)
EOF
}

# 生成任务指令
generate_task() {
    local current_chapter=$1
    local next_chapter=$((current_chapter + 1))
    local review_checkpoint=$((((current_chapter / 10) + 1) * 10))

    log_info "生成任务：处理第 ${next_chapter} 章"

    cat > "$TASK_FILE" << EOF
# 自动化任务 - 第 ${next_chapter} 章处理

## 🎯 当前目标
处理小说《斗破苍穹》第 **${next_chapter}** 章，并更新游戏数据。

## 📋 任务步骤

### 1️⃣ 读取小说章节
- 使用 Read 工具读取 \`novel/斗破苍穹.txt\`
- 找到第 ${next_chapter} 章的内容（根据章节标题定位）
- **完整阅读**章节内容，不要跳过任何段落

### 2️⃣ 分析章节内容
使用 \`prompts/01-小说分析器.md\` 的模板，分析本章：
- 核心事件
- 新角色、新地点、新设定、新物品
- 角色动态和关系变化
- 剧情分析（因果链、伏笔、冲突、悬念）
- 游戏化潜力（选择点、属性、物品、探索元素）

保存到：\`data/chapter_summaries/chapter_${next_chapter}.json\`

### 3️⃣ 更新累积上下文
- 读取 \`data/accumulated_context.json\`
- 添加本章发现的新角色、地点、物品、世界观元素
- 更新前文摘要
- 保存更新后的文件

### 4️⃣ 更新角色数据
如果发现新角色或角色有重要发展：
- 读取 \`data/characters.json\`
- 添加新角色或更新现有角色信息
- 使用 \`prompts/03-角色分析器.md\` 模板
- 保存更新后的文件

### 5️⃣ 更新世界观数据
如果发现新的世界观元素：
- 读取 \`data/world_setting.json\`
- 添加或更新相关信息
- 保存更新后的文件

### 6️⃣ 生成游戏内容（可选）
如果本章有重要剧情，考虑转换为游戏场景：
- 创建场景节点（narration/dialogue/choice）
- 设计选择点和效果
- 更新 \`frontend/data/game_data_doupo.json\`

### 7️⃣ 更新进度
- 读取 \`tools/progress.json\`
- 更新 current_chapter 为 ${next_chapter}
- 如果达到第 ${review_checkpoint} 章，设置 needs_review 为 true
- 保存更新后的文件

### 8️⃣ 提交到 Git
\`\`\`bash
git add -A
git commit -m "处理第${next_chapter}章：[章节标题]

- 完成章节分析和数据提取
- 更新角色和世界观信息
- 更新游戏内容（如适用）"
git push -u origin claude/automate-novel-writing-rwmkK
\`\`\`

## ⚠️ 重要提醒

1. **不要跳过阅读**：必须完整读取章节原文
2. **保持数据一致性**：更新文件时要保持 JSON 格式正确
3. **详细分析**：不要敷衍，要深入分析剧情和角色
4. **检查进度**：确保 progress.json 正确更新
5. **提交代码**：完成后务必 git commit 和 push

## 🔄 完成标志
当你看到以下输出时，任务完成：
- ✅ 第 ${next_chapter} 章分析完成
- ✅ 所有数据文件已更新
- ✅ Git 提交成功

完成后，脚本会自动继续下一章。

---

**当前进度**: ${current_chapter}/1694 章 ($(python3 -c "print(f'{${current_chapter}/1694*100:.1f}')"))%
**下一个回顾检查点**: 第 ${review_checkpoint} 章
EOF

    log_success "任务指令已生成：$TASK_FILE"
}

# 生成回顾任务
generate_review_task() {
    local current_chapter=$1
    local review_num=$((current_chapter / 10))
    local start_chapter=$((((review_num - 1) * 10) + 1))
    local end_chapter=$current_chapter

    log_info "生成回顾任务：第 ${start_chapter}-${end_chapter} 章"

    cat > "$TASK_FILE" << EOF
# 自动化回顾任务 - 第 ${review_num} 次回顾

## 🎯 回顾范围
第 **${start_chapter}-${end_chapter}** 章

## 📋 回顾步骤

### 1️⃣ 读取所有章节分析
使用 Read 工具读取：
\`\`\`
data/chapter_summaries/chapter_${start_chapter}.json
data/chapter_summaries/chapter_$((start_chapter + 1)).json
...
data/chapter_summaries/chapter_${end_chapter}.json
\`\`\`

### 2️⃣ 统计分析
- 新角色数量
- 新地点数量
- 新物品数量
- 新世界观元素数量
- 核心事件列表

### 3️⃣ 质量检查
- **完整性**：每章是否都有完整分析？
- **一致性**：角色信息前后是否矛盾？
- **准确性**：是否忠实于原著？

### 4️⃣ 生成回顾报告
创建文件：\`data/reviews/review_${review_num}.md\`

报告应包含：
- 章节概览（每章一句话总结）
- 数据统计
- 质量评估
- 发现的问题（如有）
- 改进建议（如有）

### 5️⃣ 更新进度
- 读取 \`tools/progress.json\`
- 设置 needs_review 为 false
- 设置 last_review_chapter 为 ${end_chapter}
- 保存

### 6️⃣ 自动批准
如果质量合格（完整性>95%，一致性良好），在报告末尾写：
\`\`\`
## ✅ 审核结果
状态：通过
批准：自动批准
\`\`\`

### 7️⃣ 提交到 Git
\`\`\`bash
git add -A
git commit -m "完成第${review_num}次回顾检查（第${start_chapter}-${end_chapter}章）"
git push -u origin claude/automate-novel-writing-rwmkK
\`\`\`

## 🔄 完成标志
- ✅ 回顾报告已生成
- ✅ 质量检查通过
- ✅ 进度已更新
- ✅ Git 提交成功

完成后，脚本会继续处理下一章。
EOF

    log_success "回顾任务指令已生成：$TASK_FILE"
}

# 检查是否需要回顾
needs_review() {
    python3 << 'EOF'
import json
try:
    with open('/home/user/novel-game-framework/tools/progress.json', 'r') as f:
        data = json.load(f)
        print('yes' if data.get('needs_review', False) else 'no')
except:
    print('no')
EOF
}

# 运行 OpenCode
run_opencode() {
    local session_log="$LOG_DIR/opencode_session_$(date '+%Y%m%d_%H%M%S').log"

    log_info "启动 OpenCode 会话..."
    log_info "会话日志：$session_log"

    cd "$PROJECT_DIR"

    # 运行 opencode，输入任务文件内容
    (
        echo "请按照文件 $TASK_FILE 中的指令完成任务。"
        echo ""
        echo "任务文件内容："
        cat "$TASK_FILE"
        echo ""
        echo "现在开始执行任务，完成后输入 /exit 退出。"
    ) | opencode 2>&1 | tee "$session_log"

    local exit_code=$?

    # 分析日志，判断是否遇到额度限制
    if grep -qi "rate limit\|quota\|too many requests\|429" "$session_log"; then
        log_warning "检测到额度限制"
        return 429
    elif grep -qi "error\|failed\|exception" "$session_log"; then
        log_error "执行过程中出现错误"
        return 1
    else
        log_success "OpenCode 会话正常结束"
        return 0
    fi
}

# 等待额度恢复
wait_for_quota() {
    local wait_hours=5
    local wait_seconds=$((wait_hours * 3600))

    log_warning "⏳ 触发5小时额度限制"
    log_info "将等待 ${wait_hours} 小时后重新启动..."

    update_state "quota_exhausted_count" "$(python3 -c "import json; f=open('$STATE_FILE'); d=json.load(f); print(d.get('quota_exhausted_count', 0) + 1); f.close()")"
    update_state "last_quota_exhausted_time" "\"$(date '+%Y-%m-%d %H:%M:%S')\""

    local end_time=$(($(date +%s) + wait_seconds))

    while [ $(date +%s) -lt $end_time ]; do
        local remaining=$((end_time - $(date +%s)))
        local hours=$((remaining / 3600))
        local minutes=$(((remaining % 3600) / 60))
        local seconds=$((remaining % 60))

        echo -ne "\r${YELLOW}⏰ 剩余等待时间: ${hours}h ${minutes}m ${seconds}s ${NC}"
        sleep 10
    done

    echo ""
    log_success "等待结束，准备重新启动"
}

# 主循环
main() {
    log_success "=========================================="
    log_success "  OpenCode 自动化运行器已启动"
    log_success "=========================================="
    log_info "项目目录: $PROJECT_DIR"
    log_info "日志目录: $LOG_DIR"
    log_info ""

    init_state

    local run_count=0
    local max_runs=1000  # 防止无限循环

    while [ $run_count -lt $max_runs ]; do
        run_count=$((run_count + 1))

        log_info "=========================================="
        log_info "第 ${run_count} 次运行"
        log_info "=========================================="

        # 获取当前进度
        local current_chapter=$(get_current_chapter)
        log_info "当前进度：第 ${current_chapter}/1694 章"

        # 检查是否完成
        if [ $current_chapter -ge 1694 ]; then
            log_success "🎉 所有章节已处理完成！"
            log_success "总运行次数：${run_count}"
            break
        fi

        # 检查是否需要回顾
        if [ "$(needs_review)" = "yes" ]; then
            log_info "📝 需要进行回顾检查"
            generate_review_task $current_chapter
        else
            log_info "📖 继续处理下一章"
            generate_task $current_chapter
        fi

        # 运行 OpenCode
        run_opencode
        local result=$?

        # 处理结果
        if [ $result -eq 429 ]; then
            # 额度限制，等待后重试
            wait_for_quota
            continue
        elif [ $result -ne 0 ]; then
            # 其他错误，记录并继续
            log_error "本次运行出现错误，等待 30 秒后继续..."
            sleep 30
            continue
        fi

        # 成功，更新状态
        update_state "run_count" "$run_count"
        update_state "last_run_time" "\"$(date '+%Y-%m-%d %H:%M:%S')\""

        # 短暂休息，避免过于频繁
        log_info "等待 10 秒后继续下一个任务..."
        sleep 10
    done

    log_success "=========================================="
    log_success "  自动化运行结束"
    log_success "=========================================="
    log_info "总运行次数：${run_count}"
    log_info "查看日志：$LOG_DIR"
}

# 信号处理
trap 'log_warning "收到中断信号，正在安全退出..."; exit 0' INT TERM

# 启动
main "$@"
