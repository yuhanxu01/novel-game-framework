#!/usr/bin/env python3
"""
智能任务生成器
- 根据进度生成详细任务
- 学习历史错误，改进提示词
- 允许 Claude Code 参与完善脚本
"""

import json
import os
from datetime import datetime
from pathlib import Path

class SmartTaskGenerator:
    def __init__(self, project_dir=None):
        if project_dir is None:
            self.project_dir = Path(__file__).resolve().parent
        else:
            self.project_dir = Path(project_dir)
            
        self.progress_file = self.project_dir / "tools" / "progress.json"
        self.learning_file = self.project_dir / "task_learning.json"
        self.prompts_dir = self.project_dir / "prompts"

        self.load_learning()

    def load_learning(self):
        """加载学习到的改进"""
        if self.learning_file.exists():
            with open(self.learning_file, 'r', encoding='utf-8') as f:
                self.learning = json.load(f)
        else:
            self.learning = {
                "common_errors": [],
                "successful_patterns": [],
                "prompt_improvements": [],
                "script_improvements": [],
                "best_practices": [
                    "完整阅读章节内容，不要跳过",
                    "保持 JSON 格式正确",
                    "及时提交 Git",
                    "详细的 commit message"
                ]
            }

    def save_learning(self):
        """保存学习结果"""
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(self.learning, f, indent=2, ensure_ascii=False)

    def get_progress(self):
        """获取当前进度"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"current_chapter": 30, "total_chapters": 1694}

    def generate_meta_task(self):
        """生成元任务：让 Claude Code 改进系统本身"""
        task = f"""# 🔧 元任务：系统改进与学习

## 🎯 目标
作为一个自我完善的系统，你现在的任务是：
1. 回顾之前的工作日志
2. 识别可以改进的地方
3. 更新脚本和提示词
4. 记录最佳实践

## 📋 任务步骤

### 1️⃣ 回顾最近的日志
读取最近的会话日志：
- 查看 `logs/` 目录
- 分析成功的模式
- 识别重复出现的错误

### 2️⃣ 改进提示词
如果发现提示词可以更清晰或更有效：
- 读取 `prompts/` 目录下的提示词文件
- 使用 Edit 工具修改提示词
- 添加更明确的指令或示例

### 3️⃣ 改进脚本
如果发现脚本有 bug 或可以优化：
- 读取 `AUTO_RUNNER.sh` 或 `smart_task_generator.py`
- 修复问题或添加新功能
- 更新注释和文档

### 4️⃣ 记录学习成果
更新 `task_learning.json`：
```json
{{
    "common_errors": ["错误描述"],
    "successful_patterns": ["成功模式"],
    "prompt_improvements": ["改进建议"],
    "script_improvements": ["脚本改进"],
    "best_practices": ["最佳实践"]
}}
```

### 5️⃣ 生成改进报告
创建 `logs/improvement_report_{{timestamp}}.md`：
- 本次发现的问题
- 实施的改进
- 预期效果
- 建议的下一步优化

## ⚠️ 指导原则

{self._get_best_practices()}

## 🤖 你的权限
你完全有权限：
- 修改任何脚本文件
- 更新提示词
- 重构代码结构
- 添加新功能
- 优化工作流程

**不要犹豫，大胆改进！**

## 🔄 完成标志
- ✅ 日志已回顾
- ✅ 改进已实施
- ✅ 学习已记录
- ✅ 报告已生成
- ✅ Git 已提交

---
**系统版本**: {self._get_system_version()}
**学习记录**: {len(self.learning.get('prompt_improvements', []))} 条改进
"""
        return task

    def generate_chapter_task(self, chapter_num):
        """生成章节处理任务"""
        next_chapter = chapter_num + 1
        review_checkpoint = ((chapter_num // 10) + 1) * 10

        task = f"""# 📖 章节处理任务 - 第 {next_chapter} 章

## 🎯 目标
处理《斗破苍穹》第 **{next_chapter}** 章

## 📋 详细步骤

### 1️⃣ 读取原文
```bash
# 使用 Read 工具读取小说文件
Read novel/斗破苍穹.txt
```

**定位方法**：
- 搜索"第{next_chapter}章"或"第{self._number_to_chinese(next_chapter)}章"
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

**保存到**：`data/chapter_summaries/chapter_{next_chapter}.json`

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
# 更新 current_chapter 为 {next_chapter}
# 如果 current_chapter == {review_checkpoint}，设置 needs_review = true
```

### 8️⃣ Git 提交
```bash
git add -A
git commit -m "处理第{next_chapter}章：[从原文提取的章节标题]

- 完成章节分析
- 发现新角色/物品 X 个
- 更新世界观设定
- 游戏内容转换（如适用）

Progress: {next_chapter}/1694 ({(next_chapter/1694*100):.1f}%)"

git push -u origin claude/automate-novel-writing-rwmkK
```

## ⚠️ 质量标准

{self._get_quality_standards()}

## 🎯 成功标志
当你完成以下所有项，任务即完成：
- ✅ 原文已完整阅读（能准确复述情节）
- ✅ chapter_{next_chapter}.json 已创建且内容详实
- ✅ accumulated_context.json 已更新
- ✅ 新角色已添加到 characters.json（如有）
- ✅ 新设定已添加到 world_setting.json（如有）
- ✅ progress.json 的 current_chapter = {next_chapter}
- ✅ Git commit 成功，push 成功

## 💡 历史经验

{self._get_historical_insights()}

---
**当前进度**: {chapter_num}/{1694} ({(chapter_num/1694*100):.1f}%)
**下一个检查点**: 第 {review_checkpoint} 章
**预计剩余**: {1694-chapter_num} 章
"""
        return task

    def generate_review_task(self, current_chapter):
        """生成回顾任务"""
        review_num = current_chapter // 10
        start_chapter = (review_num - 1) * 10 + 1
        end_chapter = current_chapter

        task = f"""# 🔍 回顾检查任务 - 第 {review_num} 次

## 🎯 回顾范围
第 **{start_chapter}-{end_chapter}** 章（共 {end_chapter - start_chapter + 1} 章）

## 📋 检查步骤

### 1️⃣ 读取所有章节分析
```python
# 批量读取
for i in range({start_chapter}, {end_chapter + 1}):
    Read data/chapter_summaries/chapter_{{i}}.json
```

### 2️⃣ 统计数据
创建统计表：
```markdown
| 章节 | 标题 | 新角色 | 新地点 | 新物品 | 核心事件 |
|------|------|--------|--------|--------|----------|
| {start_chapter} | ... | X | Y | Z | ... |
| ... | ... | ... | ... | ... | ... |
| {end_chapter} | ... | X | Y | Z | ... |
```

### 3️⃣ 质量检查

#### 完整性检查
- ✅ 每章是否都有分析文件？
- ✅ 每个必填字段都有内容？
- ✅ 描述是否足够详细（>100字）？

#### 一致性检查
- ✅ 角色名字拼写是否统一？
- ✅ 地点描述是否前后一致？
- ✅ 时间线是否合理？
- ✅ 世界观设定是否矛盾？

#### 准确性检查
- ✅ 剧情是否忠实原著？
- ✅ 角色性格是否符合设定？
- ✅ 有无明显理解错误？

### 4️⃣ 生成回顾报告
创建：`data/reviews/review_{review_num}.md`

**报告结构**：
```markdown
# 第 {review_num} 次回顾报告

## 📊 统计数据
- 章节范围：第 {start_chapter}-{end_chapter} 章
- 新增角色：X 个
- 新增地点：Y 个
- 新增物品：Z 个
- 核心事件：W 个

## 📝 章节概览
[每章一句话总结]

## ✅ 质量评估
- 完整性：XX%
- 一致性：良好/一般/需改进
- 准确性：良好/一般/需改进

## 🔍 发现的问题
[列出问题，如有]

## 💡 改进建议
[提出建议，如有]

## 🎯 审核结果
状态：通过/需修正
批准：自动批准/人工审核
```

### 5️⃣ 更新进度
```python
Read tools/progress.json
# 设置 needs_review = false
# 设置 last_review_chapter = {end_chapter}
# 设置 last_review_date = "当前日期"
```

### 6️⃣ Git 提交
```bash
git add -A
git commit -m "完成第{review_num}次回顾（第{start_chapter}-{end_chapter}章）

统计：
- 处理章节：{end_chapter - start_chapter + 1}章
- 质量评估：[评估结果]
- 状态：[通过/需修正]

累计进度：{end_chapter}/1694 ({(end_chapter/1694*100):.1f}%)"

git push -u origin claude/automate-novel-writing-rwmkK
```

## 🎯 自动批准标准
如果满足以下条件，可以自动批准：
- ✅ 完整性 ≥ 95%
- ✅ 一致性良好
- ✅ 准确性良好
- ✅ 无重大错误

否则，标记为"需人工审核"并详细说明问题。

---
**回顾编号**: {review_num}
**章节数**: {end_chapter - start_chapter + 1}
**累计进度**: {(end_chapter/1694*100):.1f}%
"""
        return task

    def _get_best_practices(self):
        """获取最佳实践"""
        practices = self.learning.get("best_practices", [])
        if practices:
            return "\n".join([f"- ✅ {p}" for p in practices])
        return "- ✅ 暂无最佳实践记录"

    def _get_quality_standards(self):
        """获取质量标准"""
        return """
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
"""

    def _get_historical_insights(self):
        """获取历史经验"""
        insights = []

        errors = self.learning.get("common_errors", [])
        if errors:
            insights.append("**常见错误（避免重复）**：")
            for err in errors[:3]:
                insights.append(f"- ⚠️ {err}")

        patterns = self.learning.get("successful_patterns", [])
        if patterns:
            insights.append("\n**成功模式（推荐使用）**：")
            for pat in patterns[:3]:
                insights.append(f"- ✅ {pat}")

        if not insights:
            return "- 💡 这是早期任务，还没有历史经验记录"

        return "\n".join(insights)

    def _get_system_version(self):
        """获取系统版本"""
        return "2.0.0-smart"

    def _number_to_chinese(self, num):
        """阿拉伯数字转中文"""
        chinese_nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        if num < 10:
            return chinese_nums[num]
        elif num < 20:
            return '十' + (chinese_nums[num - 10] if num > 10 else '')
        else:
            tens = num // 10
            ones = num % 10
            return chinese_nums[tens] + '十' + (chinese_nums[ones] if ones > 0 else '')

    def record_error(self, error_msg):
        """记录错误"""
        if error_msg not in self.learning["common_errors"]:
            self.learning["common_errors"].append(error_msg)
            self.save_learning()

    def record_success(self, pattern):
        """记录成功模式"""
        if pattern not in self.learning["successful_patterns"]:
            self.learning["successful_patterns"].append(pattern)
            self.save_learning()

    def suggest_improvement(self, suggestion):
        """记录改进建议"""
        self.learning["script_improvements"].append({
            "timestamp": datetime.now().isoformat(),
            "suggestion": suggestion
        })
        self.save_learning()

def main():
    """命令行接口"""
    import sys

    generator = SmartTaskGenerator()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "meta":
            print(generator.generate_meta_task())
        elif command == "chapter":
            chapter = int(sys.argv[2]) if len(sys.argv) > 2 else generator.get_progress()['current_chapter']
            print(generator.generate_chapter_task(chapter))
        elif command == "review":
            chapter = int(sys.argv[2]) if len(sys.argv) > 2 else generator.get_progress()['current_chapter']
            print(generator.generate_review_task(chapter))
        else:
            print("未知命令")
    else:
        # 默认：根据进度生成任务
        progress = generator.get_progress()
        current = progress['current_chapter']

        if progress.get('needs_review', False):
            print(generator.generate_review_task(current))
        else:
            print(generator.generate_chapter_task(current))

if __name__ == "__main__":
    main()
