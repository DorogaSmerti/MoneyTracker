from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/todo_main/', views.main_todo, name='main_todo'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/delete/<int:task_id>', views.delete, name='delete'),
    path('api/change_status/<int:task_id>', views.change_status, name='change_status'),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.post, name='login'),
]