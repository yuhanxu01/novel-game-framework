import json
import re
from pathlib import Path
from typing import Generator
from .ai_agent import NovelAnalyzer
from game.models import GameProject, AnalysisCache


class NovelProcessor:
    
    CHUNK_SIZE = 3000
    SUMMARY_INTERVAL = 10
    VOLUME_INTERVAL = 100
    
    def __init__(self, project: GameProject, api_key: str, api_provider: str = 'deepseek'):
        self.project = project
        self.analyzer = NovelAnalyzer(api_key, api_provider)
        
        self.accumulated_context = {
            '已识别角色': [],
            '已知世界观元素': [],
            '前文摘要': '',
            '当前剧情阶段': '起',
            '片段摘要列表': [],
            '章节总结列表': [],
            '卷总结列表': [],
            '发现的物品': [],
            '发现的地点': [],
            '发现的设定': [],
        }
        
        self.world_setting = {}
        self.characters = {}
        self.story_summaries = []
        self.discovered_items = []
        self.discovered_locations = []
    
    def read_novel(self) -> Generator[tuple[int, str], None, None]:
        novel_path = self.project.novel_file.path
        
        with open(novel_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'\s+', ' ', content)
        
        total_chars = len(content)
        chunk_index = 0
        
        for i in range(0, total_chars, self.CHUNK_SIZE):
            chunk = content[i:i + self.CHUNK_SIZE]
            yield chunk_index, chunk
            chunk_index += 1
    
        return (len(content) + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE
    
    def read_novel_by_chapters(self) -> Generator[tuple[int, str], None, None]:
        novel_path = self.project.novel_file.path
        with open(novel_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex to find chapter headers like "第X章" or "第X回"
        # We capture the header and the content until the next header
        pattern = re.compile(r'(第[0-9零一二三四五六七八九十百千]+[章回][^\n]*)')
        
        parts = pattern.split(content)
        # parts[0] is pre-chapter content (intro/preface)
        # parts[1] is header1, parts[2] is content1, parts[3] is header2, parts[4] is content2...
        
        chunk_index = 0
        
        # Handle preface if exists
        if parts[0].strip():
             yield chunk_index, parts[0]
             chunk_index += 1
             
        for i in range(1, len(parts), 2):
            header = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ""
            full_chapter = header + body
            
            # If chapter is too huge, we might still want to split it? 
            # For now, let's treat the Chapter as the basic unit as requested.
            yield chunk_index, full_chapter
            chunk_index += 1

    def get_total_chapters(self) -> int:
        novel_path = self.project.novel_file.path
        with open(novel_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = re.compile(r'(第[0-9零一二三四五六七八九十百千]+[章回])')
        return len(pattern.findall(content))

    
    def process_chunk(self, chunk_index: int, chunk_content: str) -> dict:
        cached = AnalysisCache.objects.filter(
            project=self.project,
            chunk_index=chunk_index
        ).first()
        
        if cached:
            return cached.analysis_result
        
        result = self.analyzer.analyze_chunk(
            chunk_index,
            chunk_content,
            self.accumulated_context
        )
        
        AnalysisCache.objects.create(
            project=self.project,
            chunk_index=chunk_index,
            chunk_content=chunk_content,
            analysis_result=result
        )
        
        self._update_accumulated_context(result)
        
        return result
    
    def _update_accumulated_context(self, analysis_result: dict):
        if '新发现' in analysis_result:
            new_discovery = analysis_result['新发现']
            
            if '新角色' in new_discovery:
                for char in new_discovery['新角色']:
                    if char.get('名称') and char['名称'] not in self.accumulated_context['已识别角色']:
                        self.accumulated_context['已识别角色'].append(char['名称'])
            
            if '新地点' in new_discovery:
                self.discovered_locations.extend(new_discovery['新地点'])
            
            if '新设定' in new_discovery:
                for setting in new_discovery['新设定']:
                    if setting.get('内容'):
                        self.accumulated_context['已知世界观元素'].append(setting['内容'][:100])
                self.accumulated_context['发现的设定'].extend(new_discovery['新设定'])
            
            if '新物品' in new_discovery:
                self.discovered_items.extend(new_discovery['新物品'])
        
        if '片段摘要' in analysis_result:
            summary = analysis_result['片段摘要']
            self.accumulated_context['片段摘要列表'].append(summary)
            
            if len(self.accumulated_context['片段摘要列表']) > 10:
                self.accumulated_context['片段摘要列表'] = self.accumulated_context['片段摘要列表'][-10:]
            
            recent_summaries = [s.get('核心事件', '') for s in self.accumulated_context['片段摘要列表'][-5:]]
            self.accumulated_context['前文摘要'] = '；'.join(recent_summaries)
    
    def generate_chapter_summary(self, chunk_index: int) -> dict:
        recent_chunks = self.accumulated_context['片段摘要列表'][-self.SUMMARY_INTERVAL:]
        
        summary_text = '\n'.join([
            f"片段{i+1}: {s.get('核心事件', '')} - {s.get('详细描述', '')[:100]}"
            for i, s in enumerate(recent_chunks)
        ])
        
        chapter_summary = {
            '章节序号': chunk_index // self.SUMMARY_INTERVAL,
            '片段范围': f'{chunk_index - self.SUMMARY_INTERVAL + 1} - {chunk_index}',
            '内容概要': summary_text,
            '重要事件': [s.get('核心事件') for s in recent_chunks if s.get('剧情重要性') in ['核心剧情', '高潮']],
        }
        
        self.accumulated_context['章节总结列表'].append(chapter_summary)
        self.story_summaries.append(chapter_summary)
        
        return chapter_summary
    
    def update_world_setting(self, chunk_index: int):
        new_discoveries = self.accumulated_context['发现的设定'][-20:]
        
        if new_discoveries:
            result = self.analyzer.extract_world_setting(
                self.world_setting,
                new_discoveries
            )
            
            if isinstance(result, dict) and 'raw_response' not in result:
                self._merge_world_setting(result)
    
    def _merge_world_setting(self, new_setting: dict):
        for key, value in new_setting.items():
            if key not in self.world_setting:
                self.world_setting[key] = value
            elif isinstance(value, dict) and isinstance(self.world_setting[key], dict):
                self.world_setting[key].update(value)
            elif isinstance(value, list) and isinstance(self.world_setting[key], list):
                existing = {json.dumps(item, ensure_ascii=False) for item in self.world_setting[key]}
                for item in value:
                    if json.dumps(item, ensure_ascii=False) not in existing:
                        self.world_setting[key].append(item)
    
    def update_characters(self, chunk_index: int):
        recent_char_info = []
        for summary in self.accumulated_context['片段摘要列表'][-10:]:
            if '角色动态' in summary:
                recent_char_info.extend(summary['角色动态'])
        
        if recent_char_info:
            result = self.analyzer.analyze_characters(
                self.characters,
                recent_char_info
            )
            
            if isinstance(result, dict) and 'raw_response' not in result:
                self.characters.update(result)
    
    def generate_volume_summary(self, chunk_index: int) -> dict:
        recent_chapters = self.accumulated_context['章节总结列表'][-10:]
        
        volume_summary = {
            '卷序号': chunk_index // (self.SUMMARY_INTERVAL * self.VOLUME_INTERVAL),
            '章节范围': f'{len(self.accumulated_context["卷总结列表"]) * 10 + 1} - {len(self.accumulated_context["章节总结列表"])}',
            '主要剧情': [ch.get('内容概要', '')[:200] for ch in recent_chapters],
        }
        
        self.accumulated_context['卷总结列表'].append(volume_summary)
        
        return volume_summary
    
    def finalize_game_design(self) -> dict:
        story_design = self.analyzer.design_story(
            self.world_setting,
            self.characters,
            self.story_summaries
        )
        
        convergence = self.analyzer.design_convergence(story_design)
        
        attributes = self.analyzer.design_attributes(
            self.world_setting,
            self.characters
        )
        
        items = self.analyzer.design_items(
            self.world_setting,
            self.discovered_items
        )
        
        exploration = self.analyzer.design_exploration(
            self.world_setting,
            story_design
        )
        
        return {
            'world_setting': self.world_setting,
            'characters': self.characters,
            'story_tree': story_design,
            'convergence': convergence,
            'attributes': attributes,
            'items': items,
            'exploration': exploration,
        }
    
    def run_full_analysis(self, progress_callback=None, stop_after_chapter=False, chapter_mode=False):
        total_chunks = self.get_total_chapters() if chapter_mode else self.get_total_chunks()
        
        self.project.analysis_status = 'processing'
        self.project.save()
        
        try:
            reader = self.read_novel_by_chapters() if chapter_mode else self.read_novel()
            
            for chunk_index, chunk_content in reader:
                result = self.process_chunk(chunk_index, chunk_content)
                
                # In chapter mode, every chunk IS a chapter
                is_chapter_end = True if chapter_mode else ((chunk_index + 1) % self.SUMMARY_INTERVAL == 0)
                
                if is_chapter_end:
                    self.generate_chapter_summary(chunk_index)
                    self.update_world_setting(chunk_index)
                    self.update_characters(chunk_index)
                
                if (chunk_index + 1) % (self.SUMMARY_INTERVAL * self.VOLUME_INTERVAL) == 0:
                    self.generate_volume_summary(chunk_index)
                
                progress = int((chunk_index + 1) / total_chunks * 100) if total_chunks > 0 else 0
                self.project.analysis_progress = progress
                self.project.save()
                
                if progress_callback:
                    progress_callback(progress, chunk_index, total_chunks)
                    
                # Interactive Mode: Stop after chapter summary
                # In chapter mode, stop after every chunk (since it's a chapter)
                # In normal mode, stop after SUMMARY_INTERVAL
                should_stop = stop_after_chapter and is_chapter_end
                
                if should_stop:
                    self.project.analysis_status = 'paused'
                    self.project.save()
                    return {
                        'status': 'paused', 
                        'message': f'Paused after Chapter {chunk_index + 1 if chapter_mode else chunk_index // self.SUMMARY_INTERVAL}',
                        'next_chunk_index': chunk_index + 1
                    }

            final_design = self.finalize_game_design()
            
            self.project.world_setting = final_design['world_setting']
            self.project.characters = final_design['characters']
            self.project.story_tree = final_design['story_tree']
            self.project.attributes = final_design['attributes']
            self.project.items = final_design['items']
            self.project.exploration = final_design['exploration']
            self.project.analysis_status = 'completed'
            self.project.analysis_progress = 100
            self.project.save()
            
            return final_design
            
        except Exception as e:
            self.project.analysis_status = 'failed'
            self.project.save()
            raise e
    
    def resume_analysis(self, progress_callback=None, stop_after_chapter=False, chapter_mode=False):
        last_cache = AnalysisCache.objects.filter(
            project=self.project
        ).order_by('-chunk_index').first()
        
        start_index = last_cache.chunk_index + 1 if last_cache else 0
        
        # Populate context from cache logic...
        for i in range(start_index):
            cached = AnalysisCache.objects.filter(
                project=self.project,
                chunk_index=i
            ).first()
            if cached:
                self._update_accumulated_context(cached.analysis_result)
        
        total_chunks = self.get_total_chapters() if chapter_mode else self.get_total_chunks()
        reader = self.read_novel_by_chapters() if chapter_mode else self.read_novel()
        
        for chunk_index, chunk_content in reader:
            if chunk_index < start_index:
                continue
            
            result = self.process_chunk(chunk_index, chunk_content)
            
            is_chapter_end = True if chapter_mode else ((chunk_index + 1) % self.SUMMARY_INTERVAL == 0)
            
            if is_chapter_end:
                self.generate_chapter_summary(chunk_index)
                self.update_world_setting(chunk_index)
                self.update_characters(chunk_index)
            
            progress = int((chunk_index + 1) / total_chunks * 100) if total_chunks > 0 else 0
            self.project.analysis_progress = progress
            self.project.save()
            
            if progress_callback:
                progress_callback(progress, chunk_index, total_chunks)

            # Interactive Mode: Stop after chapter summary
            should_stop = stop_after_chapter and is_chapter_end

            if should_stop:
                self.project.analysis_status = 'paused'
                self.project.save()
                return {
                    'status': 'paused', 
                    'message': f'Paused after Chapter {chunk_index + 1 if chapter_mode else chunk_index // self.SUMMARY_INTERVAL}',
                    'next_chunk_index': chunk_index + 1
                }
        
        return self.finalize_game_design()
