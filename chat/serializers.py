from django.contrib.auth import get_user_model
from chat.models import Chat
from rest_framework import serializers

class UserGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'id']
        extra_kwargs = {'id': {'read_only': True}}

class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat()
        fields = "__all__"
        extra_kwargs = {'id': {'read_only': True}}
        