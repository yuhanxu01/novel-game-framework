import json
import os
import requests
from pathlib import Path


class CreativeAgent:
    
    PROMPT_DIR = Path(__file__).parent.parent.parent / 'prompts'
    
    def __init__(self, api_key, api_provider='deepseek', base_url=None):
        self.api_key = api_key
        self.api_provider = api_provider
        self.base_url = base_url or self._get_default_base_url()
        self.system_prompt = self._load_system_prompt()
        self.conversation_history = []
    
    def _get_default_base_url(self):
        providers = {
            'deepseek': 'https://api.deepseek.com/v1',
            'openai': 'https://api.openai.com/v1',
        }
        return providers.get(self.api_provider, providers['deepseek'])
    
    def _load_system_prompt(self):
        prompt_file = self.PROMPT_DIR / '09-创造模式助手.md'
        if prompt_file.exists():
            return prompt_file.read_text(encoding='utf-8')
        return "你是一个游戏内容创作助手，帮助玩家在创造模式下设计和修改游戏内容。"
    
    def _call_api(self, messages):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat' if self.api_provider == 'deepseek' else 'gpt-4',
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 4000,
        }
        
        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def chat(self, user_message, game_context=None):
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ]
        
        if game_context:
            context_msg = f"""
当前游戏数据上下文：
- 世界观：{json.dumps(game_context.get('world_setting', {}), ensure_ascii=False)[:2000]}
- 角色数量：{len(game_context.get('characters', {}))}
- 章节数量：{len(game_context.get('story_tree', {}).get('chapters', []))}
"""
            messages.append({'role': 'system', 'content': context_msg})
        
        messages.extend(self.conversation_history)
        messages.append({'role': 'user', 'content': user_message})
        
        response = self._call_api(messages)
        
        self.conversation_history.append({'role': 'user', 'content': user_message})
        self.conversation_history.append({'role': 'assistant', 'content': response})
        
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response
    
    def generate_content(self, content_type, requirements, game_context):
        prompt = f"""
请根据以下要求生成游戏内容：

内容类型：{content_type}
具体要求：{requirements}

请以JSON格式输出，确保格式正确可以直接使用。
"""
        return self.chat(prompt, game_context)
    
    def modify_content(self, target_path, modification, game_context):
        prompt = f"""
请修改以下游戏内容：

修改目标：{target_path}
修改要求：{modification}

请输出修改后的JSON数据，以及修改说明。
"""
        return self.chat(prompt, game_context)
    
    def check_consistency(self, new_content, game_context):
        prompt = f"""
请检查以下新内容与现有游戏的一致性：

新内容：{json.dumps(new_content, ensure_ascii=False)}

请检查：
1. 世界观一致性
2. 角色行为一致性
3. 逻辑一致性
4. 数值平衡

输出检查结果和建议。
"""
        return self.chat(prompt, game_context)
    
    def suggest_ideas(self, game_context):
        prompt = """
根据当前游戏内容，请提供一些创意建议：

1. 可以扩展的剧情方向
2. 可以添加的新角色
3. 可以设计的支线任务
4. 可以改进的系统

请以结构化的方式输出建议。
"""
        return self.chat(prompt, game_context)
    
    def clear_history(self):
        self.conversation_history = []


class NovelAnalyzer:
    
    PROMPT_DIR = Path(__file__).parent.parent.parent / 'prompts'
    
    def __init__(self, api_key, api_provider='deepseek', base_url=None):
        self.api_key = api_key
        self.api_provider = api_provider
        self.base_url = base_url or self._get_default_base_url()
        self.prompts = self._load_prompts()
    
    def _get_default_base_url(self):
        providers = {
            'deepseek': 'https://api.deepseek.com/v1',
            'openai': 'https://api.openai.com/v1',
        }
        return providers.get(self.api_provider, providers['deepseek'])
    
    def _load_prompts(self):
        prompts = {}
        prompt_files = [
            ('novel_analyzer', '01-小说分析器.md'),
            ('world_extractor', '02-世界观提取器.md'),
            ('character_analyzer', '03-角色分析器.md'),
            ('story_designer', '04-剧情设计器.md'),
            ('convergence_designer', '05-世界线收束设计.md'),
            ('attribute_designer', '06-属性系统设计.md'),
            ('item_designer', '07-物品道具设计.md'),
            ('exploration_designer', '08-探索系统设计.md'),
        ]
        
        for key, filename in prompt_files:
            file_path = self.PROMPT_DIR / filename
            if file_path.exists():
                prompts[key] = file_path.read_text(encoding='utf-8')
        
        return prompts
    
    def _call_api(self, system_prompt, user_message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat' if self.api_provider == 'deepseek' else 'gpt-4',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            'temperature': 0.3,
            'max_tokens': 4000,
        }
        
        response = requests.post(
            f'{self.base_url}/chat/completions',
            headers=headers,
            json=data,
            timeout=120
        )
        
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    
    def analyze_chunk(self, chunk_index, chunk_content, accumulated_context):
        system_prompt = self.prompts.get('novel_analyzer', '')
        
        user_message = json.dumps({
            '片段序号': chunk_index,
            '片段内容': chunk_content,
            '累积上下文': accumulated_context
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def extract_world_setting(self, current_setting, new_discoveries):
        system_prompt = self.prompts.get('world_extractor', '')
        
        user_message = json.dumps({
            '任务类型': '增量更新',
            '当前世界观': current_setting,
            '新发现的设定': new_discoveries
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def analyze_characters(self, current_characters, new_info):
        system_prompt = self.prompts.get('character_analyzer', '')
        
        user_message = json.dumps({
            '任务类型': '更新角色',
            '当前角色库': current_characters,
            '新角色信息': new_info
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def design_story(self, world_setting, characters, chapter_summaries):
        system_prompt = self.prompts.get('story_designer', '')
        
        user_message = json.dumps({
            '任务类型': '详细设计',
            '世界观': world_setting,
            '角色库': characters,
            '章节总结': chapter_summaries
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def design_convergence(self, story_design):
        system_prompt = self.prompts.get('convergence_designer', '')
        
        user_message = json.dumps({
            '剧情设计': story_design
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def design_attributes(self, world_setting, characters):
        system_prompt = self.prompts.get('attribute_designer', '')
        
        user_message = json.dumps({
            '世界观': world_setting,
            '角色库': characters
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def design_items(self, world_setting, discovered_items):
        system_prompt = self.prompts.get('item_designer', '')
        
        user_message = json.dumps({
            '世界观': world_setting,
            '小说中的物品': discovered_items
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
    
    def design_exploration(self, world_setting, story_design):
        system_prompt = self.prompts.get('exploration_designer', '')
        
        user_message = json.dumps({
            '世界观': world_setting,
            '剧情设计': story_design
        }, ensure_ascii=False)
        
        response = self._call_api(system_prompt, user_message)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {'raw_response': response}
