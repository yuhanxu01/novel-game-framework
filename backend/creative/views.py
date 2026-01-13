import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from game.models import GameProject, AnalysisCache
from .models import CreativeSession, CustomContent, ModificationLog
from .ai_agent import CreativeAgent
from .analysis_service import NovelAnalysisService


@csrf_exempt
@require_http_methods(["POST"])
def start_creative_session(request, project_id):
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        api_provider = data.get('api_provider', 'deepseek')
        
        if not api_key:
            return JsonResponse({'success': False, 'error': '需要提供API Key'}, status=400)
        
        project = GameProject.objects.get(id=project_id)
        
        session = CreativeSession.objects.create(
            project=project,
            api_key=api_key,
            api_provider=api_provider
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'message': '创造模式会话已启动'
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '项目不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def creative_chat(request, session_id):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        
        if not message:
            return JsonResponse({'success': False, 'error': '消息不能为空'}, status=400)
        
        session = CreativeSession.objects.get(id=session_id)
        project = session.project
        
        game_context = {
            'world_setting': project.world_setting,
            'characters': project.characters,
            'story_tree': project.story_tree,
            'attributes': project.attributes,
            'items': project.items,
        }
        
        agent = CreativeAgent(
            api_key=session.api_key,
            api_provider=session.api_provider
        )
        agent.conversation_history = session.conversation_history
        
        response = agent.chat(message, game_context)
        
        session.conversation_history = agent.conversation_history
        session.save()
        
        return JsonResponse({
            'success': True,
            'response': response
        })
    except CreativeSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': '会话不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def generate_content(request, session_id):
    try:
        data = json.loads(request.body)
        content_type = data.get('content_type')
        requirements = data.get('requirements')
        
        session = CreativeSession.objects.get(id=session_id)
        project = session.project
        
        game_context = {
            'world_setting': project.world_setting,
            'characters': project.characters,
            'story_tree': project.story_tree,
        }
        
        agent = CreativeAgent(
            api_key=session.api_key,
            api_provider=session.api_provider
        )
        
        response = agent.generate_content(content_type, requirements, game_context)
        
        return JsonResponse({
            'success': True,
            'generated_content': response
        })
    except CreativeSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': '会话不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def apply_modification(request, session_id):
    try:
        data = json.loads(request.body)
        modification_data = data.get('modification')
        
        session = CreativeSession.objects.get(id=session_id)
        project = session.project
        
        operation_type = modification_data.get('operation_type')
        target_path = modification_data.get('target_path')
        new_value = modification_data.get('new_value')
        
        old_value = get_value_by_path(project, target_path)
        set_value_by_path(project, target_path, new_value)
        project.save()
        
        ModificationLog.objects.create(
            project=project,
            session=session,
            operation_type=operation_type,
            target_path=target_path,
            old_value=old_value,
            new_value=new_value,
            description=modification_data.get('description', '')
        )
        
        return JsonResponse({
            'success': True,
            'message': '修改已应用'
        })
    except CreativeSession.DoesNotExist:
        return JsonResponse({'success': False, 'error': '会话不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def save_custom_content(request, project_id):
    try:
        data = json.loads(request.body)
        
        content, created = CustomContent.objects.update_or_create(
            project_id=project_id,
            content_type=data.get('content_type'),
            content_id=data.get('content_id'),
            defaults={
                'content_data': data.get('content_data', {}),
                'is_active': data.get('is_active', True)
            }
        )
        
        return JsonResponse({
            'success': True,
            'content_id': content.id,
            'created': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_custom_content(request, project_id):
    try:
        content_type = request.GET.get('type')
        
        queryset = CustomContent.objects.filter(project_id=project_id)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        contents = list(queryset.values(
            'id', 'content_type', 'content_id', 'content_data', 'is_active', 'created_at'
        ))
        
        return JsonResponse({
            'success': True,
            'data': contents
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_modification_history(request, project_id):
    try:
        limit = int(request.GET.get('limit', 50))
        logs = ModificationLog.objects.filter(project_id=project_id)[:limit]
        
        history = [{
            'id': log.id,
            'operation_type': log.operation_type,
            'target_path': log.target_path,
            'description': log.description,
            'created_at': log.created_at.isoformat()
        } for log in logs]
        
        return JsonResponse({
            'success': True,
            'data': history
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def revert_modification(request, project_id, log_id):
    try:
        log = ModificationLog.objects.get(id=log_id, project_id=project_id)
        project = log.project
        
        if log.old_value is not None:
            set_value_by_path(project, log.target_path, log.old_value)
            project.save()
        
        ModificationLog.objects.create(
            project=project,
            operation_type='revert',
            target_path=log.target_path,
            old_value=log.new_value,
            new_value=log.old_value,
            description=f'撤销修改: {log.description}'
        )
        
        return JsonResponse({
            'success': True,
            'message': '修改已撤销'
        })
    except ModificationLog.DoesNotExist:
        return JsonResponse({'success': False, 'error': '修改记录不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def upload_novel(request):
    try:
        name = request.POST.get('name', '未命名游戏')
        description = request.POST.get('description', '')
        novel_file = request.FILES.get('novel')
        
        if not novel_file:
            return JsonResponse({'success': False, 'error': '请上传小说文件'}, status=400)
        
        project = GameProject.objects.create(
            name=name,
            description=description,
            novel_file=novel_file,
            analysis_status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'project_id': project.id,
            'message': '小说上传成功，等待分析'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def start_analysis(request, project_id):
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        api_provider = data.get('api_provider', 'deepseek')
        
        if not api_key:
            return JsonResponse({'success': False, 'error': '需要提供API Key'}, status=400)
        
        project = GameProject.objects.get(id=project_id)
        
        service = NovelAnalysisService(project, api_key, api_provider)
        
        project.analysis_status = 'analyzing'
        project.save()
        
        result = service.analyze_next_chunk()
        
        return JsonResponse({
            'success': True,
            'message': '分析任务已启动',
            'result': result
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '项目不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_analysis_progress(request, project_id):
    try:
        project = GameProject.objects.get(id=project_id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'status': project.analysis_status,
                'progress': project.analysis_progress,
            }
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '项目不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def continue_analysis(request, project_id):
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        api_provider = data.get('api_provider', 'deepseek')
        
        project = GameProject.objects.get(id=project_id)
        
        service = NovelAnalysisService(project, api_key, api_provider)
        result = service.analyze_next_chunk()
        
        return JsonResponse({
            'success': True,
            'result': result
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '项目不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def finalize_analysis(request, project_id):
    try:
        data = json.loads(request.body)
        api_key = data.get('api_key')
        api_provider = data.get('api_provider', 'deepseek')
        
        project = GameProject.objects.get(id=project_id)
        
        service = NovelAnalysisService(project, api_key, api_provider)
        result = service.finalize_design()
        
        project.analysis_status = 'completed'
        project.save()
        
        return JsonResponse({
            'success': True,
            'result': result
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '项目不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def get_value_by_path(project, path):
    parts = path.split('.')
    obj = project
    
    for part in parts:
        if hasattr(obj, part):
            obj = getattr(obj, part)
        elif isinstance(obj, dict):
            obj = obj.get(part)
        elif isinstance(obj, list):
            obj = obj[int(part)]
        else:
            return None
    
    return obj


def set_value_by_path(project, path, value):
    parts = path.split('.')
    field_name = parts[0]
    
    if not hasattr(project, field_name):
        return
    
    if len(parts) == 1:
        setattr(project, field_name, value)
        return
    
    obj = getattr(project, field_name)
    
    for part in parts[1:-1]:
        if isinstance(obj, dict):
            if part not in obj:
                obj[part] = {}
            obj = obj[part]
        elif isinstance(obj, list):
            obj = obj[int(part)]
    
    last_part = parts[-1]
    if isinstance(obj, dict):
        obj[last_part] = value
    elif isinstance(obj, list):
        obj[int(last_part)] = value
    
    setattr(project, field_name, getattr(project, field_name))
