import base64
import json
from crypto.Cipher import AES
from django.conf import settings

'''
WeChat Crypt
'''
class WeChatCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        del decrypted['watermark']
        del decrypted['openId']
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


'''
WeChat Pay Process
'''
import json
import random
import string
import hashlib

import xmltodict

import requests
from xml.etree.ElementTree import *


class WeChatPay:


    def __init__(self):
        self.appId = settings.WECHAT_MINIPROGRAM_CONFIG['APPID']
        self.secret = settings.WECHAT_MINIPROGRAM_CONFIG['SECRET']
        self.mch_id = settings.WECHAT_MINIPROGRAM_CONFIG["WECHAT_PAY"]['MCH_ID']
        self.notify_url = settings.WECHAT_MINIPROGRAM_CONFIG["WECHAT_PAY"]['NOTIFICATION_URL']

    def ranstr(self, num):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, num))

        return salt

    def unified_order(self, open_id, body, car_item, order_id, total_fee, spbill_create_ip):
        nonce_str = self.ranstr(16)
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        payload = {
            'appid': self.appId,
            'body': body,
            'mch_id': self.mch_id,
            'nonce_str': nonce_str,
            'notify_url': self.notify_url,
            'openid': open_id,
            'out_trade_no': str(order_id),
            'spbill_create_ip': spbill_create_ip,
            'trade_type': 'JSAPI',
            'total_fee': int((total_fee * 60) * 100),
        }
        sign = WeChatSignHelper(payload, settings.WECHAT_MINIPROGRAM_CONFIG["WECHAT_PAY"]['KEY']).getSign()
        payload['sign'] = sign
        payload = str(self.dic_to_xml(payload))
        response = requests.post(url, data=payload.encode("utf-8"))
        data = self.xml_to_dict(response.content.decode())
        return data

    def order_query(self, transaction_id):
        url = "https://api.mch.weixin.qq.com/pay/orderquery"
        nonce_str = self.ranstr(8)
        string_for_sign = "appid=" +self.appId + "&mch_id=" + self.mch_id + "&nonce_str=" + nonce_str + "&transaction_id=" + transaction_id
        sign = string_for_sign + settings.WECHAT_MINIPROGRAM_CONFIG["WECHAT_PAY"]['KEY']
        sign = str(hashlib.md5(sign.encode())).upper()
        payload = {
            'appid': self.appId,
            'mch_id': self.mch_id,
            'nonce_str': nonce_str,
            'sign': sign,
            'transaction_id': transaction_id
        }

        response = requests.post(url, data=payload)
        return response.json()

    def close_order(self, out_trade_no):
        url = "https://api.mch.weixin.qq.com/pay/closeorder"
        nonce_str = self.ranstr(8)
        string_for_sign = "appid=" +self.appId + "&mch_id=" + self.mch_id + "&nonce_str=" + nonce_str
        sign = string_for_sign + settings.WECHAT_MINIPROGRAM_CONFIG["WECHAT_PAY"]['KEY']
        sign = str(hashlib.md5(sign.encode())).upper()
        payload = {
            'appid': self.appId,
            'mch_id': self.mch_id,
            'nonce_str': nonce_str,
            'sign': sign,
            'out_trade_no': out_trade_no
        }

        response = requests.post(url, data=payload)
        return response.json()

    def dic_to_xml(self,d):
        ele = '<xml>'
        for key, val in d.items():
            ele += '<' + str(key) + '>' + str(val) + '</' + str(key) + '>'

        return ele + '</xml>'

    def xml_to_dict(self,xml):
        return xmltodict.parse(str(xml))['xml']


import collections
import hashlib
import copy

class WeChatSignHelper:
    def __init__(self,dataDict,apiKey):
        self.data = copy.deepcopy(dataDict) #type: dict
        self.apiKey = apiKey
        self.keyValueString = ""
        self.clean_up()
        self.dataToKeyValueString()


    def clean_up(self):
        if "sign" in self.data:
            del self.data["sign"]

    def dataToKeyValueString(self):
        od = collections.OrderedDict(sorted(self.data.items()))
        for key,value in od.items():
            self.keyValueString+=f"{key}={value}&"
        self.keyValueString += f"key={self.apiKey}"

    def getSign(self):
        md5Obj = hashlib.md5()
        md5Obj.update(self.keyValueString.encode("utf-8"))
        return md5Obj.hexdigest().upper()