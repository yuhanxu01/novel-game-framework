from django.db import models
from game.models import GameProject


class CreativeSession(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='creative_sessions')
    api_key = models.CharField(max_length=500, verbose_name='API Key')
    api_provider = models.CharField(max_length=50, default='deepseek', verbose_name='API提供商')
    
    conversation_history = models.JSONField(default=list, verbose_name='对话历史')
    pending_changes = models.JSONField(default=list, verbose_name='待应用的修改')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '创造会话'
        verbose_name_plural = verbose_name


class CustomContent(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='custom_contents')
    content_type = models.CharField(max_length=50, verbose_name='内容类型')
    content_id = models.CharField(max_length=100, verbose_name='内容ID')
    content_data = models.JSONField(default=dict, verbose_name='内容数据')
    
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '自定义内容'
        verbose_name_plural = verbose_name
        unique_together = ['project', 'content_type', 'content_id']


class ModificationLog(models.Model):
    project = models.ForeignKey(GameProject, on_delete=models.CASCADE, related_name='modification_logs')
    session = models.ForeignKey(CreativeSession, on_delete=models.SET_NULL, null=True)
    
    operation_type = models.CharField(max_length=50, verbose_name='操作类型')
    target_path = models.CharField(max_length=500, verbose_name='目标路径')
    old_value = models.JSONField(null=True, verbose_name='原值')
    new_value = models.JSONField(null=True, verbose_name='新值')
    
    description = models.TextField(blank=True, verbose_name='修改说明')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = '修改日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
