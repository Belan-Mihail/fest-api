"""drfapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route

# 8 import includea and add path to profile api
# 9 create serializers.py

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),

# 16
#     Now, we’ll have to add the login and  logout views for the browsable API.  
# These come with the rest framework, all we  have to do is include them in the main urls.py.
    path('api-auth/', include('rest_framework.urls')),

    # 17 create permissions.py in drfapi

    path('', include('profiles.urls')),

    # 32 views 
    # 31
    path('', include('post.urls')),

    # 43 create likes app/ add to settings and go to the models
    # 42
    path('', include('comments.urls')),

    # 47 create likes followers/ add to settings and go to the models
    # 46
    path('', include('likes.urls')),

    # 51
    path('', include('followers.urls')),
    path('', include('walls.urls')),
    path('', include('wallitems.urls')),
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
]
