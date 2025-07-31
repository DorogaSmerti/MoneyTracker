from django.urls import path
from . import views
from .views import WalletAPIView, TransactionListCreateAPIView, TransactionReportAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/', WalletAPIView.as_view(), name='main_page'),
    path('api/delete_wallet/<int:wallet_id>/', views.delete_wallet, name='delete_wallet'),
    path('api/transaction/<int:wallet_id>/', TransactionListCreateAPIView.as_view(), name='transaction'),
    path('api/transaction_report/<int:wallet_id>/', TransactionReportAPIView.as_view(), name='transaction_report'),
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]