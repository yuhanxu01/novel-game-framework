import json

# 读取现有游戏数据
with open('/home/user/novel-game-framework/frontend/data/game_data_doupo.json', 'r', encoding='utf-8') as f:
    game_data = json.load(f)

# 添加更多章节
additional_chapters = [
    {
        "chapter_id": "chapter_026",
        "chapter_name": "第二十六章：闭关修炼",
        "description": "萧炎进入苦修期，三个月突破到第六段斗之气，掌握八极崩",
        "scenes": [
            {
                "scene_id": "scene_026_001",
                "scene_name": "山中修炼",
                "location": "后山树林",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_026_001",
                            "type": "narration",
                            "content": "三个月的闭关苦修。每天天未亮就起床，在药老的指导下修炼斗之气，然后是挨打训练，锻炼身体硬度。今天，你终于突破到第六段！",
                            "next": "node_026_002",
                            "effects": {"cultivation": 6, "strength": 10}
                        },
                        {
                            "node_id": "node_026_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "不错，三个月从五段到六段，比我预计的快。现在，该试试八极崩了。",
                            "next": "node_026_003"
                        },
                        {
                            "node_id": "node_026_003",
                            "type": "narration",
                            "content": "你站在一棵半米粗的大树前，深吸一口气。体内的斗之气疯狂涌入手肘。",
                            "next": "node_026_004"
                        },
                        {
                            "node_id": "node_026_004",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "八极崩！",
                            "next": "node_026_005"
                        },
                        {
                            "node_id": "node_026_005",
                            "type": "narration",
                            "content": "砰！手肘轰在树干上，木屑四溅，蜘蛛网般的裂纹扩散。大树摇晃几下，轰然倒下！成功了！",
                            "next": "node_026_006",
                            "effects": {"items": ["item_bajibeng"], "strength": 5}
                        },
                        {
                            "node_id": "node_026_006",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "玄阶高级的八极崩，你只用六段斗之气就能发挥出八段的威力。好好练，将来这会是你的杀手锏。",
                            "next": "node_026_007"
                        },
                        {
                            "node_id": "node_026_007",
                            "type": "choice",
                            "description": "你看着自己的成果，想起了什么？",
                            "choices": [
                                {
                                    "id": "choice_026_001",
                                    "text": "【回忆】想起三年前被人嘲笑的场景",
                                    "effects": {"determination": 5},
                                    "next": "node_026_008a"
                                },
                                {
                                    "id": "choice_026_002",
                                    "text": "【展望】想象一年后成人仪式的场景",
                                    "effects": {"determination": 3},
                                    "next": "node_026_008b"
                                },
                                {
                                    "id": "choice_026_003",
                                    "text": "【感激】感谢药老的指导",
                                    "effects": {"relationship_yaolao": 5},
                                    "next": "node_026_008c"
                                }
                            ]
                        },
                        {
                            "node_id": "node_026_008a",
                            "type": "narration",
                            "content": "你想起三年前，那些嘲笑的眼神，那些轻蔑的话语。拳头紧握——我萧炎三年前能创造奇迹，三年后，我依然能！",
                            "next": "node_026_009"
                        },
                        {
                            "node_id": "node_026_008b",
                            "type": "narration",
                            "content": "一年后的成人仪式，当你展现第七段斗之气时，那些人会是什么表情？你很期待那一刻。",
                            "next": "node_026_009"
                        },
                        {
                            "node_id": "node_026_008c",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "老师，谢谢您。没有您，我不可能走到这一步。",
                            "next": "node_026_009"
                        },
                        {
                            "node_id": "node_026_009",
                            "type": "narration",
                            "content": "你对着天空大吼：纳兰嫣然，我正在一步步朝你爬过去！三年之后，云岚宗见！",
                            "next": "end_chapter"
                        }
                    ]
                }
            }
        ]
    }
]

# 添加章节
game_data['story_tree']['chapters'].extend(additional_chapters)

# 保存
with open('/home/user/novel-game-framework/frontend/data/game_data_doupo.json', 'w', encoding='utf-8') as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print(f"✅ 已添加章节")
print(f"✅ 总章节数: {len(game_data['story_tree']['chapters'])}")
print("✅ 游戏数据更新完成！")
