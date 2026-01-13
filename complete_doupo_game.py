import json

# 读取现有游戏数据
with open('/home/user/novel-game-framework/frontend/data/game_data_doupo.json', 'r', encoding='utf-8') as f:
    game_data = json.load(f)

# 添加新角色
game_data['characters']['char_guni'] = {
    "id": "char_guni",
    "name": "谷尼",
    "role": "炼药师",
    "description": "米特尔拍卖行的炼药师，鉴定丹药的专家",
    "personality": "谨慎、专业、敬畏强者",
    "avatar": "中年炼药师"
}

game_data['characters']['char_nalanyanran'] = {
    "id": "char_nalanyanran",
    "name": "纳兰嫣然",
    "role": "退婚者",
    "description": "云岚宗弟子，曾当众退婚萧炎，成为萧炎的动力来源",
    "personality": "高傲、强大、无情",
    "avatar": "白衣少女"
}

game_data['characters']['char_xiaoning'] = {
    "id": "char_xiaoning",
    "name": "萧宁",
    "role": "族人",
    "description": "萧家族人，嫉妒萧炎与薰儿的关系",
    "personality": "嫉妒、傲慢、好胜",
    "avatar": "年轻族人"
}

# 添加新物品
game_data['items']['item_xizh'] = {
    "id": "item_xizh",
    "name": "吸掌",
    "type": "skill",
    "description": "玄阶低级斗技，能吸取对手",
    "rarity": "rare",
    "effect": {"attack_power": 50}
}

game_data['items']['item_chuihuozhang'] = {
    "id": "item_chuihuozhang",
    "name": "吹火掌",
    "type": "skill",
    "description": "玄阶低级斗技，火焰攻击",
    "rarity": "rare",
    "effect": {"attack_power": 60}
}

# 准备添加的章节
new_chapters = [
    # 第24章：领取款项
    {
        "chapter_id": "chapter_024",
        "chapter_name": "第二十四章：神秘炼药师",
        "description": "萧炎伪装成神秘炼药师，与雅妃交涉获取款项",
        "scenes": [
            {
                "scene_id": "scene_024_001",
                "scene_name": "鉴宝室交涉",
                "location": "米特尔拍卖行鉴宝室",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_024_001",
                            "type": "narration",
                            "content": "戴上黑袍，在药老的帮助下，你伪装成一位神秘的炼药师。推开鉴宝室的门，雅妃和一位老者已在等候。",
                            "next": "node_024_002"
                        },
                        {
                            "node_id": "node_024_002",
                            "type": "dialogue",
                            "speaker": "char_yafei",
                            "content": "这位炼药师大人，您来了。您炼制的筑基灵液品质极佳，拍出了四万金币的高价。",
                            "next": "node_024_003"
                        },
                        {
                            "node_id": "node_024_003",
                            "type": "dialogue",
                            "speaker": "char_guni",
                            "content": "（谷尼大师低声）小姐小心，这位炼药师的炼药术...恐怕比我还要高明。",
                            "next": "node_024_004"
                        },
                        {
                            "node_id": "node_024_004",
                            "type": "narration",
                            "content": "雅妃眼神一亮，更加恭敬。她递上一张绿色卡片和一张水晶卡。",
                            "next": "node_024_005"
                        },
                        {
                            "node_id": "node_024_005",
                            "type": "dialogue",
                            "speaker": "char_yafei",
                            "content": "扣除2%的税金，这里是三万九千两百金币。这张水晶卡是我们米特尔家族的贵宾卡，在任何拍卖场都能享受最优惠的税率。",
                            "next": "node_024_006"
                        },
                        {
                            "node_id": "node_024_006",
                            "type": "choice",
                            "description": "雅妃试图套话，你该如何应对？",
                            "choices": [
                                {
                                    "id": "choice_024_001",
                                    "text": "【警觉】保持冷淡，直接拿钱走人",
                                    "condition": {"intelligence": 65},
                                    "effects": {"intelligence": 2, "relationship_yafei": -2},
                                    "next": "node_024_007a"
                                },
                                {
                                    "id": "choice_024_002",
                                    "text": "【礼貌】客气几句，但不透露身份",
                                    "effects": {"charisma": 1, "relationship_yafei": 0},
                                    "next": "node_024_007b"
                                },
                                {
                                    "id": "choice_024_003",
                                    "text": "【试探】反过来打探米特尔家族的信息",
                                    "condition": {"intelligence": 70},
                                    "effects": {"intelligence": 3, "relationship_yafei": 2},
                                    "next": "node_024_007c"
                                }
                            ]
                        },
                        {
                            "node_id": "node_024_007a",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "（通过你的嘴）怎么？来这地方，还得自报身份不成？",
                            "next": "node_024_008"
                        },
                        {
                            "node_id": "node_024_007b",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "（通过你的嘴）多谢，如果日后还有丹药需要拍卖，自然会来找米特尔。",
                            "next": "node_024_008"
                        },
                        {
                            "node_id": "node_024_007c",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "（压低声音）米特尔家族...听说你们势力遍布加玛帝国？",
                            "next": "node_024_007c2"
                        },
                        {
                            "node_id": "node_024_007c2",
                            "type": "dialogue",
                            "speaker": "char_yafei",
                            "content": "（妩媚一笑）大人谬赞了。我们只是做些小生意而已。不过，只要您需要，米特尔的大门永远为您敞开。",
                            "next": "node_024_008"
                        },
                        {
                            "node_id": "node_024_008",
                            "type": "narration",
                            "content": "离开拍卖行，你松了口气。四万金币到手！这些钱，足够你修炼到斗者级别了。",
                            "next": "node_024_009",
                            "effects": {"wealth": 39200, "items": ["item_vip_card"]}
                        },
                        {
                            "node_id": "node_024_009",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "那个女娃子不简单，差点就套出你的身份了。记住，炼药师的身份要慎重暴露。",
                            "next": "chapter_025"
                        }
                    ]
                }
            }
        ]
    },
    # 第25章：钱由我出
    {
        "chapter_id": "chapter_025",
        "chapter_name": "第二十五章：三年之约",
        "description": "萧炎购买药材准备闭关，父亲赠送筑基灵液，萧炎立下三年之约",
        "scenes": [
            {
                "scene_id": "scene_025_001",
                "scene_name": "购买药材",
                "location": "药材店",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_025_001",
                            "type": "narration",
                            "content": "接下来的几天，你低调地购买了大量药材——足够支撑八个月的闭关修炼。",
                            "next": "node_025_002",
                            "effects": {"wealth": -8000}
                        },
                        {
                            "node_id": "node_025_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "有筑基灵液辅助，加上这些药材，一年内突破到第七段不成问题。",
                            "next": "node_025_003"
                        },
                        {
                            "node_id": "node_025_003",
                            "type": "narration",
                            "content": "回到家中，父亲萧战叫住了你。他拿出一个玉瓶——里面正是筑基灵液！",
                            "next": "node_025_004"
                        },
                        {
                            "node_id": "node_025_004",
                            "type": "dialogue",
                            "speaker": "char_xiaozhan",
                            "content": "炎儿，这是父亲托人买的筑基灵液。你好好修炼，萧家的未来...就靠你了。",
                            "next": "node_025_005"
                        },
                        {
                            "node_id": "node_025_005",
                            "type": "narration",
                            "content": "（你心中苦笑——这正是你自己拍卖出去的那瓶！）",
                            "next": "node_025_006"
                        },
                        {
                            "node_id": "node_025_006",
                            "type": "choice",
                            "description": "面对父亲的期望，你该如何回应？",
                            "choices": [
                                {
                                    "id": "choice_025_001",
                                    "text": "【坚定】父亲，我一定不会让您失望！",
                                    "effects": {"determination": 5, "relationship_xiaozhan": 5},
                                    "next": "node_025_007a"
                                },
                                {
                                    "id": "choice_025_002",
                                    "text": "【承诺】三年后，我会去云岚宗，讨回尊严！",
                                    "effects": {"determination": 8, "relationship_xiaozhan": 3},
                                    "next": "node_025_007b"
                                },
                                {
                                    "id": "choice_025_003",
                                    "text": "【温情】父亲，您辛苦了。孩儿会努力的。",
                                    "effects": {"charisma": 2, "relationship_xiaozhan": 8},
                                    "next": "node_025_007c"
                                }
                            ]
                        },
                        {
                            "node_id": "node_025_007a",
                            "type": "dialogue",
                            "speaker": "char_xiaozhan",
                            "content": "好！为父相信你！",
                            "next": "node_025_008"
                        },
                        {
                            "node_id": "node_025_007b",
                            "type": "dialogue",
                            "speaker": "char_xiaozhan",
                            "content": "三年之约...纳兰嫣然那丫头，她会后悔的！",
                            "next": "node_025_008"
                        },
                        {
                            "node_id": "node_025_007c",
                            "type": "dialogue",
                            "speaker": "char_xiaozhan",
                            "content": "（拍拍你的肩膀）炎儿长大了。去吧，好好修炼。",
                            "next": "node_025_008"
                        },
                        {
                            "node_id": "node_025_008",
                            "type": "narration",
                            "content": "你回到房间，却不知道，薰儿正在暗中为父亲支付这笔十万金币的巨款...",
                            "next": "node_025_009"
                        },
                        {
                            "node_id": "node_025_009",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "（薰儿轻声自语）萧炎哥哥，薰儿会一直守护你的...",
                            "next": "chapter_026",
                            "effects": {"relationship_xuner": 10}
                        }
                    ]
                }
            }
        ]
    },
    # 第27章：冲击第七段
    {
        "chapter_id": "chapter_027",
        "chapter_name": "第二十七章：突破瓶颈",
        "description": "又修炼两个月，萧炎突破到第七段斗之气",
        "scenes": [
            {
                "scene_id": "scene_027_001",
                "scene_name": "第七段突破",
                "location": "修炼密室",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_027_001",
                            "type": "narration",
                            "content": "又是两个月的苦修。筑基灵液的药效终于完全吸收，你能感觉到第七段的瓶颈已经松动。",
                            "next": "node_027_002"
                        },
                        {
                            "node_id": "node_027_002",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "就是现在！冲击第七段！",
                            "next": "node_027_003"
                        },
                        {
                            "node_id": "node_027_003",
                            "type": "choice",
                            "description": "突破的关键时刻，你选择什么方式冲关？",
                            "choices": [
                                {
                                    "id": "choice_027_001",
                                    "text": "【稳健】循序渐进，慢慢突破",
                                    "effects": {"cultivation": 7, "strength": 3},
                                    "next": "node_027_004a"
                                },
                                {
                                    "id": "choice_027_002",
                                    "text": "【激进】全力冲击，一鼓作气！",
                                    "condition": {"determination": 8},
                                    "effects": {"cultivation": 7, "strength": 5, "determination": 2},
                                    "next": "node_027_004b"
                                }
                            ]
                        },
                        {
                            "node_id": "node_027_004a",
                            "type": "narration",
                            "content": "你选择稳扎稳打。体内的斗之气缓缓流转，一点点冲击瓶颈。砰！瓶颈破开，第七段！",
                            "next": "node_027_005"
                        },
                        {
                            "node_id": "node_027_004b",
                            "type": "narration",
                            "content": "你调动全身斗之气，如洪流般冲击瓶颈！轰！瓶颈被暴力冲破，第七段！而且根基更加扎实！",
                            "next": "node_027_005"
                        },
                        {
                            "node_id": "node_027_005",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "第七段...斗之气高级！这是成为斗者的第一把钥匙。小家伙，你有资格进入斗气阁了！",
                            "next": "node_027_006"
                        },
                        {
                            "node_id": "node_027_006",
                            "type": "narration",
                            "content": "第七段！从三段到七段，仅用一年！你握紧拳头，感受着体内澎湃的力量。",
                            "next": "node_027_007"
                        },
                        {
                            "node_id": "node_027_007",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "纳兰嫣然...你等着，我会一步步追上你的！",
                            "next": "chapter_028"
                        }
                    ]
                }
            }
        ]
    },
    # 第28章：强化吸掌
    {
        "chapter_id": "chapter_028",
        "chapter_name": "第二十八章：组合斗技",
        "description": "萧炎开发出吸掌+吹火掌的强大组合技",
        "scenes": [
            {
                "scene_id": "scene_028_001",
                "scene_name": "组合技开发",
                "location": "后山训练场",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_028_001",
                            "type": "narration",
                            "content": "突破第七段后，你开始思考如何提升战斗力。单纯的斗技威力有限，但如果能组合使用...",
                            "next": "node_028_002"
                        },
                        {
                            "node_id": "node_028_002",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "老师，吸掌能否和其他斗技配合？",
                            "next": "node_028_003"
                        },
                        {
                            "node_id": "node_028_003",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "哦？有想法了？说说看。",
                            "next": "node_028_004"
                        },
                        {
                            "node_id": "node_028_004",
                            "type": "choice",
                            "description": "你准备如何组合斗技？",
                            "choices": [
                                {
                                    "id": "choice_028_001",
                                    "text": "【创新】吸掌控制，然后近身使用八极崩",
                                    "condition": {"intelligence": 70},
                                    "effects": {"intelligence": 2},
                                    "next": "node_028_005a"
                                },
                                {
                                    "id": "choice_028_002",
                                    "text": "【火焰】吸掌拉近，配合火焰攻击",
                                    "condition": {"intelligence": 65},
                                    "effects": {"intelligence": 3, "items": ["item_chuihuozhang"]},
                                    "next": "node_028_005b"
                                }
                            ]
                        },
                        {
                            "node_id": "node_028_005a",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "思路不错，但八极崩需要蓄力，敌人被吸过来后可能来不及施展。",
                            "next": "node_028_006"
                        },
                        {
                            "node_id": "node_028_005b",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "好！吸掌控制，吹火掌攻击！我这里正好有一门玄阶低级的火系斗技——吹火掌！",
                            "next": "node_028_006"
                        },
                        {
                            "node_id": "node_028_006",
                            "type": "narration",
                            "content": "药老传授你吹火掌。经过几天的练习，你成功掌握了这套组合技——吸掌拉近敌人，吹火掌瞬间打出！",
                            "next": "node_028_007",
                            "effects": {"items": ["item_xizh", "item_chuihuozhang"], "strength": 5}
                        },
                        {
                            "node_id": "node_028_007",
                            "type": "dialogue",
                            "speaker": "char_yaolao",
                            "content": "两个玄阶低级斗技，组合起来威力堪比玄阶中高级！小家伙，你的战斗智慧不错！",
                            "next": "node_028_008"
                        },
                        {
                            "node_id": "node_028_008",
                            "type": "narration",
                            "content": "现在的你，拥有八极崩作为杀手锏，吸掌+吹火掌作为常规攻击手段。第七段斗之气，玄阶高级斗技...是时候参加成人仪式了！",
                            "next": "chapter_029"
                        }
                    ]
                }
            }
        ]
    },
    # 第29章：重要的日子
    {
        "chapter_id": "chapter_029",
        "chapter_name": "第二十九章：成人仪式预测",
        "description": "成人仪式前，萧炎参加预测，展现第七段实力",
        "scenes": [
            {
                "scene_id": "scene_029_001",
                "scene_name": "预测大厅",
                "location": "萧家测试大厅",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_029_001",
                            "type": "narration",
                            "content": "成人仪式前一个月，萧家组织预测。测试大厅里，族中长老们正在记录每个人的斗之气等级。",
                            "next": "node_029_002"
                        },
                        {
                            "node_id": "node_029_002",
                            "type": "narration",
                            "content": "轮到你了。所有人的目光都集中过来——曾经的天才，三年的废物，现在会是什么样？",
                            "next": "node_029_003"
                        },
                        {
                            "node_id": "node_029_003",
                            "type": "choice",
                            "description": "你要如何展现实力？",
                            "choices": [
                                {
                                    "id": "choice_029_001",
                                    "text": "【低调】只展现第五段，隐藏真实实力",
                                    "effects": {"intelligence": 3},
                                    "next": "node_029_004a"
                                },
                                {
                                    "id": "choice_029_002",
                                    "text": "【正常】展现第七段，震撼全场",
                                    "effects": {"charisma": 5, "determination": 3},
                                    "next": "node_029_004b"
                                },
                                {
                                    "id": "choice_029_003",
                                    "text": "【炫耀】不仅展现第七段，还展示斗技",
                                    "condition": {"charisma": 65},
                                    "effects": {"charisma": 8, "determination": 5},
                                    "next": "node_029_004c"
                                }
                            ]
                        },
                        {
                            "node_id": "node_029_004a",
                            "type": "narration",
                            "content": "你只释放出第五段的斗之气。众人微微点头——还算不错，但也不过如此。",
                            "next": "node_029_005"
                        },
                        {
                            "node_id": "node_029_004b",
                            "type": "narration",
                            "content": "你深吸一口气，释放全部斗之气——第七段！测试水晶发出耀眼的光芒！全场哗然！",
                            "next": "node_029_005"
                        },
                        {
                            "node_id": "node_029_004c",
                            "type": "narration",
                            "content": "第七段斗之气爆发！然后，你一掌拍出——八极崩！砰！训练木桩瞬间粉碎！全场鸦雀无声！",
                            "next": "node_029_005"
                        },
                        {
                            "node_id": "node_029_005",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "（薰儿在一旁微笑）萧炎哥哥...真厉害呢。",
                            "next": "node_029_006"
                        },
                        {
                            "node_id": "node_029_006",
                            "type": "narration",
                            "content": "预测结束。长老宣布：第七段以上者，可进入斗气阁选择斗技！你终于有资格进入那个地方了。",
                            "next": "chapter_030"
                        }
                    ]
                }
            }
        ]
    },
    # 第30章：辱人者，人恒辱之
    {
        "chapter_id": "chapter_030",
        "chapter_name": "第三十章：族内冲突",
        "description": "测试场地，萧宁因嫉妒而挑衅萧炎",
        "scenes": [
            {
                "scene_id": "scene_030_001",
                "scene_name": "测试场地",
                "location": "萧家训练场",
                "content": {
                    "nodes": [
                        {
                            "node_id": "node_030_001",
                            "type": "narration",
                            "content": "和薰儿一起走向测试场地。一路上，你注意到一个熟悉的身影——萧宁，你的族兄。",
                            "next": "node_030_002"
                        },
                        {
                            "node_id": "node_030_002",
                            "type": "dialogue",
                            "speaker": "char_xiaoning",
                            "content": "（阴阳怪气）哟，这不是我们的废物少爷吗？听说你最近很努力啊。",
                            "next": "node_030_003"
                        },
                        {
                            "node_id": "node_030_003",
                            "type": "narration",
                            "content": "萧宁的眼神在你和薰儿之间游移，明显充满嫉妒。他一直暗恋薰儿，但薰儿只对你温柔。",
                            "next": "node_030_004"
                        },
                        {
                            "node_id": "node_030_004",
                            "type": "choice",
                            "description": "面对萧宁的挑衅，你选择？",
                            "choices": [
                                {
                                    "id": "choice_030_001",
                                    "text": "【无视】完全不理会，继续前行",
                                    "effects": {"intelligence": 2},
                                    "next": "node_030_005a"
                                },
                                {
                                    "id": "choice_030_002",
                                    "text": "【讽刺】萧宁兄，你的修为...还在第四段吧？",
                                    "condition": {"charisma": 60},
                                    "effects": {"charisma": 3, "relationship_xiaoning": -5},
                                    "next": "node_030_005b"
                                },
                                {
                                    "id": "choice_030_003",
                                    "text": "【平静】同为族人，何必如此？",
                                    "effects": {"charisma": 1, "relationship_xiaoning": -2},
                                    "next": "node_030_005c"
                                }
                            ]
                        },
                        {
                            "node_id": "node_030_005a",
                            "type": "narration",
                            "content": "你牵着薰儿的手，从萧宁身边走过，仿佛他是空气。萧宁脸色铁青，但不敢发作。",
                            "next": "node_030_006"
                        },
                        {
                            "node_id": "node_030_005b",
                            "type": "narration",
                            "content": "萧宁脸色涨红——他确实还在第四段！周围的族人都在偷笑。他狠狠瞪了你一眼，咬牙转身离开。",
                            "next": "node_030_006"
                        },
                        {
                            "node_id": "node_030_005c",
                            "type": "dialogue",
                            "speaker": "char_xiaoning",
                            "content": "（冷笑）族人？等着瞧吧，废物就是废物！",
                            "next": "node_030_006"
                        },
                        {
                            "node_id": "node_030_006",
                            "type": "dialogue",
                            "speaker": "char_xuner",
                            "content": "萧炎哥哥，不用理会他。你现在已经是第七段了，他...还只是第四段呢。",
                            "next": "node_030_007"
                        },
                        {
                            "node_id": "node_030_007",
                            "type": "narration",
                            "content": "你微微一笑。薰儿说得对，何必和蝼蚁计较？你的目标，是云岚宗的纳兰嫣然！",
                            "next": "node_030_008"
                        },
                        {
                            "node_id": "node_030_008",
                            "type": "dialogue",
                            "speaker": "char_xiaoyan",
                            "content": "成人仪式...我会让所有人看到，萧炎，回来了！",
                            "next": "end_chapter"
                        }
                    ]
                }
            }
        ]
    }
]

# 将新章节插入到正确位置（chapter_023之后，chapter_026之前）
chapters = game_data['story_tree']['chapters']
# 找到chapter_026的位置
chapter_026_index = next((i for i, ch in enumerate(chapters) if ch['chapter_id'] == 'chapter_026'), len(chapters))

# 在chapter_026之前插入新章节
for i, new_chapter in enumerate(new_chapters):
    if new_chapter['chapter_id'] in ['chapter_024', 'chapter_025']:
        chapters.insert(chapter_026_index + i, new_chapter)
    else:
        # chapter_027-030插在chapter_026之后
        chapters.append(new_chapter)

# 更新元数据
game_data['meta']['version'] = "2.0.0"
game_data['meta']['description'] = "三年前，天才少年萧炎突然失去修炼天赋。三年后，他获得神秘药老的指导，开始绝地反击。从拍卖会的智慧博弈，到闭关苦修的艰辛历程，从掌握八极崩到突破第七段...这是一段从废材到强者的完整蜕变之路！"

# 保存更新后的游戏数据
with open('/home/user/novel-game-framework/frontend/data/game_data_doupo.json', 'w', encoding='utf-8') as f:
    json.dump(game_data, f, indent=2, ensure_ascii=False)

print(f"✅ 已添加章节 24, 25, 27-30")
print(f"✅ 总章节数: {len(game_data['story_tree']['chapters'])}")
print(f"✅ 章节列表: {[ch['chapter_id'] for ch in game_data['story_tree']['chapters']]}")
print("✅ 完整游戏数据生成完成！现在可以从第23章一直玩到第30章！")
