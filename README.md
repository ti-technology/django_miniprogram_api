![django_miniprogram_api](./LOGO/django_miniprogram_api.png)

Django MiniProgram Auth
=======================

Django MiniProgram Auth

Quick start
-----------

1. Add "miniprogram_auth" and django-rest-framework to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'miniprogram_api',
        'rest_framework.authtoken',
        'rest_framework',
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            ...
            'rest_framework.authentication.BasicAuthentication', # add this
            'rest_framework.authentication.SessionAuthentication', # add this
            'rest_framework.authentication.TokenAuthentication', # add this
        ]
    }

2. Include the miniprogram_auth URLconf in your project urls.py like this::

    url(r'^miniprogram_auth/', include('miniprogram_auth.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/.

5. Visit http://127.0.0.1:8000/ to .

Usage
-----