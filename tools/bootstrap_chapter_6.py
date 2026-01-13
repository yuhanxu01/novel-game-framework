import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from game.models import GameProject, Chapter, Scene, Character

def bootstrap():
    print("Bootstrapping Chapter 6...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 6
    chapter_6, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_006",
        defaults={
            'title': "第六章 炼药师",
            'order': 6,
            'content': {'text': "大厅中，众人的目光火热地盯着聚气散。然而，一个冷淡的声音打破了寂静..."}
        }
    )

    # 2. Define Story Nodes
    ch6_nodes = [
        {
            "node_id": "node_ch6_001",
            "node_type": "narration",
            "content": "三位长老正盘算着如何将这枚出自'丹王古河'之手的聚气散据为己有时，你忽然站了起来。",
            "next": "node_ch6_002"
        },
        {
            "node_id": "node_ch6_002",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "葛叶老先生，你还是把丹药收回去吧。今日之事，我们或许不会答应！",
            "next": "node_ch6_003"
        },
        {
            "node_id": "node_ch6_003",
            "node_type": "dialogue",
            "speaker": "长老",
            "content": "萧炎，这里哪有你说话的份？给我闭嘴！",
            "next": "node_ch6_004"
        },
        {
            "node_id": "node_ch6_004",
            "node_type": "choice",
            "description": "三位长老对你的出声感到愤怒，甚至有人准备动手。此时，薰儿再次为你出头。",
            "options": [
                {
                    "text": "感激地看向薰儿",
                    "next": "node_ch6_005_confront",
                    "effects": {"relationship_change": {"char_xun_er": 1}}
                },
                {
                    "text": "冷笑着质问长老：'如果今天悔婚的是你们家孩子，你们还会这么说吗？'",
                    "next": "node_ch6_005_confront",
                    "effects": {"attribute_change": {"Boldness": 1}}
                }
            ]
        },
        {
            "node_id": "node_ch6_005_confront",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "萧炎哥哥说得没错。这事他是当事人，各位长老还是不要插手了。",
            "next": "node_ch6_006"
        },
        {
            "node_id": "node_ch6_006",
            "node_type": "narration",
            "content": "三位长老竟然真的在薰儿的一句话下退缩了。你转过头，直视纳兰嫣然。",
            "next": "node_ch6_007"
        },
        {
            "node_id": "node_ch6_007",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "我想请问纳兰小姐，悔婚之事，纳兰老爷子可曾答应？",
            "next": "node_ch6_008"
        },
        {
            "node_id": "node_ch6_008",
            "node_type": "narration",
            "content": "纳兰嫣然开始不耐烦，开出了更多的条件：三枚聚气散，外加进入云岚宗的机会。她像是一尊骄傲的公主，等待着你的妥协。",
            "next": None
        }
    ]

    ch6_data = {
        "chapter_id": "chapter_006",
        "scenes": [
            {
                "scene_id": "scene_003_main_hall",
                "content": {"nodes": ch6_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch5 to ch6
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_005':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch6_001'

    # Add ch6
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_006'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch6_data
    else:
        chapters.append(ch6_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 6 data injected.")

if __name__ == "__main__":
    bootstrap()
