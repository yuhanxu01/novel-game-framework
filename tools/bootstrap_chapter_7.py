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
    print("Bootstrapping Chapter 7...")
    
    project = GameProject.objects.first()
    if not project: return

    # 1. Create Chapter 7
    chapter_7, _ = Chapter.objects.get_or_create(
        project=project,
        chapter_id="chapter_007",
        defaults={
            'title': "第七章 休书",
            'order': 7,
            'content': {'text': "大厅之中，萧炎掷地有声的宣告..."}
        }
    )

    # 2. Define Story Nodes
    ch7_nodes = [
        {
            "node_id": "node_ch7_001",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "纳兰小姐，你看重的无非是我的废物之名。三十年河东，三十年河西，莫欺少年穷！",
            "next": "node_ch7_002"
        },
        {
            "node_id": "node_ch7_002",
            "node_type": "narration",
            "content": "大厅内一片死寂。谁也没想到，平日里沉默的废物少年，竟有如此豪情。",
            "next": "node_ch7_003"
        },
        {
            "node_id": "node_ch7_003",
            "node_type": "dialogue",
            "speaker": "char_nalan_yanran",
            "content": "好！我等着你！三年之后，我在云岚宗等你挑战。若是能赢我，我纳兰嫣然为奴为婢，全由你发落！",
            "next": "node_ch7_004"
        },
        {
            "node_id": "node_ch7_004",
            "node_type": "action",
            "content": "你冷笑一声，俯身提笔，在大厅众目睽睽之下奋笔疾书。笔力遒劲，字字如刀。",
            "next": "node_ch7_005"
        },
        {
            "node_id": "node_ch7_005",
            "node_type": "action",
            "content": "你抽出短剑，在手掌上一划，按下了刺眼的血手印。你将那张纸重重摔在桌上。",
            "next": "node_ch7_006"
        },
        {
            "node_id": "node_ch7_006",
            "node_type": "dialogue",
            "speaker": "char_xiao_yan",
            "content": "这张不是退婚契约，而是本少爷把你逐出萧家的休书！从此你我，再无瓜葛！",
            "next": "node_ch7_007"
        },
        {
            "node_id": "node_ch7_007",
            "node_type": "narration",
            "content": "纳兰嫣然目瞪口呆，看着那张血手契约。你转身跪在父亲面前，重重磕了一头，随后绝然离去。",
            "next": "node_ch7_008"
        },
        {
            "node_id": "node_ch7_008",
            "node_type": "narration",
            "content": "就在纳兰嫣然三人离去之时，角落里的薰儿抬起脸，眸中闪过一丝淡淡的金光，吓得葛叶落荒而逃。",
            "next": None
        }
    ]

    ch7_data = {
        "chapter_id": "chapter_007",
        "scenes": [
            {
                "scene_id": "scene_003_main_hall",
                "content": {"nodes": ch7_nodes}
            }
        ]
    }

    tree = project.story_tree
    chapters = tree.get('chapters', [])
    
    # Link ch6 to ch7
    for ch in chapters:
        if ch['chapter_id'] == 'chapter_006':
            ch['scenes'][0]['content']['nodes'][-1]['next'] = 'node_ch7_001'

    # Add ch7
    existing_idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == 'chapter_007'), -1)
    if existing_idx >= 0:
        chapters[existing_idx] = ch7_data
    else:
        chapters.append(ch7_data)
    
    tree['chapters'] = chapters
    project.story_tree = tree
    project.save()
    
    print("Success! Chapter 7 data injected.")

if __name__ == "__main__":
    bootstrap()
