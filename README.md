![django_miniprogram_api](./LOGO/django_miniprogram_api.png)

Django MiniProgram API - Django 微信小程序 API
============================================

Django MiniProgram Auth

Quick start
-----------

1. 添加 "miniprogram_api" 和 django-rest-framework 相关的 modules 到 INSTALLED_APPS，并且添加 WECHAT_MINIPROGRAM_CONFIG 配置文件::
  
    ```python
    INSTALLED_APPS = [
        ...
        'miniprogram_api',
        'rest_framework.authtoken',
        'rest_framework',
]
    
    WECHAT_MINIPROGRAM_CONFIG = {
        "APPID": "",
        "SECRET": "",
        "WECHAT_PAY": {
            "MCH_ID": "",
            "KEY": "",
            "NOTIFICATION_URL": '',
        }
    }
    
     REST_FRAMEWORK = {
          'DEFAULT_PERMISSION_CLASSES': [
              ...
              'rest_framework.authentication.BasicAuthentication', # add this
              'rest_framework.authentication.SessionAuthentication', # add this
              'rest_framework.authentication.TokenAuthentication', # add this
          ]
      }
    ```
    
    
    
2. 配置小程序登陆 url /miniprogram_auth/ 到你项目的 urls.py::

    ```python
    url(r'^miniprogram_auth/', include('miniprogram_api.urls')),
    ```

    

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/.

5. Visit http://127.0.0.1:8000/ to .

Usage
-----