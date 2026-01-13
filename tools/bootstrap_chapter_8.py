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
    print("Bootstrapping Chapter 8...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 8
    chapter_8, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_008",
        defaults={
            'title': "第八章 神秘的老者",
            'order': 8,
            'content': {'text': "后山之巅，萧炎正自嘲之时，一个声音响起..."}
        }
    )

    # 2. Add Character
    yao_lao, _ = Character.objects.get_or_create(
        project=project,
        char_id="char_yao_lao",
        defaults={
            'name': "药老",
            'data': {
                'description': "A mysterious spirit residing in the ring. A pinnacle-grade Alchemist. Master of Xiao Yan.",
                'attributes': {"Mystery": "Infinity", "Class": "Alchemist Master"}
            }
        }
    )

    # 3. Define Story Nodes
    ch8_nodes = [
        {
            "node_id": "node_ch8_001",
            "node_type": "narration",
            "content": "你在后山悬崖边发泄着心中的悲愤。就在这时，一个戏谑的声音从你的戒指中传了出来。",
            "next": "node_ch8_002"
        },
        {
            "node_id": "node_ch8_002",
            "node_type": "dialogue",
            "speaker": "char_yao_lao",
            "content": "嘿嘿，小娃娃，看来你很需要帮助啊？",
            "next": "node_ch8_003"
        },
        {
            "node_id": "node_ch8_003",
            "node_type": "action",
            "content": "一道透明的苍老人影从戒指中飘荡而出。他承认了这三年是你体内的斗之气供奉了他，才让他醒来。",
            "next": "node_ch8_004"
        },
        {
            "node_id": "node_ch8_004",
            "node_type": "choice",
            "description": "得知三年来受辱的真相，你怒不可遏。老者却笑眯眯地看着你。",
            "options": [
                {
                    "text": "破口大骂：'我草你妈！你个老混蛋！'",
                    "next": "node_ch8_005_negotiate",
                    "effects": {"attribute_change": {"Anger": 1}}
                },
                {
                    "text": "强压怒火，冷冷询问：'你到底想干什么？'",
                    "next": "node_ch8_005_negotiate",
                    "effects": {"attribute_change": {"Calm": 1}}
                }
            ]
        },
        {
            "node_id": "node_ch8_005_negotiate",
            "node_type": "dialogue",
            "speaker": "char_yao_lao",
            "content": "虽然吸了你三年斗气，但也让你心智成长了许多。现在，你想变强吗？",
            "next": "node_ch8_006"
        },
        {
            "node_id": "node_ch8_006",
            "node_type": "dialogue",
            "speaker": "char_yao_lao",
            "content": "只要你跟着我，我不仅能让你一年内达到七段斗之气，还能教你... 炼药术。",
            "next": "node_ch8_007"
        },
        {
            "node_id": "node_ch8_007",
            "node_type": "choice",
            "description": "炼药师，那是斗气大陆最尊贵的职业。你看着老者，陷入了沉思。",
            "options": [
                {
                    "text": "郑重拜师：'老师在上，受徒儿一拜！'",
                    "next": "node_ch8_008_end",
                    "effects": {"relationship_change": {"char_yao_lao": 5}}
                },
                {
                    "text": "存疑观察：'先帮我把斗之气提升再说。'",
                    "next": "node_ch8_008_end",
                    "effects": {"relationship_change": {"char_yao_lao": 1}}
                }
            ]
        },
        {
            "node_id": "node_ch8_008_end",
            "node_type": "narration",
            "content": "一个惊动整片大陆的组合，在中州之外的乌坦城后山，悄然结成。你的传奇，由此开始。",
            "next": None
        }
    ]

    ch8_data = {
        "chapter_id": "chapter_008",
        "scenes": [
            {
                "scene_id": "scene_002_grove", # Reuse grove/back mountain
                "content": {"nodes": ch8_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch7 to ch8
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_007':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch8_001'

    # Add ch8
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_008'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch8_data
    else:
        chapters.append(ch8_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 8 data injected.")

if __name__ == "__main__":
    bootstrap()
