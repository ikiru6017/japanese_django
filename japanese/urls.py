"""japanese URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf  import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users.views import line_chart, line_chart_json
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from ckeditor_uploader import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('articles/', include('articles.urls', namespace='articles')),
    path('lessons/', include('lessons.urls', namespace='lessons')),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('mainApp.urls', namespace='mainApp')),
    path('ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(views.browse)), name='ckeditor_browse'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('perfomance/', user_views.PerfomanceListView.as_view(template_name='users/perfomance.html'), name='index'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', user_views.line_chart_json, name='line_chart_json'),
    

]

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
