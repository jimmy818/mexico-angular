from django.http.response import JsonResponse
from django.views.decorators.http import  require_POST
from django.shortcuts import get_object_or_404
from apps.security.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json
from django.conf import settings
from django.shortcuts import render


    
from django.http.response import HttpResponse
from django.views.decorators.http import require_GET

# Create your views here.
@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)
        print(request,data,"DATA")
        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        print(data)
        icon ='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYwLzkS-BfYdwLjwZnQXa7QwfkqM-m9v8WgA&usqp=CAU'
        payload = {'head': data['head'], 'body': data['body'], "icon": data['icon']}
        send_user_notification(user=user, payload=payload, ttl=1000)
        print(icon)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
    
    
@require_GET
def home(request):   
   user = request.user
   return render(request, 'home.html', {user: user})