# 📖 章节处理任务 - 第 42 章

## 🎯 目标
处理《斗破苍穹》第 **42** 章

## 📋 详细步骤

### 1️⃣ 读取原文
```bash
# 使用 Read 工具读取小说文件
Read novel/斗破苍穹.txt
```

**定位方法**：
- 搜索"第42章"或"第四十二章"
- 记录起始行号和结束行号
- **完整阅读**章节内容（约50-100行）

### 2️⃣ 深度分析
使用 `prompts/01-小说分析器.md` 模板分析：

**必须包含**：
- ✅ 章节标题
- ✅ 核心事件（2-3句话）
- ✅ 详细描述（5-10句话）
- ✅ 新发现（角色/地点/设定/物品）
- ✅ 角色动态
- ✅ 剧情分析（因果链、伏笔、冲突）
- ✅ 游戏化潜力

**保存到**：`data/chapter_summaries/chapter_42.json`

### 3️⃣ 更新累积上下文
```python
# 读取现有数据
Read data/accumulated_context.json

# 使用 Edit 工具更新
# 添加：新角色、新地点、新物品、新世界观
# 更新：前文摘要（最近3-5章的一句话总结）
```

### 4️⃣ 更新角色库
**如果有新角色**：
```python
Read data/characters.json
# 使用 prompts/03-角色分析器.md 模板
# 添加新角色的完整档案
```

### 5️⃣ 更新世界观
**如果有新设定**：
```python
Read data/world_setting.json
# 添加新的世界观元素
# 保持分类清晰（力量体系/功法/地理/社会）
```

### 6️⃣ 游戏内容转换（可选）
**如果本章有重要剧情**，考虑添加到游戏：
```python
Read frontend/data/game_data_doupo.json
# 创建新的 chapter 对象
# 设计 3-5 个选择点
# 每个选择有 2-4 个选项
# 设置合理的 effects（属性/关系/物品）
```

### 7️⃣ 更新进度
```python
Read tools/progress.json
# 更新 current_chapter 为 42
# 如果 current_chapter == 50，设置 needs_review = true
```

### 8️⃣ Git 提交
```bash
git add -A
git commit -m "处理第42章：[从原文提取的章节标题]

- 完成章节分析
- 发现新角色/物品 X 个
- 更新世界观设定
- 游戏内容转换（如适用）

Progress: 42/1694 (2.5%)"

git push -u origin claude/automate-novel-writing-rwmkK
```

## ⚠️ 质量标准


**必须满足**：
1. **完整性**：所有字段都有内容，没有空值或 TODO
2. **准确性**：忠实于原著，没有臆造情节
3. **详细性**：描述具体生动，不是简单罗列
4. **结构性**：JSON 格式正确，易于解析
5. **可用性**：数据可以直接用于游戏生成

**禁止**：
- ❌ 跳过阅读原文
- ❌ 敷衍了事的分析
- ❌ 不更新进度文件
- ❌ 不提交 Git
- ❌ JSON 格式错误


## 🎯 成功标志
当你完成以下所有项，任务即完成：
- ✅ 原文已完整阅读（能准确复述情节）
- ✅ chapter_42.json 已创建且内容详实
- ✅ accumulated_context.json 已更新
- ✅ 新角色已添加到 characters.json（如有）
- ✅ 新设定已添加到 world_setting.json（如有）
- ✅ progress.json 的 current_chapter = 42
- ✅ Git commit 成功，push 成功

## 💡 历史经验

**常见错误（避免重复）**：
- ⚠️ 忘记更新 progress.json 导致重复处理
- ⚠️ JSON 格式错误（中文标点符号）
- ⚠️ 跳过阅读原文导致分析不准确

**成功模式（推荐使用）**：
- ✅ 先完整阅读章节，再进行分析
- ✅ 每次更新都 git commit，保持小步提交
- ✅ 使用 Read 工具完整读取文件，不猜测内容

---
**当前进度**: 41/1694 (2.4%)
**下一个检查点**: 第 50 章
**预计剩余**: 1653 章

