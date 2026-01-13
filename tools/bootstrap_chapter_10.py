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
    print("Bootstrapping Chapter 10...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 10
    chapter_10, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_010",
        defaults={
            'title': "第十章 借钱",
            'order': 10,
            'content': {'text': "为了变强，金钱是必不可少的..."}
        }
    )

    # 2. Define Scene
    street, _ = Scene.objects.get_or_create(
        chapter=chapter_10,
        scene_id="scene_010_street",
        defaults={
            'name': "乌坦城街道",
            'order': 1,
            'location': "Wu Tan City",
            'content': {
                'description': "Hot sun, bustling crowds, streets filled with peddlers.",
                'location_type': "Public"
            }
        }
    )

    # 3. Define Story Nodes
    ch10_nodes = [
        {
            "node_id": "node_ch10_001",
            "node_type": "narration",
            "content": "为了筹集温养灵液的材料，你找到了薰儿。这是你三年来第一次主动寻求她的帮助。",
            "next": "node_ch10_002"
        },
        {
            "node_id": "node_ch10_002",
            "node_type": "choice",
            "description": "看着已经亭亭玉立的薰儿，你亲昵地捏了捏她的小脸。",
            "options": [
                {
                    "text": "打趣：'薰儿也长大了啊。'",
                    "next": "node_ch10_003_money",
                    "effects": {"relationship_change": {"char_xun_er": 2}}
                }
            ]
        },
        {
            "node_id": "node_ch10_003_money",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "咳，那个... 薰儿，你手头还有钱吗？我想借一点。",
            "next": "node_ch10_004"
        },
        {
            "node_id": "node_ch10_004",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "萧炎哥哥需要多少？我这里有一张黑卡，里面有五千金币，够吗？",
            "next": "node_ch10_005"
        },
        {
            "node_id": "node_ch10_005",
            "node_type": "narration",
            "content": "接过薰儿提供的资金，你们一起来到了乌坦城的集市。在药材店，你买下了紫叶兰草和洗骨花。",
            "next": "node_ch10_006"
        },
        {
            "node_id": "node_ch10_006",
            "node_type": "narration",
            "content": "虽然财产瞬间缩水，但材料已经基本备齐。只差最后一枚木系魔核了...",
            "next": None
        }
    ]

    ch10_data = {
        "chapter_id": "chapter_010",
        "scenes": [
            {
                "scene_id": "scene_010_street",
                "content": {"nodes": ch10_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch9 to ch10
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_009':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch10_001'

    # Add ch10
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_010'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch10_data
    else:
        chapters.append(ch10_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 10 data injected.")

if __name__ == "__main__":
    bootstrap()
