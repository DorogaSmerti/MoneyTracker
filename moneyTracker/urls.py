from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.main_page, name='main'),
    path('api/wallet/', views.WalletListApiView.as_view(), name='wallet-list'),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/delete_wallet/<int:wallet_id>/', views.delete_wallet, name='delete_wallet'),
    path('api/patch_money/', views.patch_money, name='patch_money'),
    path('api/delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]