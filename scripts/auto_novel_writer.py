#!/usr/bin/env python3
"""
自动小说处理系统 - 一键启动脚本
====================================

功能：
1. 自动处理小说的每一章，不跳过阅读
2. 每10章自动回顾检查
3. 自动批准并继续下一批次
4. 完整处理整个小说

使用方法：
python auto_novel_writer.py --novel novel/斗破苍穹.txt --name "斗破苍穹游戏" --api_key YOUR_API_KEY

可选参数：
--provider: API提供商 (deepseek/openai), 默认deepseek
--review-interval: 回顾间隔章节数, 默认10
--auto-approve: 自动批准回顾, 默认False
--resume: 从上次中断的地方继续
"""

import os
import sys
import time
import argparse
import json
from datetime import datetime
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')

import django
django.setup()

from backend.game.models import GameProject, AnalysisCache
from backend.creative.novel_processor import NovelProcessor
from backend.creative.ai_agent import NovelAnalyzer
from tools.progress_tracker import ProgressTracker


class AutoNovelWriter:
    """自动小说处理器"""

    def __init__(self, novel_path: str, project_name: str, api_key: str,
                 provider: str = "deepseek", review_interval: int = 10,
                 auto_approve: bool = False):
        self.novel_path = novel_path
        self.project_name = project_name
        self.api_key = api_key
        self.provider = provider
        self.review_interval = review_interval
        self.auto_approve = auto_approve

        # 初始化进度跟踪器
        self.tracker = ProgressTracker()
        self.tracker.state['review_milestone'] = review_interval
        self.tracker.save_state()

        # 初始化或获取项目
        self.project = self._ensure_project()

        # 初始化处理器
        self.processor = NovelProcessor(self.project, self.api_key, self.provider)

        # 统计信息
        self.stats = {
            'start_time': datetime.now(),
            'chapters_processed': 0,
            'reviews_completed': 0,
            'errors': []
        }

    def _ensure_project(self) -> GameProject:
        """确保项目存在"""
        project, created = GameProject.objects.get_or_create(
            name=self.project_name,
            defaults={'description': f'自动生成自 {os.path.basename(self.novel_path)}'}
        )

        if created or not project.novel_file:
            print(f"📁 附加小说文件: {self.novel_path}")
            from django.core.files import File
            with open(self.novel_path, 'rb') as f:
                project.novel_file.save(os.path.basename(self.novel_path), File(f))
            project.save()

        print(f"📚 项目: {self.project_name} (ID: {project.id})")
        return project

    def _print_status(self):
        """打印当前状态"""
        current = self.tracker.state['current_chapter']
        total = self.tracker.state['total_chapters']
        progress = (current / total * 100) if total > 0 else 0

        print("\n" + "="*70)
        print(f"📊 当前状态")
        print("="*70)
        print(f"当前章节: {current}/{total} ({progress:.2f}%)")
        print(f"已处理章节: {self.stats['chapters_processed']}")
        print(f"已完成回顾: {self.stats['reviews_completed']}")
        print(f"运行时间: {datetime.now() - self.stats['start_time']}")
        print("="*70 + "\n")

    def _perform_review(self, chapter_num: int):
        """执行回顾检查"""
        print("\n" + "🔍"*35)
        print(f"🔍 第 {chapter_num} 章 - 里程碑回顾")
        print("🔍"*35)

        # 读取最近处理的章节缓存
        recent_caches = AnalysisCache.objects.filter(
            project=self.project
        ).order_by('-chunk_index')[:self.review_interval]

        print(f"\n📖 回顾范围: 第 {chapter_num - self.review_interval + 1} 到 {chapter_num} 章")
        print(f"✅ 已处理片段数: {recent_caches.count()}")

        # 统计信息
        character_count = len(self.processor.accumulated_context.get('已识别角色', []))
        location_count = len(self.processor.discovered_locations)
        item_count = len(self.processor.discovered_items)

        print(f"\n📊 累积发现:")
        print(f"   - 角色: {character_count}")
        print(f"   - 地点: {location_count}")
        print(f"   - 物品: {item_count}")

        # 显示最近的章节摘要
        print(f"\n📝 最近章节摘要:")
        for i, summary in enumerate(self.processor.accumulated_context['片段摘要列表'][-5:]):
            if summary.get('核心事件'):
                print(f"   {i+1}. {summary['核心事件'][:80]}...")

        if self.auto_approve:
            print(f"\n✅ 自动批准模式已启用 - 继续处理下一批次")
            self.tracker.approve_milestone()
            self.stats['reviews_completed'] += 1
        else:
            print(f"\n⏸️  等待用户确认...")
            user_input = input("输入 'y' 批准并继续, 'q' 退出, 's' 查看详细统计: ")

            if user_input.lower() == 'q':
                print("❌ 用户中止执行")
                return False
            elif user_input.lower() == 's':
                self._show_detailed_stats()
                user_input = input("输入 'y' 批准并继续, 'q' 退出: ")
                if user_input.lower() == 'q':
                    return False

            self.tracker.approve_milestone()
            self.stats['reviews_completed'] += 1
            print("✅ 已批准 - 继续处理")

        print("🔍"*35 + "\n")
        return True

    def _show_detailed_stats(self):
        """显示详细统计信息"""
        print("\n" + "="*70)
        print("📈 详细统计信息")
        print("="*70)

        # 世界观元素
        print("\n🌍 世界观元素:")
        for i, element in enumerate(self.processor.world_setting.keys(), 1):
            print(f"   {i}. {element}")

        # 角色列表
        print("\n👥 角色列表:")
        for i, char in enumerate(self.processor.accumulated_context['已识别角色'][:10], 1):
            print(f"   {i}. {char}")
        if len(self.processor.accumulated_context['已识别角色']) > 10:
            print(f"   ... 还有 {len(self.processor.accumulated_context['已识别角色']) - 10} 个")

        # 错误列表
        if self.stats['errors']:
            print("\n❌ 错误记录:")
            for i, error in enumerate(self.stats['errors'][-5:], 1):
                print(f"   {i}. {error}")

        print("="*70 + "\n")

    def _process_single_chapter(self, chunk_index: int, chunk_content: str) -> bool:
        """处理单个章节"""
        try:
            print(f"\n📖 正在处理第 {chunk_index + 1} 章...")
            print(f"   字数: {len(chunk_content)}")

            # 分析片段（不跳过）
            start_time = time.time()
            result = self.processor.process_chunk(chunk_index, chunk_content)
            elapsed = time.time() - start_time

            print(f"   ✅ 分析完成 (耗时: {elapsed:.2f}秒)")

            # 显示分析结果概要
            if '片段摘要' in result:
                summary = result['片段摘要']
                if summary.get('核心事件'):
                    print(f"   📝 核心事件: {summary['核心事件'][:60]}...")

            # 每章都生成总结并更新世界观和角色
            self.processor.generate_chapter_summary(chunk_index)
            self.processor.update_world_setting(chunk_index)
            self.processor.update_characters(chunk_index)

            # 更新进度
            self.tracker.complete_chapter(chunk_index + 1)
            self.stats['chapters_processed'] += 1

            # 保存项目状态
            progress = int((chunk_index + 1) / self.tracker.state['total_chapters'] * 100)
            self.project.analysis_progress = progress
            self.project.save()

            return True

        except Exception as e:
            error_msg = f"第 {chunk_index + 1} 章处理失败: {str(e)}"
            print(f"   ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            self.tracker.complete_chapter(chunk_index + 1, success=False)
            return False

    def run(self):
        """运行自动处理流程"""
        print("\n" + "🚀"*35)
        print("🚀 自动小说处理系统启动")
        print("🚀"*35)
        print(f"\n📚 小说: {self.novel_path}")
        print(f"📦 项目: {self.project_name}")
        print(f"🤖 AI提供商: {self.provider}")
        print(f"📊 回顾间隔: 每 {self.review_interval} 章")
        print(f"✅ 自动批准: {'是' if self.auto_approve else '否'}")

        self._print_status()

        # 获取起始章节
        start_chapter = self.tracker.state['current_chapter']

        # 如果需要回顾，先处理
        if self.tracker.state.get('needs_review'):
            print("⚠️  检测到待回顾状态，执行回顾...")
            if not self._perform_review(start_chapter):
                return

        print(f"\n开始从第 {start_chapter + 1} 章处理...\n")

        # 按章节模式读取
        try:
            chunk_index = 0
            for chunk_index, chunk_content in self.processor.read_novel_by_chapters():
                # 跳过已处理的章节
                if chunk_index < start_chapter:
                    continue

                # 处理章节
                if not self._process_single_chapter(chunk_index, chunk_content):
                    print(f"\n⚠️  第 {chunk_index + 1} 章处理失败，是否继续？")
                    if not self.auto_approve:
                        user_input = input("输入 'y' 继续, 其他键退出: ")
                        if user_input.lower() != 'y':
                            break

                # 检查是否需要回顾
                current = chunk_index + 1
                if current > 0 and current % self.review_interval == 0:
                    self._print_status()
                    if not self._perform_review(current):
                        break

                # 每章都打印简要状态
                if (chunk_index + 1) % 5 == 0:
                    self._print_status()

            # 完成所有章节后，生成最终游戏设计
            if chunk_index >= self.tracker.state['total_chapters'] - 1:
                print("\n" + "🎉"*35)
                print("🎉 所有章节处理完成！开始生成最终游戏设计...")
                print("🎉"*35 + "\n")

                final_design = self.processor.finalize_game_design()

                # 保存最终设计
                self.project.world_setting = final_design['world_setting']
                self.project.characters = final_design['characters']
                self.project.story_tree = final_design['story_tree']
                self.project.attributes = final_design['attributes']
                self.project.items = final_design['items']
                self.project.exploration = final_design['exploration']
                self.project.analysis_status = 'completed'
                self.project.analysis_progress = 100
                self.project.save()

                print("✅ 游戏数据已生成并保存！")

        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断执行")
            self._print_status()
            print("💾 进度已保存，可使用 --resume 参数继续")

        except Exception as e:
            print(f"\n\n❌ 发生错误: {str(e)}")
            import traceback
            traceback.print_exc()

        finally:
            # 打印最终统计
            print("\n" + "="*70)
            print("📊 最终统计")
            print("="*70)
            print(f"总运行时间: {datetime.now() - self.stats['start_time']}")
            print(f"处理章节数: {self.stats['chapters_processed']}")
            print(f"完成回顾数: {self.stats['reviews_completed']}")
            print(f"错误次数: {len(self.stats['errors'])}")
            print("="*70)

            if self.stats['errors']:
                print("\n❌ 错误详情:")
                for error in self.stats['errors']:
                    print(f"   - {error}")


def main():
    parser = argparse.ArgumentParser(
        description='自动小说处理系统 - 一键启动脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用
  python auto_novel_writer.py --novel novel/斗破苍穹.txt --name "斗破苍穹游戏" --api_key YOUR_KEY

  # 自动批准模式（无需人工确认）
  python auto_novel_writer.py --novel novel/斗破苍穹.txt --name "斗破苍穹游戏" --api_key YOUR_KEY --auto-approve

  # 自定义回顾间隔（每5章回顾一次）
  python auto_novel_writer.py --novel novel/斗破苍穹.txt --name "斗破苍穹游戏" --api_key YOUR_KEY --review-interval 5

  # 从上次中断的地方继续
  python auto_novel_writer.py --resume --api_key YOUR_KEY
        """
    )

    parser.add_argument('--novel', help='小说文件路径 (如: novel/斗破苍穹.txt)')
    parser.add_argument('--name', help='项目名称 (如: "斗破苍穹游戏")')
    parser.add_argument('--api_key', help='API密钥 (或设置环境变量 DEEPSEEK_API_KEY)')
    parser.add_argument('--provider', default='deepseek',
                       choices=['deepseek', 'openai'],
                       help='AI提供商 (默认: deepseek)')
    parser.add_argument('--review-interval', type=int, default=10,
                       help='回顾间隔章节数 (默认: 10)')
    parser.add_argument('--auto-approve', action='store_true',
                       help='自动批准回顾，无需人工确认')
    parser.add_argument('--resume', action='store_true',
                       help='从上次中断的地方继续')

    args = parser.parse_args()

    # 恢复模式
    if args.resume:
        tracker = ProgressTracker()
        if not tracker.state.get('current_chapter'):
            print("❌ 没有找到之前的进度，请使用正常模式启动")
            return

        # 从状态文件读取之前的配置
        print("📂 检测到之前的进度，继续处理...")
        # 注意：resume模式下仍需要提供api_key
        if not args.api_key and not os.environ.get('DEEPSEEK_API_KEY'):
            print("❌ 请提供 API Key")
            return

        # 这里需要从之前的配置读取小说路径和项目名
        # 为简化，我们要求用户仍提供这些参数
        if not args.novel or not args.name:
            print("❌ Resume模式下仍需提供 --novel 和 --name 参数")
            return
    else:
        # 正常模式，检查必需参数
        if not args.novel or not args.name:
            parser.print_help()
            print("\n❌ 错误: --novel 和 --name 是必需参数")
            return

        if not args.api_key and not os.environ.get('DEEPSEEK_API_KEY'):
            parser.print_help()
            print("\n❌ 错误: 请提供 API Key (通过 --api_key 或环境变量 DEEPSEEK_API_KEY)")
            return

    # 创建并运行自动处理器
    writer = AutoNovelWriter(
        novel_path=args.novel,
        project_name=args.name,
        api_key=args.api_key or os.environ.get('DEEPSEEK_API_KEY'),
        provider=args.provider,
        review_interval=args.review_interval,
        auto_approve=args.auto_approve
    )

    writer.run()


if __name__ == "__main__":
    main()
