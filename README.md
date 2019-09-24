![django_miniprogram_api](./LOGO/django_miniprogram_api.png)

Django MiniProgram API - Django 微信小程序 API
============================================

Django 微信小程序 API 是依赖于 django-rest-framework 制作的restful api，封装了微信小程序的登陆，用户资料更新，微信小程序支付等一系列操作。为开发者提供微信小程序后台的简便操作。

（完善中，登陆以及用户信息更新已经可以使用）

## 目录

[TOC]

## 安装

```bash
pip install django_miniprogram_api
```

## 安装依赖

```python
pycrypto==2.6.1
djangorestframework==3.10.3
xmltodict==0.12.0
djangorestframework-xml==1.4.0
Django==2.x.x
```

快速入门
-------

1. 添加 "miniprogram_api" 和 django-rest-framework 相关的 modules 以及 配置 到 INSTALLED_APPS，并且添加 WECHAT_MINIPROGRAM_CONFIG 配置文件::
  
    ```python
    INSTALLED_APPS = [
        'miniprogram_api',
        'rest_framework.authtoken',
        'rest_framework'
    ]
    WECHAT_MINIPROGRAM_CONFIG = {
        "APPID": "",
        "SECRET": "",
        "WECHAT_PAY": {
            "MCH_ID": "",  # 微信支付商户号
            "KEY": "", # API密钥
            "NOTIFICATION_URL": '', # 微信支付回调地址
        }
    }
    REST_FRAMEWORK = {
      	'DEFAULT_PERMISSION_CLASSES': [
            ...
            'rest_framework.authentication.BasicAuthentication', # add this
            'rest_framework.authentication.TokenAuthentication', # add this
        ],
      	'DEFAULT_PARSER_CLASSES': (
            'rest_framework_xml.parsers.XMLParser', 
        ),
    }
    ```
    
    
    
2. 配置小程序登陆 url /miniprogram_auth/ 到你项目的 urls.py::

    ```python
    url(r'^miniprogram_auth/', include('miniprogram_api.urls')),
    ```

    

3. 运行 `python manage.py migrate` 来创建 WeChatAccount 模型.

4. 运行测试服务器 `python manage.py runserver 127.0.0.1:8000` 就可以开始使用了

使用
---

### 小程序登陆

**请求**

`http://127.0.0.1/miniprogram_auth/login` 

method: post, 

body: 

```json
{
	"code": "061YsgK50ru0wC1uCHH50D2mK50YsgKa"
}
```

登陆模块包括了微信 [auth.code2Session](https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html) 接口，开发者通过调用 [wx.login()](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/wx.login.html) 获取临时登录凭证code，发送给 我们的 Login api，获取 django 的用户登录状态 Token。

**返回**

```json
{
	"token": "fa7cd4cdb5554a9b69b876d6c6bf775ac6be250d", // 返回的token 需要包含在 request header
	"user_id": 1
}
```

#### 使用 Token 保持会话

在你的请求头包含token信息，要注意的是如果你没有自定义的登录状态，例如：用户手机号邮箱注册登录，那么请在之后的api中都使用同样的token请求头。

```json
Authorization: Token fa7cd4cdb5554a9b69b876d6c6bf775ac6be250d
```

### 用户信息更新

**请求**

`http://127.0.0.1/miniprogram_auth/updateUserInfo` 

method: post, 

body: 

```json
{
	"iv":"QRWwdpUUx9zaN4fXGM4Asw==",
	"encryptedData": "F7VcR8vKZqzaEqS18f7qJ3VuYLl5AjExEHldqC3og3XOKlZPg+U9ki/onlrjrG9OLZDyJrno/nEegXH9V/1sMzGFpCCqhR9MHVTaq9fyANOVazniVmkzwysD0dwwk9bj4Uulz3KuqtTwoI2VFXEAmuj0kzCG1atqCo5RXZnZ30M8O3mbnSPAvDb6pEBBgT6YoQGuIskYQ82kIO3Z/ZtX8XCcmYAjagUkie1CGZUcYd5VxtSL6iGd+HVwxC1rspvda1OcgIdRlU/tIA3Euhbd4qKuqlmR6LJVdZNs9gg/CMY1ZGcRQnz8cbQWUqFOEaZQHU/oiXeDmo5V/HeQXzv9c+lgZ+SMk81VNLC8/T4SF5ivaoULHV/Th+jqYKDjJGwDAbM4tK+4Gkb45QFny3ZDh/09Fk9TwtfR2nkH/Wxpyyhkp0DPbhvd8oq8wH13I0XbsO0WuM0D8YpZF+H74CiiPDiKRzPEpLKU2nCWdlpHDZ0="
}
```

开发者通过调用接口（如 [wx.getUserInfo](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/user-info/wx.getUserInfo.html)）获取数据时，接口会同时返回 encryptedData， iv 数据，将此数据发送给updateUserInfo api，API 将会解密数据，以获取用户信息并返回。（此操作一般在小程序授权用户信息时使用，微信小程序的新登录规则，登陆实际上是限制的 [wx.getUserInfo](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/user-info/wx.getUserInfo.html) 接口）

**返回**

```json
{
   "token": "fa7cd4cdb5554a9b69b876d6c6bf775ac6be250d",
   "wechat": {
       "id": 1,
       "nickName": "TINCHY",
       "avatarUrl": "https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLp9mKpmqTUic0TmCMo6Cbibmsvmo6Vt3NGdP0cZOYRwoGPe13LsvHEicoZGvjq6syaeG0GGWJOrqCbA/132",
       "gender": "1",
       "city": "Shanghai",
       "province": null,
       "country": null,
       "user": 1
   }

}
```

### 微信支付 class wechat_pay.WeChatPay()

微信支付的api因为每一个操作都要求不同，不同用户不同场景都有需求，因此没有封装HTTP API，但是提供了一个简单封装的object，以及提供了一个订单状态 Model：PayOrder

想要获取订单状态，请将自己的商品 OneToOne 到 PayOrder, 例如：

```python
class PickUpOrder(models.Model):
		wechat_order = models.OneToOneField(PayOrder)
		...

@receiver(post_save, sender=PickUpOrder)
def create_order(sender, instance, created, **kwargs):
    if created:
        PayOrder.objects.create(pickuporder=instance, outTradeNo='')		
```

**<u>接口返回等数据请查询微信支付官方文档</u>** https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1

#### 统一下单

```python
WeChatPay().unified_order(
  spbill_create_ip='''小程序用户的IP地址''',
  open_id='''小程序用户的open id''', 
  body='''商品描述''',  
  order_id='''订单id，必须唯一，建议使用日期时间戳''',
  total_fee='''订单金额，单位为分！！！！'''
)
```

**简单例子：**

微信统一下单接口：https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1

```python

from .model import PickupOrder # 这个model是我的测试model，用于订单查询
from django.conf import settings # 导入 settings
from .wechat_pay import WeChatPay, WeChatSignHelper # 导入 微信支付 api 以及 签名验证
from miniprogram_api.model import WeChatAccount
from rest_framework import views, status

class WeChatPayAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        from django.utils.datetime_safe import datetime
        data = request.data
        _id = data['id']
        if not PickupOrder.objects.filter(id=data['id']).exists():
            raise ValidationError('This order does not exists')
        item = PickupOrder.objects.get(id=data['id'])
        if not item.payorder.paid: # 如果未付款
          	outTradeNo = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')[:-3] # 生成 order_id 用时间精确到分秒以保证订单号的唯一性
            item.order_id = outTradeNo
            item.payorder.outTradeNo = outTradeNo # 将订单号保存到 数据库
            item.save()
        wechat_user = WeChatAccount.objects.get(user=self.request.user)
        wp = WeChatPay()
        address = self.request.META.get('HTTP_X_FORWARDED_FOR') # 获取小程序访问用户的 ip 地址
        if address:
            ip = address.split(',')[0]
        else:
            ip = address.META.get('REMOTE_ADDR') 
        res = wp.unified_order(spbill_create_ip=ip,open_id=wechat_user.union_id, body=item.car_type.desc, total_fee=item.fee, order_id=item.order_id)
        if res['return_code'] == 'SUCCESS' and res['result_code'] == 'SUCCESS':
            pay_sign = {
                'appId': settings.WECHAT_MINIPROGRAM_CONFIG['APPID'],
                'nonceStr': wp.ranstr(16),
                'package': 'prepay_id='+res['prepay_id'],
                'signType': 'MD5',
                'timeStamp': str(time.time())
            }
            sign = WeChatSignHelper(pay_sign, settings.WECHAT_MINIPROGRAM_CONFIG['WECHAT_PAY']['KEY']).getSign()
            pay_sign['paySign'] = sign # 签名验证支付订单的正确性
            return Response({'pay_sign': pay_sign}) # 返回给小程序发起小程序的支付接口 
        else:
            return Response("Make order failed", status=status.HTTP_406_NOT_ACCEPTABLE)
```

下单之后，系统会根据您在settings.py中设置的 NOTIFICATION_URL 进行回调，来更新用户的订单状态。务必设置正确。（本地环境运行的服务器，微信无法进行回调，务必在生产或者测试服务器上运行）

```python
WECHAT_MINIPROGRAM_CONFIG = {
    "WECHAT_PAY": {
        "NOTIFICATION_URL": 'http://www.example.com/miniprogram_auth/wechatPayCallback', # 填写你的服务器地址加回调域名
    }
}
```

#### 查询订单

微信查询订单接口：https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2

```python
WeChatPay().order_query(
  transaction_id='''微信的订单号，建议优先使用''',
  out_trade_no='''商户系统内部订单号，要求32个字符内, 这里指的是 order_id, 即订单号'''
)
# transaction_id 和 out_trade_no 只需要选一个，不要全部填写
```

#### 关闭订单

微信关闭订单接口：https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3

```python
WeChatPay().close_order(
  out_trade_no='''商户系统内部订单号，要求32个字符内, 这里指的是 order_id, 即订单号'''
)
```

## 以下接口正在开发...

#### [申请退款](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4)

#### [查询退款](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_5)

#### [下载对账单](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_6)

#### [下载资金账单](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_18&index=7)

#### [支付结果通知](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_7&index=8)

#### [交易保障](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_8&index=9)

#### [退款结果通知](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_16&index=10)

#### [拉取订单评价数据](https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_17&index=11)

## LICENSE

BSD 3-Clause License

## 开发者

Tinchy：tinchy@yeah.net

## 赞助

![zanshang](/Users/qintianqi/Studio/开源项目/ti_django_wechat_miniprogram/django_miniprogram_api/LOGO/zanshang.png)