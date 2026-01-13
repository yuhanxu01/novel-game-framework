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
    print("Bootstrapping Chapter 4...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 4
    chapter_4, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_004",
        defaults={
            'title': "第四章 云岚宗",
            'order': 4,
            'content': {'text': "大厅中，气氛愈发凝重..."}
        }
    )

    # 2. Update Scene (Same as Ch3 but dynamic content)
    hall = Scene.objects.get(scene_id="scene_003_main_hall")

    # 3. Define Story Nodes
    ch4_nodes = [
        {
            "node_id": "node_ch4_001",
            "node_type": "narration",
            "content": "薰儿凑近你，轻声点破了这三位客人的来头：他们竟然是加玛帝国霸主——云岚宗的人。",
            "next": "node_ch4_002"
        },
        {
            "node_id": "node_ch4_002",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "那个少女，就是纳兰嫣然，也就是那个与你指腹为婚的未婚妻。",
            "next": "node_ch4_003"
        },
        {
            "node_id": "node_ch4_003",
            "node_type": "dialogue",
            "speaker": "char_xun_er",
            "content": "她五年前被云岚宗宗主云韵收为弟子。当一个人有了改变命运的力量，就会想解决掉不满意的事... 比如这桩婚事。",
            "next": "node_ch4_004"
        },
        {
            "node_id": "node_ch4_004",
            "node_type": "choice",
            "description": "你意识到她是来退婚的。一旦在大厅提出，你和你父亲的颜面将彻底扫地。你的手掌猛然握紧。",
            "options": [
                {
                    "text": "压抑怒火，冷静观察",
                    "next": "node_ch4_005_confront",
                    "effects": {"attribute_change": {"Calm": 1}}
                },
                {
                    "text": "满脸冰霜，眼神阴沉",
                    "next": "node_ch4_005_confront",
                    "effects": {"attribute_change": {"Anger": 1}}
                }
            ]
        },
        {
            "node_id": "node_ch4_005_confront",
            "node_type": "narration",
            "content": "在大厅上首，纳兰嫣然不断向葛叶使眼色。葛叶终于站了起来，脸上带着勉强的笑容...",
            "next": None
        }
    ]

    ch4_data = {
        "chapter_id": "chapter_004",
        "scenes": [
            {
                "scene_id": "scene_003_main_hall", # Reuse scene
                "content": {"nodes": ch4_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch3 to ch4
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_003':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch4_001'

    # Add ch4
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_004'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch4_data
    else:
        chapters.append(ch4_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 4 data injected.")

if __name__ == "__main__":
    bootstrap()
