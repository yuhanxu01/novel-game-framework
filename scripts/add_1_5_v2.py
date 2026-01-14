import json
import os

def generate_chapters_1_5():
    chapters = []
    
    # Chapter 01
    chapters.append({
        "chapter_id": "chapter_001",
        "chapter_name": "第一章：陨落的天才",
        "description": "曾被誉为天才的少年萧炎，在测试中仅展示出斗之气三段，沦为全族的笑柄。",
        "scenes": [
            {
                "scene_id": "scene_001_001",
                "scene_name": "魔石碑测试",
                "content": {
                    "nodes": [
                        { "节点ID": "node_01_01", "节点类型": "旁白", "内容": "“斗之气，三段！”\n望着魔石碑之上闪亮得甚至有些刺眼的五个大字，少年面无表情，唇角带着一抹自嘲。", "下一节点": "node_01_02" },
                        { "节点ID": "node_01_02", "节点类型": "旁白", "内容": "周围，传来一阵阵整齐的嘲笑和讥讽。曾经的天才，如今的废物。", "下一节点": "node_01_03" },
                        { "节点ID": "node_01_03", "节点类型": "选择", "选择描述": "面对族人的嘲弄，你会如何应对？", "选项": [
                            { "选项ID": "opt_01_01", "选项文本": "【隐忍】面无表情地走下台", "效果": { "determination": 2 }, "导向": "node_01_04" },
                            { "选项ID": "opt_01_02", "选项文本": "【愤怒】紧握拳头，暗暗立誓", "效果": { "determination": 5 }, "导向": "node_01_04" }
                        ]},
                        { "节点ID": "node_01_04", "节点类型": "对话", "角色": "char_xuner", "内容": "萧炎哥哥，以前的你，可是很有自信的哦。", "下一节点": "node_01_05" },
                        { "节点ID": "node_01_05", "节点类型": "对话", "角色": "char_xiaoyan", "内容": "自信？那也是需要实力来支撑的，现在的我，还有什么资格拥有那东西？", "下一节点": "node_01_06" },
                        { "节点ID": "node_01_06", "节点类型": "对话", "角色": "char_xuner", "内容": "我相信，总有一天，那个意气风发的萧炎哥哥会回来的。", "下一节点": "node_01_07" },
                        { "节点ID": "node_01_07", "节点类型": "旁白", "内容": "薰儿温柔的目光中透着不容置疑的信任，让你原本冰凉的心稍稍回暖。" }
                    ]
                }
            }
        ]
    })

    # Chapter 02-04: The Humiliation (Simplified for this version)
    chapters.append({
        "chapter_id": "chapter_002",
        "chapter_name": "第二章：纳兰嫣然",
        "description": "云岚宗娇女纳兰嫣然上门，气氛紧张诡异。",
        "scenes": [{
            "scene_id": "scene_002_001", "scene_name": "大厅会见",
            "content": { "nodes": [
                { "节点ID": "node_02_01", "节点类型": "旁白", "内容": "萧家大厅内，三位长老正陪着几位尊贵的客人。其中一名少女，容貌娇美，正是云岚宗的纳兰嫣然。", "下一节点": "node_02_02" },
                { "节点ID": "node_02_02", "节点类型": "对话", "角色": "char_xiaozhan", "内容": "葛叶先生，不知此行，所为何事？", "下一节点": "node_02_03" },
                { "节点ID": "node_02_03", "节点类型": "对话", "角色": "char_geye", "内容": "呵呵，萧族长。实不相瞒，此番前来，是为嫣然小姐的婚事。", "下一节点": "node_02_04" },
                { "节点ID": "node_02_04", "节点类型": "选择", "选择描述": "察觉到不妙的气氛，你打算？", "选项": [
                    { "选项ID": "opt_02_01", "选项文本": "保持冷静，静观其变", "效果": { "intelligence": 2 }, "导向": "node_02_05" },
                    { "选项ID": "opt_02_02", "选项文本": "紧盯着纳兰嫣然", "效果": { "determination": 2 }, "导向": "node_02_05" }
                ]},
                { "节点ID": "node_02_05", "节点类型": "旁白", "内容": "纳兰嫣然虽然低着头，但眉宇间的傲气却掩盖不住。她似乎已经迫不及待要开口了。" }
            ]}
        }]
    })

    chapters.append({
        "chapter_id": "chapter_003",
        "chapter_name": "第三章：退婚之辱",
        "description": "纳兰嫣然正式提出退婚，并以聚气散作为补偿，这对萧家是莫大的羞辱。",
        "scenes": [{
            "scene_id": "scene_003_001", "scene_name": "羞辱现场",
            "content": { "nodes": [
                { "节点ID": "node_03_01", "节点类型": "对话", "角色": "char_geye", "内容": "云岚宗愿意拿出一枚‘聚气散’，以及三名名额入云岚宗，作为补偿。只求萧家能解除这份婚约。", "下一节点": "node_03_02" },
                { "节点ID": "node_03_02", "节点类型": "旁白", "内容": "大厅内，气氛瞬间凝固。萧战族长的脸色由于过度愤怒而变得通红，甚至有斗气外泄的迹象。", "下一节点": "node_03_03" },
                { "节点ID": "node_03_03", "节点类型": "选择", "选择描述": "纳兰嫣然的行为践踏了家族尊严，你决定：", "选项": [
                    { "选项ID": "opt_03_01", "选项文本": "【愤怒】怒斥对方欺人太甚", "效果": { "determination": 10, "reputation": 5 }, "导向": "node_03_04" },
                    { "选项ID": "opt_03_02", "选项文本": "【冷讽】讥笑云岚宗的‘大方’", "效果": { "intelligence": 5, "determination": 5 }, "导向": "node_03_04" }
                ]},
                { "节点ID": "node_03_04", "节点类型": "旁白", "内容": "你的声音清脆有力，在大厅内回荡。三位长老虽然眼热聚气散，但在这种大义面前，也不敢公然支持退婚。" }
            ]}
        }]
    })

    chapters.append({
        "chapter_id": "chapter_004",
        "chapter_name": "第四章：三十年河东",
        "description": "萧炎写下休书，并立下三年之约。",
        "scenes": [{
            "scene_id": "scene_004_001", "scene_name": "契约达成",
            "content": { "nodes": [
                { "节点ID": "node_04_01", "节点类型": "对话", "角色": "char_xiaoyan", "内容": "纳兰嫣然，你不需要在这里展示你的高傲。今日，不是你纳兰嫣然要退婚，而是我萧炎——休了你！", "下一节点": "node_04_02" },
                { "节点ID": "node_04_02", "节点类型": "旁白", "内容": "萧炎挥毫泼墨，一份休书瞬间落成。他将其狠狠掷在纳兰嫣然面前。", "下一节点": "node_04_03" },
                { "节点ID": "node_04_03", "节点类型": "对话", "角色": "char_xiaoyan", "内容": "三十年河东，三十年河西，莫欺少年穷！三年之后，我会上云岚宗，找回今日的尊严！", "下一节点": "node_04_04" },
                { "节点ID": "node_04_04", "节点类型": "选择", "选择描述": "面对你的决裂，纳兰嫣然恼羞成怒，你最后的话是？", "选项": [
                    { "选项ID": "opt_04_01", "选项文本": "“滚吧，萧家不欢迎你！”", "效果": { "determination": 5 }, "导向": "node_04_05" },
                    { "选项ID": "opt_04_02", "选项文本": "“三年后，云岚宗见。”", "效果": { "reputation": 5 }, "导向": "node_04_05" }
                ]},
                { "节点ID": "node_04_05", "节点类型": "旁白", "内容": "云岚宗一行人灰溜溜地离开。萧战欣慰地看着你，但也为三年后的约定感到忧心忡忡。" }
            ]}
        }]
    })

    chapters.append({
        "chapter_id": "chapter_005",
        "chapter_name": "第五章：戒指里的老头",
        "description": "药老苏醒，改变萧炎一生的时刻到了。",
        "scenes": [{
            "scene_id": "scene_005_001", "scene_name": "后山奇遇",
            "content": { "nodes": [
                { "节点ID": "node_05_01", "节点类型": "旁白", "内容": "深夜，后山。你正在疯狂修炼，却发现斗之气再次消失在戒指中。", "下一节点": "node_05_02" },
                { "节点ID": "node_05_02", "节点类型": "旁白", "内容": "“呵呵，小家伙，看你挺努力的，老头子我都有些不好意思吸了。”一个苍老的声音突然响起。", "下一节点": "node_05_03" },
                { "节点ID": "node_05_03", "节点类型": "选择", "选择描述": "面对突然出现的灵魂体，你的反应是？", "选项": [
                    { "选项ID": "opt_05_01", "选项文本": "【惊恐】你是人是鬼？", "效果": { "intelligence": 1 }, "导向": "node_05_04" },
                    { "选项ID": "opt_05_02", "选项文本": "【愤怒】是你吸走了我的斗气？", "效果": { "determination": 5 }, "导向": "node_05_04" }
                ]},
                { "节点ID": "node_05_04", "节点类型": "对话", "角色": "char_yaolao", "内容": "老夫药尘。小家伙，这三年辛苦你了。拜我为师，我能让你成为最强大的炼药师。", "下一节点": "node_05_05" },
                { "节点ID": "node_05_05", "节点类型": "旁白", "内容": "这一刻，你意识到，逆天改命的机会就在眼前。" }
            ]}
        }]
    })
    
    return chapters

def update_game_data():
    file_path = 'frontend/data/game_data_doupo.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    new_chapters = generate_chapters_1_5()
    
    # Prepend new chapters and reorder
    existing_chapters = data.get('story_tree', {}).get('chapters', [])
    data['story_tree']['chapters'] = new_chapters + existing_chapters
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    update_game_data()
    print("Successfully added Chapters 1-5 to game_data_doupo.json")
