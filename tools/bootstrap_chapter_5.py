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
    print("Bootstrapping Chapter 5...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 5
    chapter_5, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_005",
        defaults={
            'title': "第五章 聚气散",
            'order': 5,
            'content': {'text': "大厅中，空气几乎凝固。葛叶提出了解除婚约的要求..."}
        }
    )

    # 2. Add Item
    pill, _ = Item.objects.get_or_create(
        project=project,
        item_id="item_ju_qi_san",
        defaults={
            'name': "聚气散",
            'category': "Pill",
            'data': {
                'description': "A rare pill that ensures 100% success when breaking through to Dou Zhe. Extremely valuable.",
                'rarity': "High"
            }
        }
    )

    # 3. Define Story Nodes
    ch5_nodes = [
        {
            "node_id": "node_ch5_001",
            "node_type": "dialogue",
            "speaker": "char_ge_ye",
            "content": "萧族长，宗主大人想请您... 解除了这婚约。",
            "next": "node_ch5_002"
        },
        {
            "node_id": "node_ch5_002",
            "node_type": "action",
            "content": "咔的一声，萧战手中的玉杯被捏得粉碎。大厅内陷入死寂。",
            "next": "node_ch5_003"
        },
        {
            "node_id": "node_ch5_003",
            "node_type": "narration",
            "content": "萧战周身青色斗气爆发，隐隐幻化成狮头。那是萧家顶级功法：狂狮怒罡！",
            "next": "node_ch5_004"
        },
        {
            "node_id": "node_ch5_004",
            "node_type": "choice",
            "description": "三位长老厉声喝止了萧战，提醒他他是族长，不能冒犯云岚宗。此时，葛叶拿出了一只玉匣。",
            "options": [
                {
                    "text": "看向玉匣中的丹药",
                    "next": "node_ch5_005_pill"
                }
            ]
        },
        {
            "node_id": "node_ch5_005_pill",
            "node_type": "narration",
            "content": "玉匣开启，异香扑鼻。那是三位长老惊呼出的：聚气散！",
            "next": "node_ch5_006"
        },
        {
            "node_id": "node_ch5_006",
            "node_type": "dialogue",
            "speaker": "char_ge_ye",
            "content": "这是宗主大人的赔礼。只要萧家同意退婚，这枚聚气散便归萧家所有。",
            "next": "node_ch5_007"
        },
        {
            "node_id": "node_ch5_007",
            "node_type": "narration",
            "content": "三位长老的目光变得极其火热。这对他们来说是至宝，对萧炎来说却是莫大的侮辱。",
            "next": None
        }
    ]

    ch5_data = {
        "chapter_id": "chapter_005",
        "scenes": [
            {
                "scene_id": "scene_003_main_hall",
                "content": {"nodes": ch5_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch4 to ch5
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_004':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch5_001'

    # Add ch5
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_005'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch5_data
    else:
        chapters.append(ch5_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 5 data injected.")

if __name__ == "__main__":
    bootstrap()
