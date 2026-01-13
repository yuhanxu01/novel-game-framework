#!/usr/bin/env python3
"""
Agent驱动的小说处理系统
====================================

这个脚本不使用外部API，而是生成指令文件
让 Claude Code Agent 来处理整个小说

使用方法：
1. 运行此脚本生成指令文件
2. Claude Code Agent 会自动读取指令文件并执行

特点：
- ✅ 由 Claude Code Agent 完成所有分析
- ✅ 逐章阅读，不跳过任何步骤
- ✅ 每10章自动回顾
- ✅ 自动批准并继续
"""

import os
import json
from pathlib import Path
from datetime import datetime


class AgentInstructionGenerator:
    """生成给 Agent 的指令"""

    def __init__(self, novel_path: str, project_name: str, review_interval: int = 10):
        self.novel_path = novel_path
        self.project_name = project_name
        self.review_interval = review_interval
        self.instructions_dir = Path("agent_instructions")
        self.instructions_dir.mkdir(exist_ok=True)

        # 加载进度
        self.progress = self._load_progress()

    def _load_progress(self):
        """加载处理进度"""
        progress_file = Path("tools/progress.json")
        if progress_file.exists():
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "current_chapter": 0,
                "total_chapters": self._count_total_chapters(),
                "auto_mode": True,
                "review_milestone": self.review_interval,
                "last_success": True,
                "needs_review": False
            }

    def _save_progress(self):
        """保存进度"""
        progress_file = Path("tools/progress.json")
        progress_file.parent.mkdir(exist_ok=True)
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=4, ensure_ascii=False)

    def _count_total_chapters(self):
        """统计总章节数"""
        import re
        try:
            with open(self.novel_path, 'r', encoding='utf-8') as f:
                content = f.read()
            pattern = re.compile(r'第[0-9零一二三四五六七八九十百千]+[章回]')
            return len(pattern.findall(content))
        except:
            return 1694  # 默认值

    def generate_main_instruction(self):
        """生成主指令文件"""
        current = self.progress['current_chapter']
        total = self.progress['total_chapters']

        instruction = f"""# 🤖 Claude Code Agent 小说处理任务

## 📋 任务概述

你是一个专业的小说分析和游戏设计 Agent。
你的任务是将小说《{os.path.basename(self.novel_path)}》转换为交互式文字冒险游戏。

**重要提醒：不要跳过任何步骤，不要省略阅读！**

---

## 📊 当前进度

- **小说文件**: `{self.novel_path}`
- **项目名称**: {self.project_name}
- **当前章节**: {current}/{total}
- **完成进度**: {current/total*100:.2f}%
- **回顾间隔**: 每 {self.review_interval} 章

---

## 🎯 你需要做的事情

### 阶段1: 读取和分析当前章节

1. **读取章节文件**
   ```bash
   # 使用 Read 工具读取小说文件
   # 从第 {current + 1} 章开始
   ```

2. **完整阅读章节内容**
   - ⚠️ **不要跳过阅读**
   - ⚠️ **不要使用摘要或省略**
   - ✅ 完整阅读每一章的内容

3. **分析章节** (使用提示词 `prompts/01-小说分析器.md`)
   - 提取核心事件
   - 识别角色动态
   - 记录新发现（新角色、新地点、新物品、新设定）
   - 评估剧情重要性

4. **更新累积数据**
   - 更新 `data/accumulated_context.json`
   - 添加新发现到相应列表

### 阶段2: 每章都要执行的更新

对于**每一章**，你都需要：

1. **更新世界观** (使用 `prompts/02-世界观提取器.md`)
   - 提取力量体系
   - 提取地理设定
   - 提取社会制度

2. **更新角色信息** (使用 `prompts/03-角色分析器.md`)
   - 更新角色档案
   - 分析角色关系
   - 记录角色成长

3. **生成章节摘要**
   - 总结本章核心内容
   - 记录重要事件
   - 保存到 `data/chapter_summaries/chapter_{current + 1}.json`

4. **保存进度**
   - 更新 `tools/progress.json`
   - 设置 `current_chapter` 为 {current + 1}

### 阶段3: 每{self.review_interval}章的回顾

当完成第 {current + self.review_interval} 章时，执行回顾：

1. **统计分析**
   - 统计累积发现的角色数量
   - 统计累积发现的地点数量
   - 统计累积发现的物品数量

2. **质量检查**
   - 检查最近{self.review_interval}章的摘要
   - 确保没有遗漏重要信息
   - 验证角色关系的一致性

3. **生成回顾报告**
   - 保存到 `data/reviews/review_{current // self.review_interval + 1}.md`
   - 包含统计信息和质量评估

4. **自动批准并继续**
   - 在回顾报告中写明 "✅ 已批准"
   - 继续处理下一批次

---

## 📁 文件结构

你需要维护以下文件：

```
data/
├── accumulated_context.json          # 累积上下文
├── world_setting.json                # 世界观设定
├── characters.json                   # 角色档案
├── chapter_summaries/                # 章节摘要
│   ├── chapter_1.json
│   ├── chapter_2.json
│   └── ...
└── reviews/                          # 回顾报告
    ├── review_1.md                   # 第1-10章回顾
    ├── review_2.md                   # 第11-20章回顾
    └── ...
```

---

## 🔄 工作流程

```
开始
  ↓
读取第{current + 1}章 (使用 Read 工具) ← 重要：完整阅读！
  ↓
分析章节 (使用 01-小说分析器.md)
  ↓
更新世界观 (使用 02-世界观提取器.md)
  ↓
更新角色 (使用 03-角色分析器.md)
  ↓
生成章节摘要
  ↓
保存进度 (更新 tools/progress.json)
  ↓
如果到达回顾点 (第{current + self.review_interval}章)
  ├─ 执行回顾
  ├─ 生成报告
  └─ 自动批准
  ↓
继续下一章 (重复流程)
```

---

## 📝 提示词参考

处理过程中使用以下提示词：

1. **`prompts/01-小说分析器.md`** - 分析每个章节
2. **`prompts/02-世界观提取器.md`** - 提取世界观元素
3. **`prompts/03-角色分析器.md`** - 分析角色信息
4. **`prompts/04-剧情设计器.md`** - 设计剧情分支（每{self.review_interval * 10}章）
5. **`prompts/05-世界线收束设计.md`** - 设计收束点（中期）
6. **`prompts/06-属性系统设计.md`** - 设计属性系统（中期）
7. **`prompts/07-物品道具设计.md`** - 设计物品系统（中期）
8. **`prompts/08-探索系统设计.md`** - 设计探索系统（中期）

---

## ⚠️ 重要提醒

### 必须遵守的原则：

1. ✅ **完整阅读每一章** - 不要跳过，不要省略
2. ✅ **每章都要分析** - 不要批量处理
3. ✅ **每章都要更新** - 世界观、角色、摘要
4. ✅ **保存所有数据** - 不要遗漏任何文件
5. ✅ **按顺序处理** - 从第{current + 1}章开始，逐章进行

### 不要做的事情：

1. ❌ 不要跳过阅读步骤
2. ❌ 不要批量处理多章
3. ❌ 不要省略任何分析步骤
4. ❌ 不要忘记保存进度
5. ❌ 不要跳过回顾检查

---

## 🚀 开始执行

**现在开始处理第 {current + 1} 章！**

1. 使用 Read 工具读取小说文件的第 {current + 1} 章
2. 完整阅读章节内容
3. 按照上述流程进行分析和处理
4. 保存所有结果文件
5. 更新进度并继续下一章

**记住：不要跳过任何步骤，不要省略阅读！**

---

## 📊 进度跟踪

每完成一章，在此文件末尾添加完成记录：

### 完成记录

- [ ] 第{current + 1}章 - 待处理
- [ ] 第{current + 2}章 - 待处理
- [ ] ...

---

**开始执行吧！** 🎉
"""

        # 保存指令文件
        instruction_file = self.instructions_dir / "CURRENT_TASK.md"
        with open(instruction_file, 'w', encoding='utf-8') as f:
            f.write(instruction)

        print(f"✅ 主指令文件已生成: {instruction_file}")
        return instruction_file

    def generate_chapter_task(self, chapter_num: int):
        """生成单章处理任务"""
        task = f"""# 第 {chapter_num} 章处理任务

## 📖 任务说明

处理小说的第 {chapter_num} 章。

## 🔧 执行步骤

### 1. 读取章节

使用 Read 工具读取小说文件，提取第 {chapter_num} 章的内容。

```python
# 伪代码示例
content = read_file("{self.novel_path}")
chapter_{chapter_num}_content = extract_chapter(content, {chapter_num})
```

### 2. 完整阅读

⚠️ **重要**: 完整阅读章节内容，不要跳过！

### 3. 分析章节

参考 `prompts/01-小说分析器.md`，提取：

- **核心事件**: 本章发生的主要事件
- **角色动态**: 角色的行为、对话、心理
- **新发现**:
  - 新角色（名称、初步特征）
  - 新地点（名称、描述）
  - 新物品（名称、作用）
  - 新设定（世界观元素）

### 4. 更新数据

#### 4.1 更新累积上下文

编辑 `data/accumulated_context.json`:

```json
{{
  "已识别角色": [...],  // 添加新角色
  "已知世界观元素": [...],  // 添加新设定
  "前文摘要": "...",  // 更新摘要
  "片段摘要列表": [...],  // 添加本章摘要
  "发现的物品": [...],  // 添加新物品
  "发现的地点": [...]  // 添加新地点
}}
```

#### 4.2 更新世界观

参考 `prompts/02-世界观提取器.md`，更新 `data/world_setting.json`

#### 4.3 更新角色

参考 `prompts/03-角色分析器.md`，更新 `data/characters.json`

### 5. 生成章节摘要

创建 `data/chapter_summaries/chapter_{chapter_num}.json`:

```json
{{
  "chapter_number": {chapter_num},
  "核心事件": "...",
  "详细描述": "...",
  "剧情重要性": "核心剧情/支线剧情/日常",
  "角色动态": [...],
  "新发现": {{...}}
}}
```

### 6. 更新进度

编辑 `tools/progress.json`:

```json
{{
  "current_chapter": {chapter_num},
  "last_success": true
}}
```

### 7. 完成确认

在 `agent_instructions/CURRENT_TASK.md` 末尾标记完成：

```markdown
- [x] 第{chapter_num}章 - ✅ 已完成 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
```

---

**完成后，继续处理第 {chapter_num + 1} 章。**
"""

        task_file = self.instructions_dir / f"task_chapter_{chapter_num}.md"
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task)

        return task_file

    def generate_review_task(self, review_num: int, start_chapter: int, end_chapter: int):
        """生成回顾任务"""
        task = f"""# 第 {review_num} 次回顾任务

## 📊 回顾范围

第 {start_chapter} 章 到 第 {end_chapter} 章

## 🔍 回顾内容

### 1. 统计分析

检查 `data/accumulated_context.json`，统计：

- 累积角色数量: ____ 个
- 累积地点数量: ____ 个
- 累积物品数量: ____ 个
- 累积设定数量: ____ 个

### 2. 质量检查

检查以下文件：

```
data/chapter_summaries/chapter_{start_chapter}.json
data/chapter_summaries/chapter_{start_chapter + 1}.json
...
data/chapter_summaries/chapter_{end_chapter}.json
```

确认：
- ✅ 每章都有摘要文件
- ✅ 所有核心事件都已记录
- ✅ 角色动态都已提取
- ✅ 新发现都已添加

### 3. 一致性验证

检查 `data/characters.json`：
- 角色名称拼写一致
- 角色关系合理
- 角色成长连贯

### 4. 生成回顾报告

创建 `data/reviews/review_{review_num}.md`:

```markdown
# 第 {review_num} 次回顾报告

**回顾时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**回顾范围**: 第 {start_chapter} 章 - 第 {end_chapter} 章

## 📊 统计信息

- 累积角色: XXX 个
- 累积地点: XXX 个
- 累积物品: XXX 个
- 累积设定: XXX 个

## 📝 最近章节摘要

1. 第{start_chapter}章: ...
2. 第{start_chapter + 1}章: ...
...

## ✅ 质量评估

- 完整性: ✅ 良好 / ⚠️ 有遗漏
- 一致性: ✅ 良好 / ⚠️ 有矛盾
- 准确性: ✅ 良好 / ⚠️ 需修正

## 🎯 下一步

✅ 已批准，继续处理第 {end_chapter + 1} 章到第 {end_chapter + self.review_interval} 章

---

**回顾完成，继续处理！**
```

### 5. 自动批准

在报告中标记 "✅ 已批准"，然后继续处理下一批次。

---

**完成回顾后，立即开始处理第 {end_chapter + 1} 章。**
"""

        task_file = self.instructions_dir / f"review_{review_num}.md"
        with open(task_file, 'w', encoding='utf-8') as f:
            f.write(task)

        return task_file

    def setup_data_directories(self):
        """设置数据目录结构"""
        dirs = [
            "data",
            "data/chapter_summaries",
            "data/reviews"
        ]

        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        # 初始化累积上下文
        context_file = Path("data/accumulated_context.json")
        if not context_file.exists():
            initial_context = {
                "已识别角色": [],
                "已知世界观元素": [],
                "前文摘要": "",
                "当前剧情阶段": "起",
                "片段摘要列表": [],
                "章节总结列表": [],
                "卷总结列表": [],
                "发现的物品": [],
                "发现的地点": [],
                "发现的设定": []
            }
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(initial_context, f, indent=2, ensure_ascii=False)

        # 初始化世界观文件
        world_file = Path("data/world_setting.json")
        if not world_file.exists():
            with open(world_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

        # 初始化角色文件
        char_file = Path("data/characters.json")
        if not char_file.exists():
            with open(char_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2, ensure_ascii=False)

        print("✅ 数据目录结构已设置")

    def run(self):
        """运行指令生成器"""
        print("\n" + "="*70)
        print("🤖 Agent驱动的小说处理系统 - 指令生成器")
        print("="*70)
        print(f"\n📚 小说: {self.novel_path}")
        print(f"📦 项目: {self.project_name}")
        print(f"📊 当前章节: {self.progress['current_chapter']}/{self.progress['total_chapters']}")
        print(f"🔍 回顾间隔: 每 {self.review_interval} 章")
        print("\n" + "="*70 + "\n")

        # 设置目录
        self.setup_data_directories()

        # 生成主指令
        main_instruction = self.generate_main_instruction()

        # 生成当前章节任务
        current = self.progress['current_chapter']
        next_chapter = current + 1
        self.generate_chapter_task(next_chapter)

        # 如果需要回顾，生成回顾任务
        if next_chapter > 0 and next_chapter % self.review_interval == 0:
            review_num = next_chapter // self.review_interval
            start = (review_num - 1) * self.review_interval + 1
            end = next_chapter
            self.generate_review_task(review_num, start, end)

        print(f"\n✅ 指令文件已生成完毕！\n")
        print("📄 生成的文件:")
        print(f"   - {main_instruction}")
        print(f"   - agent_instructions/task_chapter_{next_chapter}.md")

        print("\n" + "="*70)
        print("🚀 下一步: 让 Claude Code Agent 读取指令文件并执行")
        print("="*70)
        print("\n📖 Agent 应该:")
        print(f"   1. 读取 {main_instruction}")
        print(f"   2. 按照指令处理第 {next_chapter} 章")
        print(f"   3. 完成后更新进度并继续下一章")
        print("\n" + "="*70 + "\n")


def main():
    generator = AgentInstructionGenerator(
        novel_path="novel/斗破苍穹.txt",
        project_name="斗破苍穹游戏",
        review_interval=10
    )
    generator.run()


if __name__ == "__main__":
    main()
