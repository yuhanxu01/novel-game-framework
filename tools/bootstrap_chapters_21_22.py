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
    project = GameProject.objects.first()
    if not project: return
    tree = project.story_tree
    chapters = tree.get('chapters', [])

    def add_chapter(ch_num, title, text, scene_id, nodes, link_from=None):
        chapter_id = f"chapter_{ch_num:03d}"
        ch_obj, _ = Chapter.objects.get_or_create(
            project=project, chapter_id=chapter_id,
            defaults={'title': title, 'order': ch_num, 'content': {'text': text}}
        )
        ch_data = {"chapter_id": chapter_id, "scenes": [{"scene_id": scene_id, "content": {"nodes": nodes}}]}
        
        if link_from:
            for ch in chapters:
                if ch['chapter_id'] == link_from:
                    ch['scenes'][0]['content']['nodes'][-1]['next'] = nodes[0]['node_id']
        
        idx = next((i for i, c in enumerate(chapters) if c['chapter_id'] == chapter_id), -1)
        if idx >= 0: chapters[idx] = ch_data
        else: chapters.append(ch_data)

    # Ch 21: Entering the Auction House
    add_chapter(21, "第二十一章 雅妃", "乌坦城最大的拍卖场，迎接你的不仅有财富，还有迷人的妖精...", "scene_021_auction", [
        {"node_id": "node_ch21_001", "node_type": "narration", "content": "你身着宽大的黑袍，遮掩住真实面貌，走进了米特尔拍卖行。", "next": "node_ch21_002"},
        {"node_id": "node_ch21_002", "node_type": "dialogue", "speaker": "char_ya_fei", "content": "这位雅阁，看您拿出的灵液品级不低，不知是哪位炼药大师的手笔？", "next": "node_ch21_003"},
        {"node_id": "node_ch21_003", "node_type": "choice", "description": "雅妃那酥麻的娇声在你耳边响起，她试探着你的底细。", "options": [
            {"text": "低沉嗓音保持神秘：'无可奉告。'", "next": "node_ch21_004", "effects": {"attribute_change": {"Mystery": 5}}},
            {"text": "淡然自若：'只管拍卖便是。'", "next": "node_ch21_004", "effects": {"attribute_change": {"Calm": 2}}}
        ]},
        {"node_id": "node_ch21_004", "node_type": "narration", "content": "经过谷尼大师的鉴定，你的筑基灵液被定为二品。拍卖正式开始。", "next": None}
    ], link_from="chapter_020")

    # Ch 22: High-stakes Bidding
    add_chapter(22, "第二十二章 筑基之争", "拍卖会场内，三大家族的族长悉数到场...", "scene_021_auction", [
        {"node_id": "node_ch22_001", "node_type": "narration", "content": "场内气氛火热。加列家族与奥巴家族拼命喊价，价格一路飙升。", "next": "node_ch22_002"},
        {"node_id": "node_ch22_002", "node_type": "narration", "content": "最终，你的父亲萧战以四万金币的高价拿下了灵液。", "next": "node_ch22_003"},
        {"node_id": "node_ch22_003", "node_type": "dialogue", "speaker": "char_xiao_yan", "content": "(心头一震) 原来父亲是为了我...", "next": "node_ch22_004"},
        {"node_id": "node_ch22_004", "node_type": "narration", "content": "这本是你炼制的低配版，却坑了父亲四万金币。这种愧疚让你更加坚定了变强的决心。", "next": None}
    ], link_from="chapter_021")

    project.story_tree = tree
    project.save()
    print("Success! Chapters 21-22 injected.")

if __name__ == "__main__":
    bootstrap()
