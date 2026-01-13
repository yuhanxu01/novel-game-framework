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
        "chapter_id": "chapter_031",
        "chapter_name": "第三十一章：一星斗者",
        "description": "薰儿展示出一星斗者的惊人实力，萧炎随后登场测试。",
        "scenes": [
            {
                "scene_id": "scene_031_001",
                "scene_name": "石碑前的震撼",
                "location": "萧家训练场",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_031_001",
                            "type": "narration",
                            "content": "石碑前，薰儿伸出皓腕，由于斗之力的输入，黑石碑强芒乍放！",
                            "next": "node_031_002"
                        },
                        {
                            "node_id": "node_031_002",
                            "type": "dialogue",
                            "speaker": "测验员",
                            "content": "薰儿小姐，一星斗者！",
                            "next": "node_031_003"
                        },
                        {
                            "node_id": "node_031_003",
                            "type": "narration",
                            "content": "全场死寂，十五岁的斗者，这在萧家历史上也是极其罕见的。薰儿下台时，对着你俏皮地眨了眨眼。",
                            "next": "node_031_004"
                        },
                        {
                            "node_id": "node_031_004",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "萧炎哥哥，该你了...",
                            "next": "node_031_005"
                        },
                        {
                            "node_id": "node_031_005",
                            "type": "choice",
                            "description": "轮到你了。曾经的天才与当下的'废物'，这一步决定了太多人的看法。",
                            "choices": [
                                {
                                    "id": "choice_031_001",
                                    "text": "【自信】大步向前，找回属于自己的尊严",
                                    "effects": {"determination": 5, "charisma": 2},
                                    "next": "node_032_001"
                                },
                                {
                                    "id": "choice_031_002",
                                    "text": "【淡然】宠辱不惊，让事实说话",
                                    "effects": {"intelligence": 3},
                                    "next": "node_032_001"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_032",
        "chapter_name": "第三十二章：挑战",
        "description": "萧炎展现七段实力，引发全场地震及萧克的挑战。",
        "scenes": [
            {
                "scene_id": "scene_032_001",
                "scene_name": "七段之光",
                "location": "萧家训练场",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_032_001",
                            "type": "narration",
                            "content": "你的手抵在石碑上。片刻后，强光陡然爆发，五个大字让全场心跳停止：斗之力，七段！",
                            "next": "node_032_002"
                        },
                        {
                            "node_id": "node_032_002",
                            "type": "dialogue",
                            "speaker": "char_xiaozhan",
                            "content": "（激动得捏碎杯子）炎儿...你真的做到了！",
                            "next": "node_032_003"
                        },
                        {
                            "node_id": "node_032_003",
                            "type": "narration",
                            "content": "测验员嗓音颤抖地宣布结果。然而，人群中传来了质疑声，萧克越众而出。",
                            "next": "node_032_004"
                        },
                        {
                            "node_id": "node_032_004",
                            "type": "dialogue",
                            "speaker": "萧克",
                            "content": "我不信！一定是假的！萧炎，我要挑战你！",
                            "next": "node_032_005"
                        },
                        {
                            "node_id": "node_032_005",
                            "type": "choice",
                            "description": "面对萧克的质疑，你打算怎么做？",
                            "choices": [
                                {
                                    "id": "choice_032_001",
                                    "text": "【果断】直接应战，用实力打肿他的脸",
                                    "effects": {"determination": 3, "fame": 10},
                                    "next": "node_033_001"
                                },
                                {
                                    "id": "choice_032_002",
                                    "text": "【冷讽】我很像软柿子么？来吧。",
                                    "effects": {"charisma": 2},
                                    "next": "node_033_001"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_033",
        "chapter_name": "第三十三章：证实",
        "description": "萧炎一招击败萧克，彻底证实实力。",
        "scenes": [
            {
                "scene_id": "scene_033_001",
                "scene_name": "实力的碾压",
                "location": "训练场中心",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_033_001",
                            "type": "narration",
                            "content": "萧克施展出'劈山掌'，风声猎猎。你身形微侧，轻描淡写地躲过攻击，反手一记'碎石掌'印在他的肩膀。",
                            "next": "node_033_002"
                        },
                        {
                            "node_id": "node_033_002",
                            "type": "narration",
                            "content": "砰！萧克脸色瞬间惨白，踉跄倒地。全场死寂，这一战，再无质疑。",
                            "next": "node_033_003"
                        },
                        {
                            "node_id": "node_033_003",
                            "type": "dialogue",
                            "speaker": "萧克",
                            "content": "（苦笑拱手）萧炎表弟，你赢了...当初你说的没错，莫欺少年穷。",
                            "next": "chapter_034"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_034",
        "chapter_name": "第三十四章：翻身",
        "description": "萧炎彻底翻身，众人态度大变，萧媚示好遭拒。",
        "scenes": [
            {
                "scene_id": "scene_034_001",
                "scene_name": "态度转换",
                "location": "训练场边缘",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_034_001",
                            "type": "narration",
                            "content": "测试结束，你走向薰儿。曾经那些嘲讽你的眼神，现在都变得敬畏。萧媚竟然也主动凑了上来。",
                            "next": "node_034_002"
                        },
                        {
                            "node_id": "node_034_002",
                            "type": "dialogue",
                            "speaker": "char_xiaomei",
                            "content": "萧炎表哥，明天斗技堂有教导课程，你一起去吗？",
                            "next": "node_034_003"
                        },
                        {
                            "node_id": "node_034_003",
                            "type": "choice",
                            "description": "面对萧媚的变脸式示好，你如何回应？",
                            "choices": [
                                {
                                    "id": "choice_034_001",
                                    "text": "【淡然】拒绝，她太现实了",
                                    "effects": {"relationship_xiaomei": -5, "intelligence": 2},
                                    "next": "node_034_004"
                                },
                                {
                                    "id": "choice_034_002",
                                    "text": "【回护】由薰儿代为回绝",
                                    "effects": {"relationship_xuner": 5, "relationship_xiaomei": -10},
                                    "next": "node_034_005"
                                }
                            ]
                        },
                        {
                            "node_id": "node_034_005",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "不好意思，明天萧炎哥哥要陪我。对吧，哥哥？",
                            "next": "node_034_006"
                        },
                        {
                            "node_id": "node_034_006",
                            "type": "narration",
                            "content": "萧媚尴尬退场。而远处的萧宁，嫉妒得快要发疯了。",
                            "next": "chapter_035"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_035",
        "chapter_name": "第三十五章：罪恶感",
        "description": "小道上的旖旎与内心斗争。",
        "scenes": [
            {
                "scene_id": "scene_035_001",
                "scene_name": "旖旎小道",
                "location": "萧家后山小道",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_035_001",
                            "type": "narration",
                            "content": "薰儿挽着你的手，走在铺满碎石的小路上。手臂上传来的温润触感，让你的思绪有些杂乱。",
                            "next": "node_035_002"
                        },
                        {
                            "node_id": "node_035_002",
                            "type": "choice",
                            "description": "面对这份突如其来的亲昵和内心的'邪念'，你会？",
                            "choices": [
                                {
                                    "id": "choice_035_001",
                                    "text": "【自责】心中暗骂自己，怎么能对妹妹有妄想",
                                    "effects": {"guilt": 10},
                                    "next": "node_035_003"
                                },
                                {
                                    "id": "choice_035_002",
                                    "text": "【享受】感受这一刻的温馨",
                                    "effects": {"relationship_xuner": 5},
                                    "next": "node_035_003"
                                }
                            ]
                        },
                        {
                            "node_id": "node_035_003",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "（脸红）萧炎哥哥，明天...也要陪着我哦。",
                            "next": "node_035_004"
                        },
                        {
                            "node_id": "node_035_004",
                            "type": "narration",
                            "content": "落荒而逃的你回到房间，脑中仍挥之不去她的娇羞。纳兰嫣然...我会变强，为了这份守护！",
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
# 检查是否已存在，避免重复
existing_ids = [ch['chapter_id'] for ch in chapters]
for ch in new_chapters:
    if ch['chapter_id'] not in existing_ids:
        chapters.append(ch)

# 保存
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print(f"成功添加 31-35 章")
