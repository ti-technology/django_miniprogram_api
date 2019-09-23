from django.conf import settings

if not settings.WECHAT_MINIPROGRAM_CONFIG:
    raise Exception


def get_wechat_login_code_url(code):
    return f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WECHAT_MINIPROGRAM_CONFIG['APPID']}&secret={settings.WECHAT_MINIPROGRAM_CONFIG['SECRET']}&js_code={code}&grant_type=authorization_code"


def get_wechat_update_uerinfo_url():
    return