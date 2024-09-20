"""
URL configuration for stairs_factory project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='My API Docs',
        default_version='v1',
        description=(
            'This project leverages Django REST Framework and JWT for robust '
            'user authentication and device management. It is designed to uniquely '
            'identify each device by its device ID and includes comprehensive features '
            'for managing user registration, authentication, and device operations. '
            'The system integrates a variety of models, views, and APIs to facilitate '
            'not only device and user management but also detailed job tracking and '
            'history management. Key functionalities include CRUD operations for various '
            'models, job and worklist management, error logging, and timesheet tracking. '
            'The project also incorporates a custom logging mechanism to capture'
            'and record critical events and actions throughout the application.'
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('jobs.urls')),
    path(
        'api/docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
