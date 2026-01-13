import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import GameProject, GameSave, Chapter, Scene, Character, Item


@csrf_exempt
@require_http_methods(["GET"])
def get_game_data(request, project_id):
    try:
        project = GameProject.objects.get(id=project_id)
        return JsonResponse({
            'success': True,
            'data': {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'world_setting': project.world_setting,
                'characters': project.characters,
                'story_tree': project.story_tree,
                'attributes': project.attributes,
                'items': project.items,
                'exploration': project.exploration,
            }
        })
    except GameProject.DoesNotExist:
        return JsonResponse({'success': False, 'error': '游戏项目不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_chapter(request, project_id, chapter_id):
    try:
        chapter = Chapter.objects.get(project_id=project_id, chapter_id=chapter_id)
        return JsonResponse({
            'success': True,
            'data': {
                'chapter_id': chapter.chapter_id,
                'title': chapter.title,
                'content': chapter.content,
                'scenes': list(chapter.scenes.values('scene_id', 'name', 'content', 'order'))
            }
        })
    except Chapter.DoesNotExist:
        return JsonResponse({'success': False, 'error': '章节不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_scene(request, project_id, scene_id):
    try:
        scene = Scene.objects.get(chapter__project_id=project_id, scene_id=scene_id)
        return JsonResponse({
            'success': True,
            'data': {
                'scene_id': scene.scene_id,
                'name': scene.name,
                'location': scene.location,
                'content': scene.content
            }
        })
    except Scene.DoesNotExist:
        return JsonResponse({'success': False, 'error': '场景不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def save_game(request, project_id):
    try:
        data = json.loads(request.body)
        slot = data.get('slot', 0)
        
        save, created = GameSave.objects.update_or_create(
            project_id=project_id,
            slot=slot,
            user=request.user if request.user.is_authenticated else None,
            defaults={
                'save_name': data.get('save_name', f'存档 {slot}'),
                'current_chapter': data.get('current_chapter', ''),
                'current_scene': data.get('current_scene', ''),
                'current_node': data.get('current_node', ''),
                'player_attributes': data.get('attributes', {}),
                'player_inventory': data.get('inventory', []),
                'player_flags': data.get('flags', []),
                'relationship_data': data.get('relationships', {}),
                'exploration_data': data.get('exploration', {}),
                'play_time': data.get('play_time', 0),
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': '存档成功',
            'save_id': save.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def load_game(request, project_id, slot):
    try:
        save = GameSave.objects.get(
            project_id=project_id,
            slot=slot,
            user=request.user if request.user.is_authenticated else None
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'save_name': save.save_name,
                'current_chapter': save.current_chapter,
                'current_scene': save.current_scene,
                'current_node': save.current_node,
                'attributes': save.player_attributes,
                'inventory': save.player_inventory,
                'flags': save.player_flags,
                'relationships': save.relationship_data,
                'exploration': save.exploration_data,
                'play_time': save.play_time,
                'updated_at': save.updated_at.isoformat()
            }
        })
    except GameSave.DoesNotExist:
        return JsonResponse({'success': False, 'error': '存档不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def list_saves(request, project_id):
    saves = GameSave.objects.filter(
        project_id=project_id,
        user=request.user if request.user.is_authenticated else None
    ).values('slot', 'save_name', 'current_chapter', 'play_time', 'updated_at')
    
    return JsonResponse({
        'success': True,
        'data': list(saves)
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_save(request, project_id, slot):
    try:
        GameSave.objects.filter(
            project_id=project_id,
            slot=slot,
            user=request.user if request.user.is_authenticated else None
        ).delete()
        return JsonResponse({'success': True, 'message': '存档已删除'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def list_projects(request):
    projects = GameProject.objects.all().values(
        'id', 'name', 'description', 'analysis_status', 'analysis_progress', 'created_at'
    )
    return JsonResponse({
        'success': True,
        'data': list(projects)
    })


@csrf_exempt
@require_http_methods(["POST"])
def check_condition(request, project_id):
    try:
        data = json.loads(request.body)
        condition = data.get('condition', {})
        player_state = data.get('player_state', {})
        
        result = evaluate_condition(condition, player_state)
        
        return JsonResponse({
            'success': True,
            'result': result
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def evaluate_condition(condition, player_state):
    if not condition:
        return True
    
    attributes = player_state.get('attributes', {})
    inventory = player_state.get('inventory', [])
    flags = player_state.get('flags', [])
    relationships = player_state.get('relationships', {})
    
    if 'needs_attribute' in condition:
        for attr, value in condition['needs_attribute'].items():
            if attributes.get(attr, 0) < value:
                return False
    
    if 'needs_item' in condition:
        for item in condition['needs_item']:
            if item not in inventory:
                return False
    
    if 'needs_flag' in condition:
        for flag in condition['needs_flag']:
            if flag not in flags:
                return False
    
    
    if 'needs_relationship' in condition:
        for char, value in condition['needs_relationship'].items():
            if relationships.get(char, 0) < value:
                return False
    
    return True

