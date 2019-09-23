from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        write_only_fields = ['password']


class WeChatAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatAccount
        fields = '__all__'
        write_only_fields = ['unionId', 'openId', 'sessionKey']
