"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import re_path, path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

api_view = get_schema_view(
   openapi.Info(
      title="Quiz API",
      default_version='v1',
      description="글로벌널리지 백엔드 개발자 실무 과제",
      terms_of_service="https://www.google.com/policies/terms/"
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', api_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', api_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', api_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('account/', include('account.urls')),
    path('quiz/', include('quiz_manager.urls')),
    path('board/', include('quiz_board.urls')),
    path('exam/', include('exam.urls')),
]
