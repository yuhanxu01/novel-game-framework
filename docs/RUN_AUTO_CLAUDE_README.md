# 🤖 Claude Code 完全自动化运行指南

## 📖 简介

`RUN_AUTO_CLAUDE.sh` 是一个**完全自动化**的脚本，使用 **Claude Code CLI** 无需任何人工干预即可持续处理小说章节。

## ✨ 核心特性

### ✅ 100% 自动化
- 使用 Claude Code 官方 CLI
- 无需任何确认或输入
- 自动检测并恢复卡死情况
- 自动提交 Git
- 自动处理额度限制

### 🛡️ 智能保护
- **超时保护**：单次任务超过30分钟自动终止
- **进度监控**：实时检测处理进度
- **连续失败保护**：连续失败3次自动停止
- **详细日志**：所有操作详细记录

### 🔄 自动恢复
- 检测到 claude 卡死自动重启
- 触发额度限制自动等待5小时
- Mac 防休眠支持（caffeinate）

## 🚀 快速开始

### 1️⃣ 检查环境
```bash
# 确认 claude 命令已安装
which claude

# 如果未安装，执行：
npm install -g @anthropic-ai/claude-code
```

### 2️⃣ 查看状态
```bash
./START.sh status
```

### 3️⃣ 启动完全自动化
```bash
# 方法1：使用启动器（推荐）
./START.sh

# 方法2：直接运行
./RUN_AUTO_CLAUDE.sh

# 元任务模式 - 让 AI 改进系统
./RUN_AUTO_CLAUDE.sh --meta

# 只运行一次（不自动继续）
./RUN_AUTO_CLAUDE.sh --once
```

### 4️⃣ 放心离开
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

# 查看 claude 输出
tail -f logs/claude_output.log
```

### 进度查询
```bash
# 随时查看状态
./START.sh status

# 或直接查看进度文件
cat tools/progress.json

# 查看运行统计
cat auto_state.json
```

### 运行统计
状态文件 `auto_state.json` 记录：
- 总运行次数
- 成功完成次数
- 卡死恢复次数
- 额度限制次数

## ⚙️ 配置选项

编辑 `RUN_AUTO_CLAUDE.sh` 中的以下变量来自定义行为：

```bash
MAX_RUN_TIME=1800          # 单次最大运行时间（秒）
CHECK_INTERVAL=60          # 进度检查间隔（秒）
MAX_IDLE_TIME=600          # 最大空闲时间（秒）
```

## 🔧 故障排除

### 问题 1：找不到 claude 命令
```bash
# 安装 Claude Code CLI
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### 问题 2：权限被拒绝
脚本使用了 `--dangerously-skip-permissions` 标志，但如果你仍遇到权限问题：

```bash
# 手动测试 claude
echo "测试任务" | claude -p --permission-mode bypassPermissions
```

### 问题 3：频繁卡死
**可能原因**：
- 额度已用完
- 网络问题
- 章节内容异常

**解决方法**：
```bash
# 查看日志了解原因
cat logs/claude_output.log

# 检查是否有额度限制
grep -i "rate limit\|quota" logs/claude_output.log
```

### 问题 4：Git push 失败
```bash
# 检查远程仓库
git remote -v

# 手动测试 push
git push -u origin claude/automate-novel-writing-rwmkK
```

### 问题 5：恢复后无法继续
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
| `RUN_AUTO_CLAUDE.sh` | 主自动化脚本（Claude Code 版） |
| `START.sh` | 简单启动器 |
| `auto_state.json` | 运行状态统计 |
| `logs/auto_runner.log` | 主日志 |
| `logs/claude_output.log` | claude 输出日志 |
| `CURRENT_TASK.md` | 当前任务指令 |
| `CLAUDE_AUTO_INSTRUCTION.txt` | 自动化指令（临时） |

## 🆚 对比：不同版本

| 特性 | START_AUTO.sh | RUN_AUTO_CLAUDE.sh |
|------|---------------|-------------------|
| **CLI 工具** | opencode | Claude Code (claude) |
| **自动化程度** | 需要输入提示 | 100% 无需输入 |
| **权限模式** | 交互式 | bypassPermissions |
| **卡死检测** | ❌ 无 | ✅ 有 |
| **超时保护** | ❌ 无 | ✅ 30分钟 |
| **进度监控** | ❌ 无 | ✅ 实时监控 |
| **自动重启** | ❌ 无 | ✅ 有 |
| **详细统计** | ❌ 简单 | ✅ 完整 |
| **日志系统** | ❌ 无 | ✅ 完善 |

## 💡 最佳实践

### ✅ 推荐
1. **首次运行**：先用 `--once` 测试一次
   ```bash
   ./RUN_AUTO_CLAUDE.sh --once
   ```

2. **长期运行**：在 tmux 或 screen 中运行
   ```bash
   # 创建新会话
   tmux new -s novel

   # 启动脚本
   ./START.sh

   # 分离会话（按 Ctrl+B 然后 D）
   # 重新连接
   tmux attach -t novel
   ```

3. **定期检查**：每天查看一次日志
   ```bash
   tail -100 logs/auto_runner.log
   tail -100 logs/claude_output.log
   ```

4. **备份重要**：定期备份 `data/` 目录
   ```bash
   tar -czf backup_$(date +%Y%m%d).tar.gz data/
   ```

### ❌ 避免
1. ❌ 不要在运行时手动修改文件
2. ❌ 不要同时运行多个实例
3. ❌ 不要在额度限制时强行重启
4. ❌ 不要忽略错误日志

## 🎯 预期性能

- **单章处理时间**：1-5 分钟
- **每天处理量**：约 100-300 章（取决于额度）
- **总耗时估计**：约 6-17 天处理完全部 1694 章

## 🔍 Claude Code CLI 关键参数

脚本使用的 Claude Code 参数：

```bash
claude -p \
  --permission-mode bypassPermissions \
  --dangerously-skip-permissions \
  <指令文件
```

**参数说明**：
- `-p, --print`：非交互式输出模式
- `--permission-mode bypassPermissions`：绕过权限检查
- `--dangerously-skip-permissions`：完全跳过权限（用于信任目录）

## 📞 获取帮助

```bash
# 查看脚本帮助
./RUN_AUTO_CLAUDE.sh --help

# 查看 Claude Code 帮助
claude --help

# 查看 Claude Code 版本
claude --version
```

## 🔐 安全说明

脚本使用了 `--dangerously-skip-permissions` 标志，这意味着：
- ⚠️ Claude 可以执行任何工具而无需确认
- ⚠️ 仅在信任的目录中使用
- ⚠️ 确保你的代码库是安全的
- ✅ 脚本已经过测试，可以安全使用

如果你想更安全，可以编辑脚本移除该标志，但可能需要手动批准某些操作。

---

**享受完全自动化的快乐吧！** 🎉

使用 **Claude Code** 官方 CLI，更稳定、更可靠！
