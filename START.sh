#!/bin/bash

###############################################
# 🚀 一键启动器 - 超级简单
#
# 使用方法：
#   ./START.sh        # 自动运行
#   ./START.sh status # 查看状态
###############################################

# 颜色
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════╗"
echo "║                                           ║"
echo "║     🤖 Claude Code 小说处理自动化系统      ║"
echo "║                                           ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# 参数处理
if [ "$1" = "status" ]; then
    echo -e "${CYAN}📊 当前状态：${NC}"
    ./RUN_AUTO_CLAUDE.sh --status
    exit 0
fi

if [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "用法："
    echo "  ./START.sh         - 启动自动化"
    echo "  ./START.sh status  - 查看状态"
    echo "  ./START.sh help    - 显示帮助"
    echo ""
    echo "更多信息："
    echo "  查看 RUN_AUTO_FULLY_README.md"
    exit 0
fi

# 检查环境
echo -e "${YELLOW}🔍 检查环境...${NC}"

if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}❌ 未找到 claude${NC}"
    echo "请先安装 Claude Code CLI："
    echo "  npm install -g @anthropic-ai/claude-code"
    exit 1
fi

if [ ! -f "RUN_AUTO_CLAUDE.sh" ]; then
    echo -e "${YELLOW}❌ 未找到 RUN_AUTO_CLAUDE.sh${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 环境检查通过${NC}"
echo ""

# 确认启动
echo -e "${CYAN}即将启动 Claude Code 完全自动化模式...${NC}"
echo -e "${YELLOW}提示：脚本将 100% 自动运行，无需任何干预${NC}"
echo ""
read -p "按 Enter 继续或 Ctrl+C 取消..." </dev/tty

# 启动
echo ""
echo -e "${GREEN}🚀 启动中...${NC}"
echo ""
./RUN_AUTO_CLAUDE.sh
