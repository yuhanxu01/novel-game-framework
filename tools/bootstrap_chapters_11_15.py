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

    # Ch 11: Facing Jialie Ao
    add_chapter(11, "第十一章 冲突", "萧家坊市内，冲突一触即发...", "scene_010_street", [
        {"node_id": "node_ch11_001", "node_type": "narration", "content": "你在坊市中寻找魔核，却发现薰儿被加列家族的少爷加列奥纠缠。", "next": "node_ch11_002"},
        {"node_id": "node_ch11_002", "node_type": "action", "content": "你冷哼一声，走了过去，一把抓住了薰儿被纠缠的小手。", "next": "node_ch11_003"},
        {"node_id": "node_ch11_003", "node_type": "dialogue", "speaker": "char_xiao_yan", "content": "以后离他远点。一条疯狗咬了你，你难道还要咬回去？", "next": None}
    ], link_from="chapter_010")

    # Ch 12-14: The Black Iron & Refinement
    add_chapter(12, "第十二章 捡漏", "在坊市的地摊上，你发现了一块不起眼的黑铁片...", "scene_010_street", [
        {"node_id": "node_ch12_001", "node_type": "narration", "content": "在药老的提醒下，你以极低的价格‘顺带’买走了一块生锈的黑铁片。", "next": "node_ch12_002"},
        {"node_id": "node_ch12_002", "node_type": "narration", "content": "回到房间，药老告诉你这就是玄阶低级斗技：吸掌！", "next": "node_ch12_003"},
        {"node_id": "node_ch12_003", "node_type": "action", "content": "药老展示出森白火焰，为你炼制了第一瓶筑基灵液。你踏入了疯狂修炼的阶段。", "next": None}
    ], link_from="chapter_011")

    # Ch 15-16: Training & Xiao Ning
    add_chapter(15, "第十五章 萧宁的挑战", "斗技堂内，你遇到了大长老的孙子萧宁...", "scene_ch16_hall", [
        {"node_id": "node_ch15_001", "node_type": "narration", "content": "在练习‘吸掌’半个月后，你前往斗技堂寻书，撞见了正在切磋的萧宁与薰儿。", "next": "node_ch15_002"},
        {"node_id": "node_ch15_002", "node_type": "dialogue", "speaker": "char_xiao_ning", "content": "萧炎，你这个废物也配和薰儿在一起？成人仪式上，我会让你变成残废！", "next": "node_ch15_003"},
        {"node_id": "node_ch15_003", "node_type": "choice", "description": "面对萧宁的挑衅，你该如何回应？", "options": [
            {"text": "冷淡回应：'我等着。'", "next": "node_ch15_004", "effects": {"attribute_change": {"Calm": 2}}},
            {"text": "反唇相讥：'三年前你可不敢这么说话。'", "next": "node_ch15_004", "effects": {"attribute_change": {"Reputation": 1}}}
        ]},
        {"node_id": "node_ch15_004", "node_type": "narration", "content": "你头也不回地离去，只留下愤怒的萧宁和担心的薰儿。", "next": None}
    ], link_from="chapter_012")

    project.story_tree = tree
    project.save()
    print("Success! Chapters 11-15 injected.")

if __name__ == "__main__":
    bootstrap()
