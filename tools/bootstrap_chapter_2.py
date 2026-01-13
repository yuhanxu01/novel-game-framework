import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

from game.models import GameProject, Chapter, Scene, Character

def bootstrap():
    print("Bootstrapping Chapter 2...")
    
    project = GameProject.objects.first()
    if not project:
        print("Project not found! Run bootstrap_chapter_1.py first.")
        return

    # 1. Create Chapter 2
    chapter_title = "第二章 斗气大陆"
    # We'll use a summary or truncated text for the 'content' field to save space/time in this script
    chapter_content_text = """“呸。”吐出嘴中的草根，萧炎忽然跳起身来，脸庞狰狞，对着夜空失态的咆哮道：“我草你奶奶的，把劳资穿过来当废物玩吗？草！”..."""

    chapter_2, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_002",
        defaults={
            'title': chapter_title,
            'order': 2,
            'content': {'text': chapter_content_text}
        }
    )

    # 2. Update Characters
    # Xiao Zhan
    xiao_zhan, _ = Character.objects.get_or_create(
        project=project,
        char_id="char_xiao_zhan",
        defaults={
            'name': "萧战",
            'data': {
                'description': "Xiao Yan's father. Clan Leader. 5-Star Da Dou Shi. Loves his son heavily.",
                'attributes': {
                    "Strength": "5-Star Da Dou Shi",
                    "Role": "Clan Leader"
                }
            }
        }
    )
    
    # 3. Create Scenes
    # Back Mountain
    grove, _ = Scene.objects.get_or_create(
        chapter=chapter_2,
        scene_id="scene_002_grove",
        defaults={
            'name': "萧家后山",
            'order': 1,
            'location': "Back Mountain",
            'content': {
                'description': "Night time. A quiet grove on the back mountain. Moonlight filters through the trees.",
                'location_type': "Private",
                'time': "Night"
            }
        }
    )

    # 4. Define Story Nodes for Chapter 2
    # We append these to the existing story_tree logic or structured chapters.
    # Since our frontend engine looks at `story_tree.chapters`, we need to make sure that structure exists.
    # In Chapter 1 bootstrap, we put nodes directly in `story_tree['nodes']`. 
    # To support multi-chapter, let's look at `story.js`:
    # `gameData.story_tree.chapters` -> find chapter -> startScene -> processNode.
    
    # We need to restructure the project.story_tree to support the frontend's expected format if it changed,
    # OR (more likely) I should just stick to the 'nodes' flat list if that's what I set up, 
    # BUT `story.js` line 44: `return gameData.story_tree.chapters.find(...)`
    # So I MUST Structure `story_tree` to have a `chapters` list.
    
    # Let's fix Chapter 1 data first while we are at it, or just ensure Chapter 2 follows the format.
    # Actually, let's rewrite the `story_tree` to be robust.

    current_tree = project.story_tree or {}
    
    # If it was flat (from ch1 script), convert to chapters format
    if 'chapters' not in current_tree:
        # Retrofit Chapter 1
        ch1_nodes = current_tree.get('nodes', {})
        current_tree = {
            "chapters": [
                {
                    "chapter_id": "chapter_001",
                    "scenes": [
                        {
                            "scene_id": "scene_001",
                            "content": {
                                "nodes": list(ch1_nodes.values()) 
                                # Note: This assumes ch1_nodes values are the node objects. 
                                # If ch1 script put them in a dict keyed by ID, this works.
                            }
                        }
                    ]
                }
            ]
        }

    # Prepare Chapter 2 Nodes
    ch2_nodes = [
        {
            "node_id": "node_ch2_001",
            "node_type": "narration",
            "content": "夜幕降临，你独自一人来到后山，嘴里叼着草根，心中愤懑难平。",
            "next": "node_ch2_002"
        },
        {
            "node_id": "node_ch2_002",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "把劳资穿过来当废物玩吗？草！",
            "next": "node_ch2_003"
        },
        {
            "node_id": "node_ch2_003",
            "node_type": "action",
            "content": "你对着夜空咆哮，发泄着心中的不甘。然而，咆哮过后，只有更深的落寞。",
            "next": "node_ch2_004"
        },
        {
            "node_id": "node_ch2_004",
            "node_type": "dialogue",
            "speaker": "char_xiao_zhan",
            "content": "呵呵，炎儿，这么晚了，怎么还待在这上面呢？",
            "next": "node_ch2_005"
        },
        {
            "node_id": "node_ch2_005",
            "node_type": "narration",
            "content": "父亲萧战从树林中走出，脸上带着关切的笑容。",
            "next": "node_ch2_006"
        },
        {
            "node_id": "node_ch2_006",
            "node_type": "dialogue",
            "speaker": "char_xiao_zhan",
            "content": "再有一年，就是成年仪式了... 如果斗之气达不到七段，我也只能忍痛把你分配到家族产业中去。",
            "next": "node_ch2_007"
        },
        {
            "node_id": "node_ch2_007",
            "node_type": "choice",
            "description": "面对父亲的担忧和残酷的现实，你...",
            "options": [
                {
                    "text": "强颜欢笑，安慰父亲",
                    "condition": {},
                    "next": "node_ch2_008_comfort",
                    "effects": {"relationship_change": {"char_xiao_zhan": 1}}
                },
                {
                    "text": "沉默不语，攥紧拳头",
                    "condition": {},
                    "next": "node_ch2_008_silent",
                    "effects": {"attribute_change": {"Determination": 1}}
                }
            ]
        },
        {
            "node_id": "node_ch2_008_comfort",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "父亲放心，我会努力的！一年后，我一定达到七段！",
            "next": "node_ch2_009"
        },
        {
            "node_id": "node_ch2_008_silent",
            "node_type": "narration",
            "content": "你低下头，指甲陷入掌心。父亲叹了口气，拍了拍你的肩膀。",
            "next": "node_ch2_009"
        },
        {
            "node_id": "node_ch2_009",
            "node_type": "dialogue",
            "speaker": "char_xiao_zhan",
            "content": "早点休息吧，明天家族有贵客，别失了礼数。",
            "next": "node_ch2_010"
        },
        {
            "node_id": "node_ch2_010",
            "node_type": "narration",
            "content": "父亲走后，你抚摸着手指上母亲留下的古朴黑戒指，喃喃自语。",
            "next": "node_ch2_011"
        },
        {
            "node_id": "node_ch2_011",
            "node_type": "event",
            "event_type": "ring_glow",
            "content": "就在那一刹那，戒指忽然亮起了一抹极其微弱的光芒...",
            "next": None # End of chapter for now
        }
    ]

    # Add Chapter 2 to tree
    chapter_2_data = {
        "chapter_id": "chapter_002",
        "scenes": [
            {
                "scene_id": "scene_002_grove",
                "content": {
                    "nodes": ch2_nodes
                }
            }
        ]
    }
    
    # Append or Replace
    existing_ch2_idx = next((i for i, c in enumerate(current_tree['chapters']) if c['chapter_id'] == 'chapter_002'), -1)
    if existing_ch2_idx >= 0:
        current_tree['chapters'][existing_ch2_idx] = chapter_2_data
    else:
        current_tree['chapters'].append(chapter_2_data)

    project.story_tree = current_tree
    project.save()

    print("Success! Chapter 2 data injected.")
    print(f"Created characters: {xiao_zhan.name}")

if __name__ == "__main__":
    bootstrap()
