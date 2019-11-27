import os

from django.conf import settings

doc = "https://github.com/ti-technology/django_miniprogram_api"

if not settings.WECHAT_MINIPROGRAM_CONFIG:
    raise ValueError(f"Wechat mini-program config is required, please check the doc {doc}")


if not settings.WECHAT_MINIPROGRAM_CONFIG.get("APPID", None) or settings.WECHAT_MINIPROGRAM_CONFIG.get("APPID", None) == "":
    raise ValueError(f"Value APPID is required for this mini program, please check the doc {doc}")

if not settings.WECHAT_MINIPROGRAM_CONFIG.get("SECRET", None) or settings.WECHAT_MINIPROGRAM_CONFIG.get("SECRET", None) == "":
    raise ValueError(f"Value SECRET KEY is required for this mini program, please check the doc {doc}")


