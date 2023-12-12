from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Message
from django.contrib.auth.decorators import login_required
from users.models import MyUser


@login_required
def send_message(request, receiver_id):
    if request.method == 'POST':
        receiver = get_object_or_404(MyUser, id=receiver_id)
        content = request.POST.get('message', '')

        if content:
            message = Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return JsonResponse({'status': 'success', 'message': '私信发送成功'})
        else:
            return JsonResponse({'status': 'error', 'message': '私信内容不能为空'})
    else:
        return JsonResponse({'status': 'error', 'message': '仅接受POST请求'})
