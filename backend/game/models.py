from django.db import models
from django.contrib.auth.models import User
import json


class GameProject(models.Model):
    name = models.CharField(max_length=200, verbose_name='游戏名称')
    description = models.TextField(blank=True, verbose_name='游戏描述')
    novel_file = models.FileField(upload_to='novels/', verbose_name='小说文件')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    world_setting = models.JSONField(default=dict, verbose_name='世界观设定')
    characters = models.JSONField(default=dict, verbose_name='角色数据')
    story_tree = models.JSONField(default=dict, verbose_name='剧情树')
    attributes = models.JSONField(default=dict, verbose_name='属性系统')
    items = models.JSONField(default=dict, verbose_name='物品系统')
    exploration = models.JSONField(default=dict, verbose_name='探索系统')
    
    analysis_progress = models.IntegerField(default=0, verbose_name='分析进度')
    analysis_status = models.CharField(max_length=50, default='pending', verbose_name='分析状态')
    
    class Meta:
        verbose_name = '游戏项目'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.name


class Chapter(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='chapters')
    chapter_id = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    content = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['order']
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Scene(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='scenes')
    scene_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    location = models.CharField(max_length=200, blank=True)
    content = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['order']
        verbose_name = '场景'
        verbose_name_plural = verbose_name


class Character(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='character_models')
    char_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    data = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Item(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='item_models')
    item_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = verbose_name


class GameSave(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='saves')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    slot = models.IntegerField(default=0, verbose_name='存档槽位')
    save_name = models.CharField(max_length=100, verbose_name='存档名称')
    
    current_chapter = models.CharField(max_length=100)
    current_scene = models.CharField(max_length=100)
    current_node = models.CharField(max_length=100)
    
    player_attributes = models.JSONField(default=dict)
    player_inventory = models.JSONField(default=list)
    player_flags = models.JSONField(default=list)
    relationship_data = models.JSONField(default=dict)
    exploration_data = models.JSONField(default=dict)
    
    play_time = models.IntegerField(default=0, verbose_name='游戏时间(秒)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '游戏存档'
        verbose_name_plural = verbose_name
        unique_together = ['project', 'user', 'slot']


class AnalysisCache(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='analysis_cache')
    chunk_index = models.IntegerField()
    chunk_content = models.TextField()
    analysis_result = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '分析缓存'
        verbose_name_plural = verbose_name
        unique_together = ['project', 'chunk_index']
