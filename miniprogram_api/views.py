import string

from django.contrib.auth.models import User
from django.shortcuts import render
from pip._vendor import requests
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.crypto import random

from .wechat_process import WeChatCrypt
from .models import *
from .constants import *
from .serializers import *
from rest_framework import viewsets, generics, views, status


# Create your views here.

'''
Mini Program Login
@params:
    str:code
'''
class WeChatLogin(views.APIView):
    def post(self, request):
        code = request.data.get('code', None)
        if not code:
            raise Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        url = get_wechat_login_code_url(code)
        resp = requests.get(url)

        openid,session_key,unionid = None, None, None
        if resp.status_code != 200:
            raise Response({"error": "WeChat server return error, please try again later"})
        else:
            json = resp.json()
            if "errcode" in json:
                raise Response({"error": json["errmsg"]})
            else:
                openid, session_key, unionid = json['openid'], json['openid'], json['openid']

        if not session_key:
            raise Response({"error": "WeChat server doesn't return session key"})
        if not openid:
            raise Response({"error": "WeChat server doesn't return openid"})

        user = User.objects.filter(username=openid).first()
        if not user:
            user = User()
            user.username = openid
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            user.set_password(password)
            user.wechataccount.session_key = session_key
            user.wechataccount.openId = openid
            user.wechataccount.unionId = unionid
            user.save()

        token, created = Token.objects.get_or_create(user=None)
        if created:

            return Response({
                'token': token.key
            })
        else:
            raise Response({"error": "Create new user error, token doesn't generate"})


'''
Mini Program Update UserInfo
@params:
    str:encryptedData
    str:iv
'''
class WeChatUserInfoUpdateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        params = request.data
        encryptedData = params.get('encryptedData',None)
        iv = params.get('iv',None)

        if not encryptedData:
            raise Response({"encryptedData": "This field is reuqired"}, status=status.HTTP_400_BAD_REQUEST)

        if not iv:
            raise Response({"iv": "This field is reuqired"}, status=status.HTTP_400_BAD_REQUEST)

        wechat_user = WeChatAccount.objects.filter(user=self.request.user).first()
        pc = WeChatCrypt(wechat_user.session_key)

        user = pc.decrypt(encryptedData, iv)
        token = Token.objects.get(user=self.request.user)
        wechat_user.nickNone = user['nickName']
        wechat_user.gender = user['gender']
        wechat_user.language = user['language']
        wechat_user.city = user['city']
        wechat_user.avatarUrl = user['avatarUrl']
        wechat_user.save()
        return Response({'token': token.key, 'user': WeChatAccountSerializer(wechat_user).data}, status=status.HTTP_200_OK)

'''
Mini Program Payment 
'''
