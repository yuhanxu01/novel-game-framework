#!/bin/bash
################################################################################
# 一键启动自动小说处理系统
################################################################################
#
# 这个脚本会自动处理整个小说，包括：
# ✅ 逐章阅读和分析（不跳过任何步骤）
# ✅ 每10章自动回顾检查
# ✅ 自动批准并继续
# ✅ 完整处理整个小说
#
################################################################################

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                   自动小说处理系统启动器                            ║"
echo "║                    Auto Novel Writer Launcher                     ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 默认配置
NOVEL_PATH="novel/斗破苍穹.txt"
PROJECT_NAME="斗破苍穹游戏"
API_PROVIDER="deepseek"
REVIEW_INTERVAL=10
AUTO_APPROVE=true  # 设置为true启用完全自动模式

# 检查API Key
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  未检测到环境变量 DEEPSEEK_API_KEY${NC}"
    echo -e "请设置API Key："
    echo -e "   export DEEPSEEK_API_KEY='your-api-key-here'"
    echo -e ""
    echo -e "或者直接在命令中提供："
    echo -e "   ./start_auto_writer.sh --api-key your-api-key-here"
    echo -e ""
    read -p "现在输入API Key (留空退出): " input_key
    if [ -z "$input_key" ]; then
        echo -e "${RED}❌ 未提供API Key，退出${NC}"
        exit 1
    fi
    export DEEPSEEK_API_KEY="$input_key"
fi

echo -e "${GREEN}✅ API Key已配置${NC}"
echo ""

# 检查小说文件是否存在
if [ ! -f "$NOVEL_PATH" ]; then
    echo -e "${RED}❌ 小说文件不存在: $NOVEL_PATH${NC}"
    echo -e "请确保小说文件在正确的位置"
    exit 1
fi

echo -e "${GREEN}✅ 找到小说文件: $NOVEL_PATH${NC}"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python环境检查通过${NC}"
echo ""

# 显示配置信息
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 当前配置${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "📚 小说文件: ${GREEN}$NOVEL_PATH${NC}"
echo -e "📦 项目名称: ${GREEN}$PROJECT_NAME${NC}"
echo -e "🤖 AI提供商: ${GREEN}$API_PROVIDER${NC}"
echo -e "📊 回顾间隔: ${GREEN}每 $REVIEW_INTERVAL 章${NC}"
echo -e "✅ 自动批准: ${GREEN}$([ "$AUTO_APPROVE" = true ] && echo "是（完全自动）" || echo "否（需人工确认）")${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 询问是否继续
if [ "$AUTO_APPROVE" != true ]; then
    read -p "按 Enter 开始处理，或输入 'q' 退出: " confirm
    if [ "$confirm" = "q" ]; then
        echo -e "${YELLOW}用户取消操作${NC}"
        exit 0
    fi
fi

echo ""
echo -e "${GREEN}🚀 启动自动处理系统...${NC}"
echo ""

# 构建命令
CMD="python3 auto_novel_writer.py \
    --novel \"$NOVEL_PATH\" \
    --name \"$PROJECT_NAME\" \
    --api_key \"$DEEPSEEK_API_KEY\" \
    --provider \"$API_PROVIDER\" \
    --review-interval $REVIEW_INTERVAL"

# 如果启用自动批准
if [ "$AUTO_APPROVE" = true ]; then
    CMD="$CMD --auto-approve"
fi

# 检查是否要恢复之前的进度
if [ -f "tools/progress.json" ]; then
    echo -e "${YELLOW}📂 检测到之前的进度文件${NC}"
    cat tools/progress.json
    echo ""
    if [ "$AUTO_APPROVE" = true ]; then
        echo -e "${GREEN}自动模式：将从上次进度继续${NC}"
        use_resume="y"
    else
        read -p "是否从上次进度继续? (y/n): " use_resume
    fi

    if [ "$use_resume" = "y" ]; then
        CMD="$CMD --resume"
        echo -e "${GREEN}✅ 将从上次进度继续${NC}"
    fi
fi

echo ""
echo -e "${BLUE}执行命令:${NC}"
echo -e "${GREEN}$CMD${NC}"
echo ""

# 创建日志目录
mkdir -p logs

# 生成日志文件名
LOG_FILE="logs/auto_writer_$(date +%Y%m%d_%H%M%S).log"

echo -e "${BLUE}📝 日志文件: $LOG_FILE${NC}"
echo ""

# 执行命令并记录日志
eval $CMD 2>&1 | tee "$LOG_FILE"

# 检查执行结果
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                          ✅ 执行完成                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "📝 日志已保存到: ${GREEN}$LOG_FILE${NC}"
else
    echo ""
    echo -e "${RED}"
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                          ❌ 执行失败                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "📝 错误日志: ${RED}$LOG_FILE${NC}"
    echo -e "💾 进度已保存，可使用 --resume 参数继续"
fi
