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
    print("Bootstrapping Chapter 3...")
    
    project = GameProject.objects.first()
    if not project:
        print("Project not found!")
        return

    # 1. Create Chapter 3
    chapter_3, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_003",
        defaults={
            'title': "第三章 客从远方来",
            'order': 3,
            'content': {'text': "大厅很是宽敞，人数不少..."}
        }
    )

    # 2. Add/Update Characters
    characters_data = [
        {
            "char_id": "char_xun_er",
            "name": "萧熏儿",
            "data": {
                "description": "Childhood friend of Xiao Yan. Elegant and mysterious. Extremely talented.",
                "attributes": {"Mystery": "High", "Support": "Max"}
            }
        },
        {
            "char_id": "char_nalan_yanran",
            "name": "纳兰嫣然",
            "data": {
                "description": "Yun Lan Sect genius. Proud and distant.",
                "attributes": {"Power": "3-Star Dou Zhe", "Sect": "Yun Lan"}
            }
        },
        {
            "char_id": "char_ge_ye",
            "name": "葛叶",
            "data": {
                "description": "Elder of Yun Lan Sect. 7-Star Da Dou Shi.",
                "attributes": {"Power": "7-Star Da Dou Shi"}
            }
        }
    ]
    
    for c_info in characters_data:
        Character.objects.get_or_create(
            project=project,
            char_id=c_info['char_id'],
            defaults={
                'name': c_info['name'],
                'data': c_info['data']
            }
        )

    # 3. Create Scene
    hall, _ = Scene.objects.get_or_create(
        chapter=chapter_3,
        scene_id="scene_003_main_hall",
        defaults={
            'name': "萧家迎客大厅",
            'order': 1,
            'location': "Xiao Clan Main Hall",
            'content': {
                'description': "Spacious hall filled with elders and guests. Tension is in the air.",
                'location_type': "Public"
            }
        }
    )

    # 4. Update Story Tree
    tree = project.story_tree
    
    ch3_nodes = [
        {
            "node_id": "node_ch3_001",
            "node_type": "narration",
            "content": "你被管家请到了大厅。推开门，只见厅内座无虚席，空气中弥漫着严肃的气息。",
            "next": "node_ch3_002"
        },
        {
            "node_id": "node_ch3_002",
            "node_type": "narration",
            "content": "大厅里坐着三位陌生人。带头的老者竟然是一位七星大斗师，身旁的少女相貌娇嫩，气质高贵。",
            "next": "node_ch3_003"
        },
        {
            "node_id": "node_ch3_003",
            "node_type": "choice",
            "description": "你扫视全场，发现竟然没有人为你准备座次，周围的年轻人正准备看你笑话。",
            "options": [
                {
                    "text": "站在原地，不卑不亢",
                    "next": "node_ch3_004_xun_er"
                },
                {
                    "text": "自嘲一笑，寻找位置",
                    "next": "node_ch3_004_xun_er"
                }
            ]
        },
        {
            "node_id": "node_ch3_004_xun_er",
            "node_id_alias": "薰儿发声",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "萧炎哥哥，坐这里吧！",
            "next": "node_ch3_005"
        },
        {
            "node_id": "node_ch3_005",
            "node_type": "narration",
            "content": "在众人嫉妒的注视下，你坐在了萧薰儿身旁。她正在安静地翻看一本古籍，气质淡雅。",
            "next": "node_ch3_006"
        },
        {
            "node_id": "node_ch3_006",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "萧炎哥哥有三年没和熏儿单独坐一起了吧？",
            "next": "node_ch3_007"
        },
        {
            "node_id": "node_ch3_007",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "你还记得四岁到六岁时，每天晚上偷偷溜进我房间温养经脉的事吗？",
            "next": "node_ch3_008"
        },
        {
            "node_id": "node_ch3_008",
            "node_type": "choice",
            "description": "面对薰儿的调侃和心虚的回忆，你...",
            "options": [
                {
                    "text": "装傻充愣：“你在说什么？”",
                    "next": "node_ch3_009_end"
                },
                {
                    "text": "尴尬低头，默认不语",
                    "next": "node_ch3_009_end"
                }
            ]
        },
        {
            "node_id": "node_ch3_009_end",
            "node_type": "narration",
            "content": "大厅的主位上，萧战与云岚宗的葛叶正在交谈。关键的时刻即将来临...",
            "next": None
        }
    ]

    ch3_data = {
        "chapter_id": "chapter_003",
        "scenes": [
            {
                "scene_id": "scene_003_main_hall",
                "content": {"nodes": ch3_nodes}
            }
        ]
    }

    # Add to tree
    chapters = tree.get('chapters', [])
    # Re-link chain: chapter_002 last node should point to chapter_003 first node
    # Actually story.js handles this via _checkChapterEnd if no 'next' is found, 
    # but we can also set 'next' to 'node_ch3_001' in chapter_002's last node.
    
    # Update ch2 chain
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_002':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch3_001'

    # Add ch3
    existing_ch3 = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_003'), -1)
    if existing_ch3 >= 0:
        chapters[existing_ch3] = ch3_data
    else:
        chapters.append(ch3_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 3 data injected.")

if __name__ == "__main__":
    bootstrap()
