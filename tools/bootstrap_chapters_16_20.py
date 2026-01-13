import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from game.models import GameProject, Chapter, Scene, Character, Item

def bootstrap():
    project = GameProject.objects.first()
    if not project: return
    tree = project.story_tree
    chapters = tree.get('chapters', [])

    def add_chapter(ch_num, title, text, scene_id, nodes, link_from=None):
        chapter_id = f"chapter_{ch_num:03d}"
        ch_obj, _ = Chapter.objects.get_or_create(
            project=project, chapter_id=chapter_id,
            defaults={'title': title, 'order': ch_num, 'content': {'text': text}}
        )
        ch_data = {"chapter_id": chapter_id, "scenes": [{"scene_id": scene_id, "content": {"nodes": nodes}}]}
        
        if link_from:
            for ch in chapters:
                if ch['chapter_id'] == link_from:
                    ch['scenes'][0]['content']['nodes'][-1]['next'] = nodes[0]['node_id']
        
        idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == chapter_id), -1)
        if idx >= 0: chapters[idx] = ch_data
        else: chapters.append(ch_data)

    # Ch 18: Yao Lao's Teaching
    add_chapter(18, "第十八章 八极崩", "药老传授了你一门极其霸道的决战技巧...", "scene_002_grove", [
        {"node_id": "node_ch18_001", "node_type": "narration", "content": "回到房间，药老决定传授你防身斗技。他手指轻点你的额头。", "next": "node_ch18_002"},
        {"node_id": "node_ch18_002", "node_type": "narration", "content": "玄阶高级斗技：八极崩！其威力可叠加八重劲气，堪比地阶！", "next": "node_ch18_003"},
        {"node_id": "node_ch18_003", "node_type": "dialogue", "speaker": "char_yao_lao", "content": "但这招对肉体负荷极大。想要变强，就得先学会‘挨打’。", "next": None}
    ], link_from="chapter_015")

    # Ch 19: Sadistic Training
    add_chapter(19, "第十九章 突破五段", "后山的小树林里，惨叫声连绵不断...", "scene_002_grove", [
        {"node_id": "node_ch19_001", "node_type": "narration", "content": "一个半月的‘鞭挞’训练。你在痛苦中感受着肉体的强化与斗之气的活跃。", "next": "node_ch19_002"},
        {"node_id": "node_ch19_002", "node_type": "action", "content": "通过筑基灵液的药浴，你的身体终于发生了质变。", "next": "node_ch19_003"},
        {"node_id": "node_ch19_003", "node_type": "narration", "content": "突破！你终于跨入了第五段斗之气的境界！", "next": None}
    ], link_from="chapter_018")

    # Ch 20: The Auction Plan
    add_chapter(20, "第二十章 拍卖行", "钱，成了目前最大的绊脚石...", "scene_010_street", [
        {"node_id": "node_ch20_001", "node_type": "narration", "content": "灵液耗尽，金币不足。你拒绝了找薰儿借钱，决定自食其力。", "next": "node_ch20_002"},
        {"node_id": "node_ch20_002", "node_type": "dialogue", "speaker": "char_xiao_yan", "content": "老师，我们可以炼制一些低配版的灵液，拿去拍卖行换钱。", "next": "node_ch20_003"},
        {"node_id": "node_ch20_003", "node_type": "narration", "content": "你换上一身黑袍，怀揣着足以引起乌坦城震动的宝物，走向了特米尔拍卖场...", "next": None}
    ], link_from="chapter_019")

    project.story_tree = tree
    project.save()
    print("Success! Chapters 16-20 injected.")

if __name__ == "__main__":
    bootstrap()
