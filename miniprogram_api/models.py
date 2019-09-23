from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class WeChatAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=100, null=True,blank=False)
    avatarUrl = models.CharField(max_length=255, null=True,blank=False)
    openId = models.CharField(max_length=255, null=True,blank=False)
    unionId = models.CharField(max_length=100, null=True,blank=False)
    gender = models.CharField(max_length=100, null=True,blank=False)
    city = models.CharField(max_length=100, null=True,blank=False)
    province = models.CharField(max_length=100, null=True,blank=False)
    country = models.CharField(max_length=100, null=True,blank=False)
    unionId = models.CharField(max_length=255, null=True,blank=False)
    session_key = models.CharField(max_length=255, null=True,blank=False)
    def __str__(self):
        if self.nickName:
            return self.nickName
        else:
            return self.user.username

@receiver(post_save, sender=User)
def create_wechat_user(sender, instance, created, **kwargs):
    if created:
        WeChatAccount.objects.create(user=instance, nickName='')

class PayOrder(models.Model):
    appId = models.CharField(max_length=32)
    mchId = models.CharField(max_length=32)
    deviceInfo = models.CharField(max_length=32)
    nonceStr = models.CharField(max_length=32)
    sign = models.CharField(max_length=32,null=True)
    signType = models.CharField(max_length=32)
    body = models.CharField(max_length=128)
    outTradeNo = models.CharField(max_length=32)
    totalFee = models.IntegerField()
    spBillCreateIp = models.CharField(max_length=64)
    timeStart = models.CharField(max_length=14)
    timeExpire = models.CharField(max_length=14)
    notifyUrl = models.CharField(max_length=256)
    tradeType = models.CharField(max_length=16)
    openId = models.CharField(max_length=128)

    returnCode = models.CharField(max_length=16,null=True)
    returnMsg = models.CharField(max_length=128,null=True)

    resultCode = models.CharField(max_length=16,null=True)
    errCode = models.CharField(max_length=32,null=True)
    errCodeDesc = models.CharField(max_length=128,null=True)

    prepayId = models.CharField(max_length=64)