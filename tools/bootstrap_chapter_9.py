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
    print("Bootstrapping Chapter 9...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 9
    chapter_9, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_009",
        defaults={
            'title': "第九章 进阶",
            'order': 9,
            'content': {'text': "拜师之后，真正的修炼即将开始..."}
        }
    )

    # 2. Add New Items
    items_data = [
        {"item_id": "item_purple_leaf_orchid", "name": "紫叶兰草", "desc": "Used for refining Nurturing Spirit Liquid."},
        {"item_id": "item_bone_washing_flower", "name": "洗骨花", "desc": "Used for refining Nurturing Spirit Liquid."},
        {"item_id": "item_wood_core_1", "name": "木系一级魔核", "desc": "A primary monster core of wood attribute."}
    ]
    for i_info in items_data:
        Item.objects.get_or_create(
            project=project,
            item_id=i_info['item_id'],
            defaults={'name': i_info['name'], 'data': {'description': i_info['desc']}}
        )

    # 3. Define Story Nodes
    ch9_nodes = [
        {
            "node_id": "node_ch9_001",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "老师，您打算怎么让我在一年内达到七段斗之气？",
            "next": "node_ch9_002"
        },
        {
            "node_id": "node_ch9_002",
            "node_type": "dialogue",
            "speaker": "char_yao_lao",
            "content": "你现在的经脉比常人更扎实，这是三年来实力倒退带来的馈赠。不过，我们需要一点外力：温养灵液。",
            "next": "node_ch9_003"
        },
        {
            "node_id": "node_ch9_003",
            "node_type": "dialogue",
            "speaker": "char_yao_lao",
            "content": "去准备：3支紫叶兰草，2株洗骨花，还有1颗木系一级魔核。",
            "next": "node_ch9_004"
        },
        {
            "node_id": "node_ch9_004",
            "node_type": "narration",
            "content": "你暗自计算了一下，这些材料起码要上千金币，而你手头只有四百。这让刚燃起希望的你感到一阵肉痛。",
            "next": "node_ch9_005"
        },
        {
            "node_id": "node_ch9_005",
            "node_type": "choice",
            "description": "虽然缺钱，但变强的欲望更胜一筹。此时，远处传来一阵灵动的脚步声...",
            "options": [
                {
                    "text": "回头望去",
                    "next": "node_ch9_006_end"
                }
            ]
        },
        {
            "node_id": "node_ch9_006_end",
            "node_type": "narration",
            "content": "一袭紫裙的萧薰儿正轻灵跃来。她似乎察觉到了什么，目光在你的戒指上停留了片刻。",
            "next": None
        }
    ]

    ch9_data = {
        "chapter_id": "chapter_009",
        "scenes": [
            {
                "scene_id": "scene_002_grove",
                "content": {"nodes": ch9_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch8 to ch9
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_008':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch9_001'

    # Add ch9
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_009'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch9_data
    else:
        chapters.append(ch9_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 9 data injected.")

if __name__ == "__main__":
    bootstrap()
