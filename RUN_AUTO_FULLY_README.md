# 🤖 完全自动化运行指南

## 📖 简介

`RUN_AUTO_FULLY.sh` 是一个**完全自动化**的脚本，无需任何人工干预即可持续处理小说章节。

## ✨ 核心特性

### ✅ 100% 自动化
- 无需任何确认或输入
- 自动检测并恢复卡死情况
- 自动提交 Git
- 自动处理额度限制

### 🛡️ 智能保护
- **超时保护**：单次任务超过30分钟自动终止
- **进度监控**：实时检测处理进度
- **连续失败保护**：连续失败3次自动停止
- **日志记录**：所有操作详细记录

### 🔄 自动恢复
- 检测到 opencode 卡死自动重启
- 触发额度限制自动等待5小时
- Mac 防休眠支持（caffeinate）

## 🚀 快速开始

### 1️⃣ 查看状态
```bash
./RUN_AUTO_FULLY.sh --status
```

### 2️⃣ 启动完全自动化
```bash
# 正常模式 - 处理小说章节
./RUN_AUTO_FULLY.sh

# 元任务模式 - 让 AI 改进系统
./RUN_AUTO_FULLY.sh --meta

# 只运行一次（不自动继续）
./RUN_AUTO_FULLY.sh --once
```

### 3️⃣ 放心离开
脚本会自动：
- ✅ 读取小说章节
- ✅ 深度分析内容
- ✅ 更新所有数据文件
- ✅ 提交到 Git
- ✅ 检测卡死并重启
- ✅ 等待额度恢复
- ✅ 继续下一章

你可以：
- ☕ 去喝咖啡
- 🛌 去睡觉
- 🎮 去玩游戏
- 📱 去做其他事

## 📊 监控运行状态

### 实时日志
```bash
# 查看主日志
tail -f logs/auto_runner.log

# 查看 opencode 输出
tail -f logs/opencode_output.log
```

### 进度查询
```bash
# 随时查看状态
./RUN_AUTO_FULLY.sh --status

# 或直接查看进度文件
cat tools/progress.json
```

### 运行统计
状态文件 `auto_state.json` 记录：
- 总运行次数
- 成功完成次数
- 卡死恢复次数
- 额度限制次数

## ⚙️ 配置选项

编辑脚本中的以下变量来自定义行为：

```bash
MAX_RUN_TIME=1800          # 单次最大运行时间（秒）
CHECK_INTERVAL=60          # 进度检查间隔（秒）
MAX_IDLE_TIME=600          # 最大空闲时间（秒）
```

## 🔧 故障排除

### 问题 1：脚本无法启动
```bash
# 添加执行权限
chmod +x RUN_AUTO_FULLY.sh

# 检查 opencode 是否安装
which opencode
```

### 问题 2：频繁卡死
**可能原因**：
- 额度已用完
- 网络问题
- 章节内容异常

**解决方法**：
```bash
# 查看日志了解原因
cat logs/opencode_output.log

# 手动测试 opencode
echo "测试" | opencode
```

### 问题 3：Git push 失败
```bash
# 检查远程仓库
git remote -v

# 手动测试 push
git push -u origin claude/automate-novel-writing-rwmkK
```

### 问题 4：恢复后无法继续
```bash
# 检查进度文件
cat tools/progress.json

# 手动更新进度（如需要）
python3 << 'EOF'
import json
with open('tools/progress.json', 'r') as f:
    data = json.load(f)
data['current_chapter'] = 31  # 设置为正确的章节
with open('tools/progress.json', 'w') as f:
    json.dump(data, f, indent=2)
EOF
```

## 📂 文件说明

| 文件 | 说明 |
|------|------|
| `RUN_AUTO_FULLY.sh` | 主自动化脚本 |
| `auto_state.json` | 运行状态统计 |
| `logs/auto_runner.log` | 主日志 |
| `logs/opencode_output.log` | opencode 输出日志 |
| `CURRENT_TASK.md` | 当前任务指令 |
| `AUTO_INSTRUCTION.txt` | 自动化指令（临时） |

## 🆚 对比：旧版 vs 新版

| 特性 | START_AUTO.sh | RUN_AUTO_FULLY.sh |
|------|---------------|-------------------|
| 自动化程度 | 需要输入提示 | 100% 无需输入 |
| 卡死检测 | ❌ 无 | ✅ 有 |
| 超时保护 | ❌ 无 | ✅ 30分钟 |
| 进度监控 | ❌ 无 | ✅ 实时监控 |
| 自动重启 | ❌ 无 | ✅ 有 |
| 详细统计 | ❌ 简单 | ✅ 完整 |
| 日志系统 | ❌ 无 | ✅ 完善 |

## 💡 最佳实践

### ✅ 推荐
1. **首次运行**：先用 `--once` 测试一次
2. **长期运行**：在 tmux 或 screen 中运行
3. **定期检查**：每天查看一次日志
4. **备份重要**：定期备份 `data/` 目录

### ❌ 避免
1. ❌ 不要在运行时手动修改文件
2. ❌ 不要同时运行多个实例
3. ❌ 不要在额度限制时强行重启
4. ❌ 不要忽略错误日志

## 🎯 预期性能

- **单章处理时间**：1-5 分钟
- **每天处理量**：约 100-300 章（取决于额度）
- **总耗时估计**：约 6-17 天处理完全部 1694 章

## 📞 获取帮助

```bash
# 查看帮助信息
./RUN_AUTO_FULLY.sh --help
```

---

**享受完全自动化的快乐吧！** 🎉
