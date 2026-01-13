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
        "chapter_id": "chapter_046",
        "chapter_name": "第四十六章：暴怒的萧炎",
        "description": "萧玉寻仇，后山的激烈对峙。",
        "scenes": [
            {
                "scene_id": "scene_046_001",
                "scene_name": "后山寻仇",
                "location": "萧家后山",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_046_001",
                            "type": "narration",
                            "content": "你在后山修炼时，萧玉突然杀到。她因弟弟萧宁被打伤而怒火中烧，三星斗者的气息压得你喘不过气。",
                            "next": "node_046_002"
                        },
                        {
                            "node_id": "node_046_002",
                            "type": "dialogue",
                            "speaker": "萧玉",
                            "content": "小混蛋，今天就算萧战叔叔在也救不了你！",
                            "next": "node_046_003"
                        },
                        {
                            "node_id": "node_046_003",
                            "type": "choice",
                            "description": "面对三星斗者的含怒一击，你决定？",
                            "choices": [
                                {
                                    "id": "choice_046_001",
                                    "text": "【反击】利用吸掌制造破绽，出奇制胜",
                                    "effects": {"intelligence": 5, "fame": 5},
                                    "next": "node_047_001"
                                },
                                {
                                    "id": "choice_046_002",
                                    "text": "【忍让】尽量躲避，解释清楚",
                                    "effects": {"charisma": 2},
                                    "next": "node_047_001"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_047",
        "chapter_name": "第四十七章：亵渎",
        "description": "占点便宜，报复这一顿打。",
        "scenes": [
            {
                "scene_id": "scene_047_001",
                "scene_name": "亵渎时刻",
                "location": "乱石堆旁",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_047_001",
                            "type": "narration",
                            "content": "你利用吸掌和推力成功将萧玉压倒。看着她那双傲人的长腿，你心一横，狠狠地摸了一把。",
                            "next": "node_047_002"
                        },
                        {
                            "node_id": "node_047_002",
                            "type": "dialogue",
                            "speaker": "萧玉",
                            "content": "（尖叫）萧炎！我要杀了你！",
                            "next": "node_047_003"
                        },
                        {
                            "node_id": "node_047_003",
                            "type": "narration",
                            "content": "你趁她愣神之际落荒而逃。刚好遇到下山的薰儿，她俏脸似笑非笑地看着你。",
                            "next": "node_047_004"
                        },
                        {
                            "node_id": "node_047_004",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "看来萧炎哥哥刚才...做了什么不得了的事呢。明天可要进斗气阁了，别太分心哦。",
                            "next": "chapter_048"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_048",
        "chapter_name": "第四十八章：斗气阁",
        "description": "萧家秘地，选择最重要的根基。",
        "scenes": [
            {
                "scene_id": "scene_048_001",
                "scene_name": "属性测试",
                "location": "斗气阁门前",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_048_001",
                            "type": "narration",
                            "content": "斗气阁，萧家的根基所在。在众人的注视下，你触摸感应水晶。瞬间，炽热的红色代表了你的火属性。",
                            "next": "node_048_002"
                        },
                        {
                            "node_id": "node_048_002",
                            "type": "narration",
                            "content": "随后薰儿上台，那光芒之盛差点让水晶碎裂。萧战低声告诉你：'去火道第43号房间'。",
                            "next": "chapter_049"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_049",
        "chapter_name": "第四十九章：选择功法",
        "description": "黄阶高级功法，还是更好的选择？",
        "scenes": [
            {
                "scene_id": "scene_049_001",
                "scene_name": "炼火焚",
                "location": "火道深处",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_049_001",
                            "type": "narration",
                            "content": "第43号房间的光幕异常坚固。你深吸一口气，八极崩！在那恐怖的震劲下，光幕轰然破碎。",
                            "next": "node_049_002"
                        },
                        {
                            "node_id": "node_049_002",
                            "type": "narration",
                            "content": "你拿到了黄阶高级功法《炼火焚》。薰儿见状，竟然拿出了一卷玄阶高级的《弄炎决》想要送给你。",
                            "next": "node_049_003"
                        },
                        {
                            "node_id": "node_049_003",
                            "type": "choice",
                            "description": "面对这份重礼，你的坚持是？",
                            "choices": [
                                {
                                    "id": "choice_049_001",
                                    "text": "【拒绝】我能弄到更好的。这份情，我会用实力还。",
                                    "effects": {"determination": 10, "relationship_xuner": 5},
                                    "next": "chapter_050"
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_050",
        "chapter_name": "第五十章：帮？",
        "description": "虽有积怨，但不失底线。",
        "scenes": [
            {
                "scene_id": "scene_050_001",
                "scene_name": "无助的萧媚",
                "location": "风道走廊",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_050_001",
                            "type": "narration",
                            "content": "路过风道，你看到萧媚正焦急得落泪。因为实力不足，她始终无法打破那一层象征前途的光幕。",
                            "next": "node_050_002"
                        },
                        {
                            "node_id": "node_050_002",
                            "type": "choice",
                            "description": "她曾如此势利待你，你会伸出援手吗？",
                            "choices": [
                                {
                                    "id": "choice_050_001",
                                    "text": "【伸手】仅仅因为这一句表哥。我变强，不是为了报复弱者。",
                                    "effects": {"charisma": 10, "relationship_xiaomei": 10},
                                    "next": "node_050_003"
                                },
                                {
                                    "id": "choice_050_002",
                                    "text": "【嘲讽】早知今日，何必当初？",
                                    "effects": {"intelligence": 2, "relationship_xiaomei": -10},
                                    "next": "node_050_003"
                                }
                            ]
                        },
                        {
                            "node_id": "node_050_003",
                            "type": "narration",
                            "content": "（如果你选择帮）你走上前，随手一脚踢碎了光幕，在众人的震撼中冷淡离去，只留下萧媚复杂的眼神。",
                            "next": "chapter_051"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_051",
        "chapter_name": "第五十一章：安心",
        "description": "背后的保障，全心全意的突破。",
        "scenes": [
            {
                "scene_id": "scene_051_001",
                "scene_name": "药老的承诺",
                "location": "萧家演武场后",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_051_001",
                            "type": "narration",
                            "content": "走出斗气阁，萧战满心欢喜。你却在心中暗自焦虑药老的功法是否靠谱。",
                            "next": "node_051_002"
                        },
                        {
                            "node_id": "node_051_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "呵呵，瞧你那没出息的样。玄阶高级算什么？放心，我给你的东西，日后必不比那妮子差。",
                            "next": "node_051_003"
                        },
                        {
                            "node_id": "node_051_003",
                            "type": "narration",
                            "content": "有了这句话，你心中最后一丝顾虑也烟消云散。接下来，就是全速冲击斗者！",
                            "next": "chapter_052"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_052",
        "chapter_name": "第五十二章：燕返击",
        "description": "与薰儿的切磋。",
        "scenes": [
            {
                "scene_id": "scene_052_001",
                "scene_name": "高强度切磋",
                "location": "萧家后山森林",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_052_001",
                            "type": "narration",
                            "content": "森林中，你与薰儿掌风交错。薰儿施展出奇妙的《燕返击》，借力打力，让你吃了不少苦头。",
                            "next": "node_052_002"
                        },
                        {
                            "node_id": "node_052_002",
                            "type": "narration",
                            "content": "战斗后，你脱力倒在草地上，进入了一种奇妙的冥想状态。",
                            "next": "chapter_053"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_053",
        "chapter_name": "第五十三章：第九段",
        "description": "最后的阶梯，金钱的烦恼。",
        "scenes": [
            {
                "scene_id": "scene_053_001",
                "scene_name": "水到渠成",
                "location": "后山森林",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_053_001",
                            "type": "narration",
                            "content": "在沉睡中，天地斗之气源源不断涌入体内。当你醒来时，已经是斗之气第九段！距离斗者，仅一步之遥。",
                            "next": "node_053_002",
                            "effects": {"cultivation": 9}
                        },
                        {
                            "node_id": "node_053_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "想要快速晋升，聚气散必不可少。开单子吧：墨叶莲、二级魔核...总共五万金币。",
                            "next": "node_053_003"
                        },
                        {
                            "node_id": "node_053_003",
                            "type": "choice",
                            "description": "看着空空如也的钱包（仅剩一万），你的对策是？",
                            "choices": [
                                {
                                    "id": "choice_053_001",
                                    "text": "【赚钱】炼制筑基灵液去卖，我可是炼药师！",
                                    "effects": {"intelligence": 5},
                                    "next": "end_chapter"
                                },
                                {
                                    "id": "choice_053_002",
                                    "text": "【无奈】老师，能不能便宜点？",
                                    "effects": {"charisma": 2},
                                    "next": "end_chapter"
                                }
                            ]
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

print(f"成功添加 46-53 章")
