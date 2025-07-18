from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from todo.views import register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grade/', include('grade.urls')),
    path('', include('todo.urls')),
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='todo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
