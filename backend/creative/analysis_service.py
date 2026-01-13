import json
from pathlib import Path
from game.models import GameProject, AnalysisCache
from .ai_agent import NovelAnalyzer


class NovelAnalysisService:
    
    CHUNK_SIZE = 3000
    CHUNKS_PER_SUMMARY = 10
    
    def __init__(self, project, api_key, api_provider='deepseek'):
        self.project = project
        self.analyzer = NovelAnalyzer(api_key, api_provider)
        self.novel_content = self._load_novel()
        self.total_chunks = len(self.novel_content) // self.CHUNK_SIZE + 1
    
    def _load_novel(self):
        novel_path = self.project.novel_file.path
        
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(novel_path, 'r', encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        raise ValueError('无法读取小说文件，请检查编码格式')
    
    def _get_chunk(self, index):
        start = index * self.CHUNK_SIZE
        end = start + self.CHUNK_SIZE
        return self.novel_content[start:end]
    
    def _get_accumulated_context(self):
        world_setting = self.project.world_setting or {}
        characters = self.project.characters or {}
        
        recent_caches = AnalysisCache.objects.filter(
            project=self.project
        ).order_by('-chunk_index')[:10]
        
        recent_summaries = []
        for cache in recent_caches:
            result = cache.analysis_result
            if '片段摘要' in result:
                recent_summaries.append(result['片段摘要'].get('核心事件', ''))
        
        return {
            '已识别角色': list(characters.keys()) if characters else [],
            '已知世界观元素': list(world_setting.keys()) if world_setting else [],
            '前文摘要': ' → '.join(reversed(recent_summaries[-5:])),
            '当前剧情阶段': self._determine_stage()
        }
    
    def _determine_stage(self):
        progress = self.project.analysis_progress
        total = self.total_chunks
        
        if progress < total * 0.2:
            return '起'
        elif progress < total * 0.5:
            return '承'
        elif progress < total * 0.8:
            return '转'
        else:
            return '合'
    
    def analyze_next_chunk(self):
        current_index = self.project.analysis_progress
        
        if current_index >= self.total_chunks:
            return {
                'status': 'completed',
                'message': '小说分析已完成'
            }
        
        chunk_content = self._get_chunk(current_index)
        
        if not chunk_content.strip():
            self.project.analysis_progress = current_index + 1
            self.project.save()
            return self.analyze_next_chunk()
        
        accumulated_context = self._get_accumulated_context()
        
        analysis_result = self.analyzer.analyze_chunk(
            current_index,
            chunk_content,
            accumulated_context
        )
        
        AnalysisCache.objects.update_or_create(
            project=self.project,
            chunk_index=current_index,
            defaults={
                'chunk_content': chunk_content[:500],
                'analysis_result': analysis_result
            }
        )
        
        self._update_project_data(analysis_result)
        
        self.project.analysis_progress = current_index + 1
        self.project.save()
        
        if (current_index + 1) % self.CHUNKS_PER_SUMMARY == 0:
            self._generate_chapter_summary(current_index)
        
        return {
            'status': 'processing',
            'current_chunk': current_index + 1,
            'total_chunks': self.total_chunks,
            'progress_percent': round((current_index + 1) / self.total_chunks * 100, 2),
            'analysis_result': analysis_result
        }
    
    def _update_project_data(self, analysis_result):
        if '新发现' in analysis_result:
            new_data = analysis_result['新发现']
            
            if '新角色' in new_data:
                characters = self.project.characters or {}
                for char in new_data['新角色']:
                    char_id = f"char_{len(characters) + 1:03d}"
                    characters[char_id] = {
                        'name': char.get('名称'),
                        'description': char.get('首次描述'),
                        'importance': char.get('重要程度预估'),
                        'relationship': char.get('与主角关系')
                    }
                self.project.characters = characters
            
            if '新设定' in new_data:
                world_setting = self.project.world_setting or {}
                for setting in new_data['新设定']:
                    setting_type = setting.get('类型', '其他')
                    if setting_type not in world_setting:
                        world_setting[setting_type] = []
                    world_setting[setting_type].append(setting.get('内容'))
                self.project.world_setting = world_setting
            
            if '新物品' in new_data:
                items = self.project.items or {'items': []}
                for item in new_data['新物品']:
                    items['items'].append({
                        'item_id': f"item_{len(items['items']) + 1:03d}",
                        'name': item.get('名称'),
                        'description': item.get('描述'),
                        'function': item.get('功能'),
                        'rarity': item.get('稀有度预估')
                    })
                self.project.items = items
            
            if '新地点' in new_data:
                exploration = self.project.exploration or {'areas': []}
                for location in new_data['新地点']:
                    exploration['areas'].append({
                        'area_id': f"area_{len(exploration['areas']) + 1:03d}",
                        'name': location.get('名称'),
                        'description': location.get('描述'),
                        'type': location.get('类型')
                    })
                self.project.exploration = exploration
        
        if '游戏化潜力' in analysis_result:
            potential = analysis_result['游戏化潜力']
            
            if potential.get('可作为选择点'):
                story_tree = self.project.story_tree or {'choice_points': []}
                if 'choice_points' not in story_tree:
                    story_tree['choice_points'] = []
                story_tree['choice_points'].append({
                    'chunk_index': self.project.analysis_progress,
                    'suggestion': potential.get('选择点建议'),
                    'attributes': potential.get('属性相关', [])
                })
                self.project.story_tree = story_tree
        
        self.project.save()
    
    def _generate_chapter_summary(self, end_index):
        start_index = max(0, end_index - self.CHUNKS_PER_SUMMARY + 1)
        
        caches = AnalysisCache.objects.filter(
            project=self.project,
            chunk_index__gte=start_index,
            chunk_index__lte=end_index
        ).order_by('chunk_index')
        
        summaries = []
        for cache in caches:
            result = cache.analysis_result
            if '片段摘要' in result:
                summaries.append(result['片段摘要'])
        
        world_setting = self.project.world_setting or {}
        characters = self.project.characters or {}
        
        new_world_data = self.analyzer.extract_world_setting(
            world_setting,
            summaries
        )
        
        if isinstance(new_world_data, dict) and 'raw_response' not in new_world_data:
            self.project.world_setting = {**world_setting, **new_world_data}
            self.project.save()
    
    def finalize_design(self):
        world_setting = self.project.world_setting or {}
        characters = self.project.characters or {}
        
        caches = AnalysisCache.objects.filter(project=self.project).order_by('chunk_index')
        chapter_summaries = []
        for cache in caches:
            result = cache.analysis_result
            if '片段摘要' in result:
                chapter_summaries.append(result['片段摘要'])
        
        story_design = self.analyzer.design_story(
            world_setting,
            characters,
            chapter_summaries[-100:]
        )
        
        if isinstance(story_design, dict) and 'raw_response' not in story_design:
            self.project.story_tree = story_design
        
        convergence_design = self.analyzer.design_convergence(story_design)
        if isinstance(convergence_design, dict) and 'raw_response' not in convergence_design:
            story_tree = self.project.story_tree or {}
            story_tree['convergence'] = convergence_design
            self.project.story_tree = story_tree
        
        attribute_design = self.analyzer.design_attributes(world_setting, characters)
        if isinstance(attribute_design, dict) and 'raw_response' not in attribute_design:
            self.project.attributes = attribute_design
        
        items = self.project.items or {}
        item_design = self.analyzer.design_items(world_setting, items.get('items', []))
        if isinstance(item_design, dict) and 'raw_response' not in item_design:
            self.project.items = item_design
        
        exploration_design = self.analyzer.design_exploration(world_setting, story_design)
        if isinstance(exploration_design, dict) and 'raw_response' not in exploration_design:
            self.project.exploration = exploration_design
        
        self.project.analysis_status = 'completed'
        self.project.save()
        
        return {
            'status': 'completed',
            'message': '游戏设计已完成',
            'summary': {
                'characters_count': len(characters),
                'world_setting_keys': list(world_setting.keys()),
                'has_story_tree': bool(self.project.story_tree),
                'has_attributes': bool(self.project.attributes),
                'has_items': bool(self.project.items),
                'has_exploration': bool(self.project.exploration)
            }
        }
    
    def get_analysis_summary(self):
        return {
            'project_name': self.project.name,
            'total_chunks': self.total_chunks,
            'analyzed_chunks': self.project.analysis_progress,
            'progress_percent': round(self.project.analysis_progress / self.total_chunks * 100, 2),
            'status': self.project.analysis_status,
            'characters_found': len(self.project.characters or {}),
            'world_setting_categories': list((self.project.world_setting or {}).keys()),
            'choice_points_found': len((self.project.story_tree or {}).get('choice_points', []))
        }
