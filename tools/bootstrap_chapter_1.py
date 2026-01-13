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
    print("Bootstrapping Chapter 1...")
    
    # 1. Create Project
    # GameProject does not have 'status' field.
    project = GameProject.objects.first()
    if not project:
        project = GameProject.objects.create(
            name="斗破苍穹",
            description="Thirty years east of the river, thirty years west. Don't bully the young for being poor.",
            # novel_file is required but we can skip it or give a dummy path for now if allowed, 
            # or just assume the file exists at 'novel/斗破苍穹.txt' relative to media root.
            # For now we skip assigning FileField explicitly or accept it might be empty/error if validation runs.
            # But create() hits DB directly.
        )
    else:
        project.name = "斗破苍穹"
        project.save()
        
    print(f"Project: {project.name}")

    # 2. Create Chapter 1
    chapter_title = "第一章 陨落的天才"
    chapter_content_text = """“斗之力，三段！”... (Content truncated for brevity) ..."""
    
    # Chapter content is a JSONField.
    chapter, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_001",
        defaults={
            'title': chapter_title,
            'order': 1,
            'content': {'text': chapter_content_text}
        }
    )
    
    # 3. Create Characters
    # Character has 'data' JSONField.
    # Xiao Yan
    xiao_yan, _ = Character.objects.get_or_create(
        project=project,
        char_id="char_xiao_yan",
        defaults={
            'name': "萧炎",
            'data': {
                'description': "Former genius, now 'trash'. Son of the clan leader. Perseverant but bitter.",
                'attributes': {
                    "Dou Zhi Li": 3,
                    "Reputation": "Low",
                    "Talent": "Dormant"
                }
            }
        }
    )
    
    # Xiao Mei
    xiao_mei, _ = Character.objects.get_or_create(
        project=project,
        char_id="char_xiao_mei",
        defaults={
            'name': "萧媚",
            'data': {
                'description': "Cousin of Xiao Yan. 14 years old. Charming and innocent. Talented.",
                'attributes': {
                    "Dou Zhi Li": 7,
                    "Reputation": "High",
                    "Relationship_XiaoYan": "Distant"
                }
            }
        }
    )

    # 4. Create World Setting / Scenes
    # Scene has 'location' string and 'content' JSONField.
    square, _ = Scene.objects.get_or_create(
        chapter=chapter,
        scene_id="scene_001",
        defaults={
            'name': "乌坦城萧家广场",
            'order': 1,
            'location': "Family Square",
            'content': {
                'description': "A large square in the Xiao Family estate where testing takes place. Crowded and noisy.",
                'location_type': "Public"
            }
        }
    )

    # 5. Link Story Logic
    project.story_tree = {
        "start_node": "node_001",
        "nodes": {
            "node_001": {
                "id": "node_001",
                "text": "萧炎站在测验魔石碑前，看着那耀眼的'斗之力，三段'，听着周围的嘲笑声。",
                "options": [
                    {
                        "text": "默然承受，转身离开",
                        "next_node": "node_002",
                        "effect": {"mood": -1}
                    },
                    {
                        "text": "怒视周围的人",
                        "next_node": "node_003",
                        "effect": {"mood": -1, "reputation": -1}
                    }
                ],
                "scene_id": square.scene_id,
                "characters": [xiao_yan.char_id]
            },
            "node_002": {
                "id": "node_002",
                "text": "你默默地走回队伍后排，孤单的身影显得格外落寞。这时，你听到了'下一个，萧媚'的喊声。",
                "options": [
                    {
                        "text": "观看萧媚的测验",
                        "next_node": "node_004"
                    }
                ]
            }
        }
    }
    project.save()

    print("Success! Chapter 1 data injected.")
    print(f"Created characters: {xiao_yan.name}, {xiao_mei.name}")
    print(f"Created scene: {square.name}")

if __name__ == "__main__":
    bootstrap()
