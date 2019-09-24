import datetime
import random
import string

import xmltodict
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.contrib.auth.models import User
from django.shortcuts import render
from pip._vendor import requests
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .wechat_process import WeChatCrypt, WeChatSignHelper, WeChatPay
from .models import *
from .constants import *
from .serializers import *
from rest_framework import viewsets, generics, views, status
from rest_framework_xml.parsers import XMLParser


# Create your views here.

'''
Mini Program Login
@params:
    str:code
'''
class WeChatLoginAPIView(views.APIView):
    permission_classes = []
    def post(self, request):
        code = request.data.get('code', None)
        if not code:
            return Response({"code": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        url = get_wechat_login_code_url(code)
        resp = requests.get(url)

        openid = None
        session_key = None
        unionid = None
        if resp.status_code != 200:
            return Response({"error": "WeChat server return error, please try again later"})
        else:
            json = resp.json()
            if "errcode" in json:
                return Response({"error": json["errmsg"]})
            else:
                openid = json['openid']
                session_key = json['session_key']

            if "unionid" in json:
                unionid = json['unionid']

        if not session_key:
            return Response({"error": "WeChat server doesn't return session key"})
        if not openid:
            return Response({"error": "WeChat server doesn't return openid"})

        user = User.objects.filter(username=openid).first()
        if not user:
            user = User()
            user.username = openid
            password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
            user.set_password(password)
            user.save()
        user.wechataccount.session_key = session_key
        user.wechataccount.openId = openid
        user.wechataccount.unionId = unionid
        user.wechataccount.save()
        user.save()

        token, created = Token.objects.get_or_create(user=user)
        if created:

            return Response({
                'token': token.key,
                'user_id': user.id
            })
        else:
            Token.objects.get(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.id
            })


'''
Mini Program Update UserInfo
@params:
    str:encryptedData
    str:iv
'''
class WeChatUserInfoUpdateAPIView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        params = request.data
        encryptedData = params.get('encryptedData',None)
        iv = params.get('iv',None)

        if not encryptedData:
            return Response({"encryptedData": "This field is reuqired"}, status=status.HTTP_400_BAD_REQUEST)

        if not iv:
            return Response({"iv": "This field is reuqired"}, status=status.HTTP_400_BAD_REQUEST)

        wechat_user = WeChatAccount.objects.filter(user=request.user).first()
        pc = WeChatCrypt(settings.WECHAT_MINIPROGRAM_CONFIG['APPID'], wechat_user.session_key)

        user = pc.decrypt(encryptedData, iv)
        token = Token.objects.get(user=self.request.user)
        wechat_user.nickName = user['nickName']
        wechat_user.gender = user['gender']
        wechat_user.language = user['language']
        wechat_user.city = user['city']
        wechat_user.avatarUrl = user['avatarUrl']
        wechat_user.save()
        return Response({'token': token.key, 'wechat': WeChatAccountSerializer(wechat_user).data}, status=status.HTTP_200_OK)

'''
Mini Program Payment Callback
'''

class PayResultsNotice(views.APIView):
    parser_classes = (XMLParser,)
    IGNORE_FIELDS_PREFIX = ["coupon_type_","coupon_id_","coupon_fee_"]
    def post(self,request):
        dataDict = xmltodict.parse(request.body)["xml"] #type:dict
        sign = WeChatSignHelper(dataDict,settings.WECHAT_MINIPROGRAM_CONFIG['WECHAT_PAY']['KEY']).getSign()
        if sign != dataDict['sign']:
            return Response(status=status.HTTP_403_FORBIDDEN)

        keyToBeDelete = []
        for key in dataDict.keys():
            for ignorePrefix in self.IGNORE_FIELDS_PREFIX:
                if ignorePrefix in key:
                    keyToBeDelete.append(key)
        for key in keyToBeDelete:
            del dataDict[key]

        #process timeEnd
        dataDict['time_end'] = datetime.datetime.strptime(dataDict['time_end'],"%Y%m%d%H%M%S")

        dataDict['out_trade_no'] = dataDict['out_trade_no']
        # assign order Id
        preOrder = PayOrder.objects.filter(out_trade_no=dataDict['out_trade_no']).first()

        if preOrder and not preOrder.paid:
            preOrder.paid = True
            preOrder.save()

        return Response(data=WeChatPay().dic_to_xml({'return_code':'SUCCESS'}))