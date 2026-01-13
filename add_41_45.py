import json
import os

# 定义路径
data_path = '/Users/renqing/novel-game-framework/frontend/data/game_data_doupo.json'

# 加载数据
with open(data_path, 'r', encoding='utf-8') as f:
    game_data = json.load(f)

# 新章节数据
new_chapters = [
    {
        "chapter_id": "chapter_041",
        "chapter_name": "第四十一章：增气散",
        "description": "萧宁心怀嫉妒，服用丹药挑战萧炎。",
        "scenes": [
            {
                "scene_id": "scene_041_001",
                "scene_name": "萧宁的挑战",
                "location": "成人仪式高台",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_041_001",
                            "type": "narration",
                            "content": "测试结束后是挑战环节。本以为无人敢上，萧宁却在萧玉的默许下，吞下一枚绿色丹药，跃上台来。",
                            "next": "node_041_002"
                        },
                        {
                            "node_id": "node_041_002",
                            "type": "dialogue",
                            "speaker": "萧宁",
                            "content": "萧炎，别以为等级高就了不起。实战，才是检验实力的唯一标准！我要挑战你！",
                            "next": "node_041_003"
                        },
                        {
                            "node_id": "node_041_003",
                            "type": "choice",
                            "description": "看着气息诡异暴涨的萧宁，你的回应是？",
                            "choices": [
                                {
                                    "id": "choice_041_001",
                                    "text": "【平淡】如你所愿。",
                                    "effects": {"charisma": 2},
                                    "next": "node_042_001"
                                },
                                {
                                    "id": "choice_041_002",
                                    "text": "【警觉】服用了丹药么？真是不知廉耻。",
                                    "effects": {"intelligence": 5},
                                    "next": "node_042_001"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_042",
        "chapter_name": "第四十二章：你输了",
        "description": "萧炎展示玄阶斗技，震撼全场。",
        "scenes": [
            {
                "scene_id": "scene_042_001",
                "scene_name": "玄阶斗技之威",
                "location": "战斗高台",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_042_001",
                            "type": "narration",
                            "content": "战斗开始，萧宁如疯虎般扑来。你摊开手掌，掌心凹陷，一股强横的吸力陡然爆发：吸掌！",
                            "next": "node_042_002"
                        },
                        {
                            "node_id": "node_042_002",
                            "type": "narration",
                            "content": "萧宁一个重心不稳被拉了过来。紧接着，你反手一掌：吹火掌！狂猛的推力直接将他轰退数步。",
                            "next": "node_042_003"
                        },
                        {
                            "node_id": "node_042_003",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "你，输了。",
                            "next": "chapter_043"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_043",
        "chapter_name": "第四十三章：强横的萧炎",
        "description": "面对偷袭，展现恐怖实力。",
        "scenes": [
            {
                "scene_id": "scene_043_001",
                "scene_name": "最后的疯狂",
                "location": "高台边缘",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_043_001",
                            "type": "narration",
                            "content": "萧宁并未认输，反而面带狰狞，借着增气散最后的药力发动了狠辣的偷袭：'小混蛋，去死！'",
                            "next": "node_043_002"
                        },
                        {
                            "node_id": "node_043_002",
                            "type": "narration",
                            "content": "你眼神一冷，不再留手。体内的斗之气在此刻顺着奇异的脉络疯狂运转。八极崩！",
                            "next": "node_043_003"
                        },
                        {
                            "node_id": "node_043_003",
                            "type": "narration",
                            "content": "轰！双拳对撞，骨裂声清晰可闻。萧宁整个人如炮弹般飞出高台，重重摔在地上，昏死过去。",
                            "next": "chapter_044",
                            "effects": {"strength": 5}
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_044",
        "chapter_name": "第四十四章：陪你试试",
        "description": "萧玉的刁难与薰儿的回护。",
        "scenes": [
            {
                "scene_id": "scene_044_001",
                "scene_name": "薰儿的温柔",
                "location": "高台之上",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_044_001",
                            "type": "narration",
                            "content": "看到弟弟重伤，萧玉怒不可遏跳上高台。就在你已经脱力、准备强行应对时，一道绿影优雅护在你身前。",
                            "next": "node_044_002"
                        },
                        {
                            "node_id": "node_044_002",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "萧玉表姐，萧炎哥哥已经累了，若真要打，我陪你试试？",
                            "next": "node_044_003"
                        },
                        {
                            "node_id": "node_044_003",
                            "type": "narration",
                            "content": "萧玉看着眼前这位看似温婉、实则深不可测的少女，最终只能恨恨咬牙退场。",
                            "next": "node_044_004"
                        },
                        {
                            "node_id": "node_044_004",
                            "type": "choice",
                            "description": "薰儿如此回护你，你的想法是？",
                            "choices": [
                                {
                                    "id": "choice_044_001",
                                    "text": "【感动】谢谢你，薰儿。",
                                    "effects": {"relationship_xuner": 10},
                                    "next": "chapter_045"
                                },
                                {
                                    "id": "choice_044_002",
                                    "text": "【坚定】下次，我会更强，不再让你站在我面前。",
                                    "effects": {"determination": 10},
                                    "next": "chapter_045"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_045",
        "chapter_name": "第四十五章：落幕",
        "description": "仪式结束，内心的坚持。",
        "scenes": [
            {
                "scene_id": "scene_045_001",
                "scene_name": "夕阳下的谈话",
                "location": "后山小径",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_045_001",
                            "type": "narration",
                            "content": "成人仪式落下帷幕。薰儿突然提出可以给你弄到更高级的功法，这足以让你少走十年弯路。",
                            "next": "node_045_002"
                        },
                        {
                            "node_id": "node_045_002",
                            "type": "choice",
                            "description": "面对这份足以改变命运的馈赠，你会？",
                            "choices": [
                                {
                                    "id": "choice_045_001",
                                    "text": "【拒绝】路，要自己走。功法，我自己能找。",
                                    "effects": {"determination": 10, "intelligence": 5},
                                    "next": "node_045_003"
                                },
                                {
                                    "id": "choice_045_002",
                                    "text": "【婉拒】现在这样，我也能变强。",
                                    "effects": {"relationship_xuner": 2},
                                    "next": "node_045_003"
                                }
                            ]
                        },
                        {
                            "node_id": "node_045_003",
                            "type": "narration",
                            "content": "拒绝了薰儿后，你轻轻摩挲着手上的古老戒指。你明白，自己选择了一条最难，却也最精彩的路。纳兰嫣然，还有两年！",
                            "next": "end_chapter"
                        }
                    ]
                }
            }
        ]
    }
]

# 插入章节
chapters = game_data['story_tree']['chapters']
existing_ids = [ch['chapter_id'] for ch in chapters]
for ch in new_chapters:
    if ch['chapter_id'] not in existing_ids:
        chapters.append(ch)

# 保存
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print(f"成功添加 41-45 章")
