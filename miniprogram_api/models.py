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
    outTradeNo = models.CharField(max_length=32)
    paid = models.BooleanField(default=False)