from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserGetSerializer, ChatSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from chat.models import Chat
import time
# Create your views here.

User = get_user_model()

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 30

@api_view(['GET'])
def get_user_list(request):
    time.sleep(1)
    if request.method == 'GET':
        try:
            user_obj = User.objects.exclude(id=request.user.id)
            seralizer = UserGetSerializer(user_obj, many=True)
            return Response(seralizer.data)
        except Exception as e:
            print(e)
            return Response(seralizer.errors)

@api_view(['GET'])
def get_chat_list(request, opponent_id):
    if request.method == 'GET':
        try:
            time.sleep(4)
            user_ids = [int(request.user.id), int(opponent_id)]
            user_ids = sorted(user_ids)
            thread_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            chats = Chat.objects.filter(thread_name=thread_name).order_by('-message_time')
            paginator = CustomPagination()
            results = paginator.paginate_queryset(chats, request)
            serializer = ChatSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
