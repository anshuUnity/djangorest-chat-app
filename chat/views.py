from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import UserGetSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
import time
# Create your views here.

User = get_user_model()

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
