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
        "chapter_id": "chapter_036",
        "chapter_name": "第三十六章：滑稽的突破",
        "description": "成人仪式前夕，萧炎在此刻竟以意想不到的方式突破。",
        "scenes": [
            {
                "scene_id": "scene_036_001",
                "scene_name": "梦中的突破",
                "location": "萧炎卧室",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_036_001",
                            "type": "narration",
                            "content": "仪式前两天的夜晚，你在睡梦中竟梦游般跳入木盆。等第二天清醒，你惊讶地发现，那层屏障竟然不见了。",
                            "next": "node_036_002"
                        },
                        {
                            "node_id": "node_036_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "呵呵，看来有些东西是水到渠成。恭喜你，小家伙，已经是第八段了。",
                            "next": "node_036_003"
                        },
                        {
                            "node_id": "node_036_003",
                            "type": "choice",
                            "description": "面对这种'滑稽'的突破方式，你的感想是？",
                            "choices": [
                                {
                                    "id": "choice_036_001",
                                    "text": "【哭笑不得】这突破方式也太随便了吧！",
                                    "effects": {"intelligence": 2},
                                    "next": "node_036_004"
                                },
                                {
                                    "id": "choice_036_002",
                                    "text": "【坚定】不管怎样，变强就行！成人仪式，我准备好了。",
                                    "effects": {"determination": 5},
                                    "next": "node_036_004"
                                }
                            ]
                        },
                        {
                            "node_id": "node_036_004",
                            "type": "narration",
                            "content": "第八段斗之气在体内澎湃。你握紧拳头，成人仪式，就让你作为回归的第一步吧！",
                            "next": "chapter_037",
                            "effects": {"cultivation": 8}
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_037",
        "chapter_name": "第三十七章：萧玉",
        "description": "迦南学院的暴力堂姐归来。",
        "scenes": [
            {
                "scene_id": "scene_037_001",
                "scene_name": "长腿堂姐",
                "location": "成人仪式广场",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_037_001",
                            "type": "narration",
                            "content": "人群中，一个身材高挑、长腿惊人的女子引起了你的注意。那是你的堂姐萧玉，刚从迦南学院回来。",
                            "next": "node_037_002"
                        },
                        {
                            "node_id": "node_037_002",
                            "type": "dialogue",
                            "speaker": "萧玉",
                            "content": "萧炎，听说你翻身了？呵，别又是耍什么手段吧。迦南学院出来的我，可不吃这一套。",
                            "next": "node_037_003"
                        },
                        {
                            "node_id": "node_037_003",
                            "type": "choice",
                            "description": "面对这位一直对你抱有成见的刁蛮堂姐，你选择？",
                            "choices": [
                                {
                                    "id": "choice_037_001",
                                    "text": "【反击】你的腿还是这么长，就是脾气没变好。",
                                    "effects": {"charisma": 3, "relationship_xiaonv": -10},
                                    "next": "node_037_004"
                                },
                                {
                                    "id": "choice_037_002",
                                    "text": "【无视】关你屁事。",
                                    "effects": {"intelligence": 2},
                                    "next": "node_037_004"
                                }
                            ]
                        },
                        {
                            "node_id": "node_037_004",
                            "type": "narration",
                            "content": "萧玉气得脸色通红，娇躯微颤。由于萧战的到来，冲突才暂时平息。",
                            "next": "chapter_038"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_038",
        "chapter_name": "第三十八章：这小家伙，不简单呐",
        "description": "初见雅妃，精明女人的评价。",
        "scenes": [
            {
                "scene_id": "scene_038_001",
                "scene_name": "雅妃的关注",
                "location": "贵宾席边缘",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_038_001",
                            "type": "narration",
                            "content": "萧战向你介绍了一位惊艳全场的女子——特米尔拍卖行的雅妃。",
                            "next": "node_038_002"
                        },
                        {
                            "node_id": "node_038_002",
                            "type": "dialogue",
                            "speaker": "char_yafei",
                            "content": "萧炎小弟弟，听说你最近创造了不少奇迹呢。这双眼睛，真不像个孩子该有的成熟。",
                            "next": "node_038_003"
                        },
                        {
                            "node_id": "node_038_003",
                            "type": "choice",
                            "description": "面对雅妃审视的目光，你要如何回应？",
                            "choices": [
                                {
                                    "id": "choice_038_001",
                                    "text": "【腼腆】雅妃小姐过誉了。",
                                    "effects": {"charisma": 5, "relationship_yafei": 5},
                                    "next": "node_038_004"
                                },
                                {
                                    "id": "choice_038_002",
                                    "text": "【成熟】这世界会教人成长的。",
                                    "effects": {"intelligence": 5, "relationship_yafei": 10},
                                    "next": "node_038_004"
                                }
                            ]
                        },
                        {
                            "node_id": "node_038_004",
                            "type": "narration",
                            "content": "雅妃掩唇轻笑，眼神中掠过一抹精光。她心中暗道：这小家伙，不简单呐。",
                            "next": "chapter_039"
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_039",
        "chapter_name": "第三十九章：仪式复测",
        "description": "成人正式仪式的时刻，万众瞩目。",
        "scenes": [
            {
                "scene_id": "scene_039_001",
                "scene_name": "繁琐的仪式",
                "location": "高台之上",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_039_001",
                            "type": "narration",
                            "content": "在经历了一系列繁杂的传统仪式后，终于迎来了最关键的环节——复测。这次是由二长老亲自监控。",
                            "next": "node_039_002"
                        },
                        {
                            "node_id": "node_039_002",
                            "type": "narration",
                            "content": "你缓缓将手放上黑石碑，全场屏息。萧玉在台下瞪大眼睛，她倒要看看你是否真的有七段。",
                            "next": "node_039_003"
                        },
                        {
                            "node_id": "node_039_003",
                            "type": "narration",
                            "content": "嗡！金色的字符在石碑上凝聚，由于实力的突破，字符再次变换：斗之力，八段！",
                            "next": "node_040_001",
                            "effects": {"fame": 20}
                        }
                    ]
                }
            }
        ]
    },
    {
        "chapter_id": "chapter_040",
        "chapter_name": "第四十章：震撼",
        "description": "一年五段，惊世骇俗！",
        "scenes": [
            {
                "scene_id": "scene_040_001",
                "scene_name": "死寂后的爆发",
                "location": "高台之上",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_040_001",
                            "type": "narration",
                            "content": "八段！不再是七段！这意味着你在一年内连跳五级！看台上传来茶杯破碎的声音。",
                            "next": "node_040_002"
                        },
                        {
                            "node_id": "node_040_002",
                            "type": "dialogue",
                            "speaker": "各家代表",
                            "content": "这...这怎么可能！萧家...难不成真要出个斗皇强者？",
                            "next": "node_040_003"
                        },
                        {
                            "node_id": "node_040_003",
                            "type": "narration",
                            "content": "萧战在高台大悦，而萧玉则陷入了思维崩溃。你缓缓走下台，那股来自灵魂深处的淡定，让原本对你敌视的人感到了深深的压力。",
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

print(f"成功添加 36-40 章")
