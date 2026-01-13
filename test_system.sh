#!/bin/bash

###############################################
# 系统测试脚本
# 验证所有组件是否正常工作
###############################################

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🧪 开始系统测试...${NC}"
echo ""

# 测试 1: 检查必要文件
echo -e "${BLUE}测试 1: 检查必要文件${NC}"
files=(
    "START_AUTO.sh"
    "smart_task_generator.py"
    "novel/斗破苍穹.txt"
    "tools/progress.json"
    "task_learning.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✅ $file${NC}"
    else
        echo -e "${RED}  ❌ $file (不存在)${NC}"
    fi
done
echo ""

# 测试 2: 检查 Python 脚本
echo -e "${BLUE}测试 2: 检查 Python 脚本${NC}"
if python3 -c "import smart_task_generator" 2>/dev/null; then
    echo -e "${GREEN}  ✅ smart_task_generator.py 可以导入${NC}"
else
    echo -e "${RED}  ❌ smart_task_generator.py 导入失败${NC}"
fi
echo ""

# 测试 3: 生成测试任务
echo -e "${BLUE}测试 3: 生成测试任务${NC}"
if python3 smart_task_generator.py chapter 30 > /tmp/test_task.md 2>/dev/null; then
    echo -e "${GREEN}  ✅ 任务生成成功${NC}"
    echo -e "${BLUE}  📄 任务预览（前5行）：${NC}"
    head -n 5 /tmp/test_task.md | sed 's/^/      /'
else
    echo -e "${RED}  ❌ 任务生成失败${NC}"
fi
echo ""

# 测试 4: 检查 JSON 文件格式
echo -e "${BLUE}测试 4: 检查 JSON 文件格式${NC}"
json_files=(
    "tools/progress.json"
    "task_learning.json"
    "data/characters.json"
    "data/world_setting.json"
    "data/accumulated_context.json"
)

for file in "${json_files[@]}"; do
    if [ -f "$file" ]; then
        if python3 -c "import json; json.load(open('$file'))" 2>/dev/null; then
            echo -e "${GREEN}  ✅ $file (格式正确)${NC}"
        else
            echo -e "${RED}  ❌ $file (格式错误)${NC}"
        fi
    else
        echo -e "${YELLOW}  ⚠️  $file (不存在)${NC}"
    fi
done
echo ""

# 测试 5: 检查 Git 状态
echo -e "${BLUE}测试 5: 检查 Git 状态${NC}"
if git status &>/dev/null; then
    echo -e "${GREEN}  ✅ Git 仓库正常${NC}"
    current_branch=$(git branch --show-current)
    echo -e "${BLUE}  📍 当前分支: $current_branch${NC}"
else
    echo -e "${RED}  ❌ Git 仓库异常${NC}"
fi
echo ""

# 测试 6: 读取当前进度
echo -e "${BLUE}测试 6: 读取当前进度${NC}"
if [ -f "tools/progress.json" ]; then
    current_chapter=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['current_chapter'])")
    total_chapters=$(python3 -c "import json; print(json.load(open('tools/progress.json'))['total_chapters'])")
    percent=$(python3 -c "print(f'{$current_chapter/$total_chapters*100:.1f}')")

    echo -e "${GREEN}  ✅ 进度读取成功${NC}"
    echo -e "${BLUE}  📊 当前: 第 $current_chapter/$total_chapters 章 (${percent}%)${NC}"
else
    echo -e "${RED}  ❌ 无法读取进度${NC}"
fi
echo ""

# 测试 7: 检查日志目录
echo -e "${BLUE}测试 7: 检查日志目录${NC}"
if [ -d "logs" ]; then
    log_count=$(ls logs/*.log 2>/dev/null | wc -l)
    echo -e "${GREEN}  ✅ 日志目录存在${NC}"
    echo -e "${BLUE}  📝 已有日志: $log_count 个${NC}"
else
    echo -e "${YELLOW}  ⚠️  日志目录不存在（首次运行会创建）${NC}"
fi
echo ""

# 测试 8: 检查脚本权限
echo -e "${BLUE}测试 8: 检查脚本权限${NC}"
if [ -x "START_AUTO.sh" ]; then
    echo -e "${GREEN}  ✅ START_AUTO.sh 可执行${NC}"
else
    echo -e "${RED}  ❌ START_AUTO.sh 不可执行${NC}"
    echo -e "${YELLOW}  💡 运行: chmod +x START_AUTO.sh${NC}"
fi

if [ -x "smart_task_generator.py" ]; then
    echo -e "${GREEN}  ✅ smart_task_generator.py 可执行${NC}"
else
    echo -e "${RED}  ❌ smart_task_generator.py 不可执行${NC}"
    echo -e "${YELLOW}  💡 运行: chmod +x smart_task_generator.py${NC}"
fi
echo ""

# 总结
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ 系统测试完成！${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}💡 下一步：${NC}"
echo -e "  1. 查看状态: ${YELLOW}./START_AUTO.sh --status${NC}"
echo -e "  2. 开始运行: ${YELLOW}./START_AUTO.sh${NC}"
echo -e "  3. 查看文档: ${YELLOW}cat README_AUTO.md${NC}"
echo ""
