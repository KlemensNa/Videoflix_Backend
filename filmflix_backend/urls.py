"""
URL configuration for filmflix_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from filmflix.views import ChangeName, ChangePassword, CurrentUserView, CustomPasswordResetConfirmView, CustomPasswordResetView, IconListView, IconView, LoginView, RegisterView, VideoChoicesView, VideoView, activate  
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('api/users/me', CurrentUserView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('icons/', IconListView.as_view(), name='icon-list'),
    path('icons/<int:pk>/', IconView.as_view(), name='icon-detail'),
    path('video/', VideoView.as_view(), name='video'),
    path('video/<int:pk>/', VideoView.as_view(), name='single_video'),
    path('video/choices/', VideoChoicesView.as_view(), name='video_choices'),
    path("__debug__/", include("debug_toolbar.urls")),
    path('django-rq/', include('django_rq.urls')),
    path('change_password/<int:pk>/', ChangePassword.as_view()),
    path('change_name/<int:pk>/', ChangeName.as_view(), name='change-name'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
