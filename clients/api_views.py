from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import ServicePlan, UserGroup
import json

@require_GET
def service_plans(request):
    query = request.GET.get('q', '')
    plans = ServicePlan.objects.filter(name__icontains=query)[:10]
    return JsonResponse([{'id': plan.id, 'name': plan.name} for plan in plans], safe=False)

@csrf_exempt
@require_POST
def create_service_plan(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        plan = ServicePlan.objects.create(name=name)
        return JsonResponse({'id': plan.id, 'name': plan.name})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_GET
def user_groups(request):
    query = request.GET.get('q', '')
    groups = UserGroup.objects.filter(name__icontains=query)[:10]
    return JsonResponse([{'id': group.id, 'name': group.name} for group in groups], safe=False)

@csrf_exempt
@require_POST
def create_user_group(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        group = UserGroup.objects.create(name=name)
        return JsonResponse({'id': group.id, 'name': group.name})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)