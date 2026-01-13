#!/bin/bash

# 实时监控脚本
echo "🔍 实时监控 Claude Code 自动化"
echo "================================"
echo ""

while true; do
    clear
    echo "📊 当前状态："
    echo "================================"
    date
    echo ""

    # 检查进程
    if ps -p 56518 > /dev/null 2>&1; then
        echo "✅ Claude 进程运行中 (PID: 56518)"
        ps -p 56518 -o pid,time,%cpu,command
    else
        echo "⏹️ Claude 进程已结束"
        echo ""
        echo "查看结果..."
        break
    fi

    echo ""
    echo "📁 最近修改的文件："
    ls -lt data/chapter_summaries/ | head -3

    echo ""
    echo "📝 当前进度："
    cat tools/progress.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"第 {d['current_chapter']} 章\")" 2>/dev/null || echo "无法读取"

    echo ""
    echo "📋 最新日志（最后10行）："
    if [ -s logs/claude_output.log ]; then
        tail -10 logs/claude_output.log
    else
        echo "⏳ 等待日志输出..."
    fi

    echo ""
    echo "按 Ctrl+C 退出监控..."
    sleep 5
done

echo ""
echo "================================"
echo "最终状态："
cat logs/auto_runner.log | tail -20
