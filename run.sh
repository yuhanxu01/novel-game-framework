#!/bin/bash

###############################################
# 斗破苍穹游戏 - 快捷启动脚本
#
# 功能：
# - 🎮 启动游戏服务器
# - 🤖 运行Claude自动化
# - 📊 查看项目状态
# - 🧪 运行测试
###############################################

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 打印banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║        🎮 斗破苍穹：萧炎的逆袭 v2.0.0                    ║"
    echo "║                                                          ║"
    echo "║        ⚡ 三十年河东，三十年河西，莫欺少年穷！⚡        ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 显示主菜单
show_menu() {
    echo -e "${YELLOW}请选择操作：${NC}"
    echo ""
    echo "  1) 🎮 启动游戏（推荐）"
    echo "  2) 🤖 运行Claude自动生成内容"
    echo "  3) 📊 查看项目状态"
    echo "  4) 🧪 运行测试"
    echo "  5) 📖 查看文档"
    echo "  6) 🔧 开发者工具"
    echo "  0) 退出"
    echo ""
    echo -n "输入选项 [1-6]: "
}

# 启动游戏
start_game() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎮 启动游戏服务器${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 检查是否有Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ 找不到 python3，请先安装 Python 3${NC}"
        exit 1
    fi

    echo -e "${CYAN}启动HTTP服务器...${NC}"
    echo -e "${CYAN}访问地址: ${GREEN}http://localhost:8001${NC}"
    echo ""
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    echo ""

    cd frontend
    python3 -m http.server 8001
}

# 运行Claude自动化
run_claude_auto() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🤖 Claude自动化系统${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "${YELLOW}选择模式：${NC}"
    echo "  1) 正常模式 - 自动生成游戏内容"
    echo "  2) 查看状态"
    echo "  3) 返回主菜单"
    echo ""
    echo -n "输入选项 [1-3]: "

    read claude_choice

    case $claude_choice in
        1)
            echo ""
            echo -e "${CYAN}启动Claude自动化...${NC}"
            ./scripts/RUN_AUTO_CLAUDE.sh
            ;;
        2)
            echo ""
            ./scripts/RUN_AUTO_CLAUDE.sh --status
            echo ""
            read -p "按Enter继续..."
            ;;
        3)
            return
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            return
            ;;
    esac
}

# 查看项目状态
show_status() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📊 项目状态${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Git状态
    echo -e "${CYAN}Git 状态：${NC}"
    git status --short | head -10
    echo ""

    # 文件统计
    echo -e "${CYAN}文件统计：${NC}"
    echo -n "  章节数据: "
    ls data/chapters/*.json 2>/dev/null | wc -l
    echo -n "  支线任务: "
    python3 -c "import json; data=json.load(open('data/side_quests.json')); print(len(data['side_quests']))" 2>/dev/null || echo "N/A"
    echo -n "  随机事件: "
    python3 -c "import json; data=json.load(open('data/random_events.json')); print(len(data['random_events']))" 2>/dev/null || echo "N/A"
    echo ""

    # 代码统计
    echo -e "${CYAN}代码统计：${NC}"
    echo -n "  JavaScript: "
    find frontend/static/js -name "*.js" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1 " 行"}'
    echo -n "  Python: "
    find scripts -name "*.py" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1 " 行"}'
    echo ""

    read -p "按Enter继续..."
}

# 运行测试
run_tests() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🧪 运行测试${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # 检查数据文件完整性
    echo -e "${CYAN}检查数据文件...${NC}"

    files=(
        "data/story_routes.json"
        "data/side_quests.json"
        "data/random_events.json"
        "data/battle_system.json"
    )

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
                echo -e "  ✅ $file"
            else
                echo -e "  ❌ $file (JSON格式错误)"
            fi
        else
            echo -e "  ⚠️  $file (文件不存在)"
        fi
    done

    echo ""

    # 检查前端文件
    echo -e "${CYAN}检查前端文件...${NC}"

    frontend_files=(
        "frontend/index.html"
        "frontend/static/js/engine/battle.js"
        "frontend/static/js/engine/quest.js"
        "frontend/static/js/engine/random_events.js"
        "frontend/static/js/engine/route.js"
    )

    for file in "${frontend_files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "  ✅ $file"
        else
            echo -e "  ❌ $file (文件不存在)"
        fi
    done

    echo ""
    read -p "按Enter继续..."
}

# 查看文档
show_docs() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}📖 查看文档${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "${YELLOW}可用文档：${NC}"
    echo ""
    echo "  1) README.md - 项目主文档"
    echo "  2) GAME_EVALUATION_REPORT.md - 游戏评估报告"
    echo "  3) GAME_UPDATE_SUMMARY.md - v2.0.0更新总结"
    echo "  4) GAME_EXPERIENCE_GUIDE.md - 体验优化指南"
    echo "  5) GAME_SYSTEMS_GUIDE.md - 游戏系统完整指南"
    echo "  6) 返回主菜单"
    echo ""
    echo -n "输入选项 [1-6]: "

    read doc_choice

    case $doc_choice in
        1)
            less README.md 2>/dev/null || cat README.md
            ;;
        2)
            less docs/GAME_EVALUATION_REPORT.md 2>/dev/null || cat docs/GAME_EVALUATION_REPORT.md
            ;;
        3)
            less docs/GAME_UPDATE_SUMMARY.md 2>/dev/null || cat docs/GAME_UPDATE_SUMMARY.md
            ;;
        4)
            less docs/GAME_EXPERIENCE_GUIDE.md 2>/dev/null || cat docs/GAME_EXPERIENCE_GUIDE.md
            ;;
        5)
            less agent_instructions/GAME_SYSTEMS_GUIDE.md 2>/dev/null || cat agent_instructions/GAME_SYSTEMS_GUIDE.md
            ;;
        6)
            return
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            ;;
    esac

    echo ""
    read -p "按Enter继续..."
}

# 开发者工具
dev_tools() {
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🔧 开发者工具${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "${YELLOW}可用工具：${NC}"
    echo ""
    echo "  1) 生成斗破苍穹游戏数据"
    echo "  2) 完善游戏内容"
    echo "  3) 验证JSON文件格式"
    echo "  4) 清理日志文件"
    echo "  5) 返回主菜单"
    echo ""
    echo -n "输入选项 [1-5]: "

    read dev_choice

    case $dev_choice in
        1)
            echo ""
            echo -e "${CYAN}生成游戏数据...${NC}"
            python3 scripts/generate_doupo_game.py
            echo ""
            echo -e "${GREEN}✅ 完成${NC}"
            read -p "按Enter继续..."
            ;;
        2)
            echo ""
            echo -e "${CYAN}完善游戏内容...${NC}"
            python3 scripts/complete_doupo_game.py
            echo ""
            echo -e "${GREEN}✅ 完成${NC}"
            read -p "按Enter继续..."
            ;;
        3)
            echo ""
            echo -e "${CYAN}验证JSON文件...${NC}"
            for file in data/*.json data/chapters/*.json frontend/data/*.json; do
                if [ -f "$file" ]; then
                    if python3 -m json.tool "$file" > /dev/null 2>&1; then
                        echo -e "  ✅ $file"
                    else
                        echo -e "  ❌ $file (格式错误)"
                    fi
                fi
            done
            echo ""
            read -p "按Enter继续..."
            ;;
        4)
            echo ""
            echo -e "${CYAN}清理日志文件...${NC}"
            rm -rf logs/history/*
            rm -f logs/*.log
            echo -e "${GREEN}✅ 日志已清理${NC}"
            echo ""
            read -p "按Enter继续..."
            ;;
        5)
            return
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            ;;
    esac
}

# 主循环
main() {
    # 显示banner
    print_banner

    while true; do
        show_menu
        read choice

        case $choice in
            1)
                start_game
                ;;
            2)
                run_claude_auto
                ;;
            3)
                show_status
                ;;
            4)
                run_tests
                ;;
            5)
                show_docs
                ;;
            6)
                dev_tools
                ;;
            0)
                echo ""
                echo -e "${GREEN}感谢使用！再见！${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新输入${NC}"
                sleep 1
                ;;
        esac

        # 清屏（可选）
        # clear
        echo ""
    done
}

# 检查是否有参数
if [ $# -gt 0 ]; then
    case $1 in
        game|play)
            print_banner
            start_game
            ;;
        auto|claude)
            print_banner
            run_claude_auto
            ;;
        status)
            print_banner
            show_status
            ;;
        test)
            print_banner
            run_tests
            ;;
        docs)
            print_banner
            show_docs
            ;;
        dev)
            print_banner
            dev_tools
            ;;
        --help|-h)
            print_banner
            echo "用法: $0 [命令]"
            echo ""
            echo "命令:"
            echo "  game, play    - 启动游戏"
            echo "  auto, claude  - 运行Claude自动化"
            echo "  status        - 查看项目状态"
            echo "  test          - 运行测试"
            echo "  docs          - 查看文档"
            echo "  dev           - 开发者工具"
            echo "  (无参数)      - 显示交互菜单"
            echo ""
            exit 0
            ;;
        *)
            echo "未知命令: $1"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
else
    # 交互模式
    main
fi
