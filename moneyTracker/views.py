from django.shortcuts import get_object_or_404
from .models import Wallet, Transaction
from .serializers import WalletSerializers, TransactionSerializers, RegisterSerializer, LoginSerializers
from rest_framework import generics, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

class WalletAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        wallet = Wallet.objects.filter(user=request.user)
        serializers = WalletSerializers(wallet, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = WalletSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_wallet(request, wallet_id):
    wallet = Wallet.objects.filter(user=request.user, id=wallet_id).first()
    wallet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
class TransactionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['wallet', 'amount', 'category']
    ordering_fields= ['created']
    ordering = ['-created']

    def get_queryset(self): # Получение транзакций
        wallet_id = self.kwargs.get('wallet_id')
        return Transaction.objects.filter(wallet__user=self.request.user, wallet__id=wallet_id)
        
    def perform_create(self, serializer): # Добавление транзакции в кошель
        wallet_id = self.kwargs.get('wallet_id')
        wallet = Wallet.objects.filter(user=self.request.user, id=wallet_id).first()

        if not wallet:
            return Response({'detail': 'Не найден кошелек'}, status=status.HTTP_400_BAD_REQUEST)
        
        transactions = serializer.save(wallet=wallet)
        wallet.amount += transactions.amount
        wallet.save()
        return Response(TransactionSerializers(transactions).data, status=status.HTTP_201_CREATED)
    
class TransactionReportAPIView(APIView): # Агрегация транзакций(отчёты)
    def get(self, request, wallet_id):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({'detail': "Обязательны даты"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet = Wallet.objects.get(user=request.user, id=wallet_id)
        except Wallet.DoesNotExist:
            return Response({'detail': 'Кошелек не найден'}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction_by_id = Transaction.objects.filter(wallet=wallet, created__date__range=(start_date, end_date))
        total_overall_amount = transaction_by_id.aggregate(total = Sum('amount'))['total'] or 0
        categories_data = transaction_by_id.values("category").annotate(
            total = Sum('amount'),
            name = Count('name'),
        )

        return Response({
            "total_amount": total_overall_amount,
            "walletID": wallet.id,
            "categories": list(categories_data)},
            status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id)
    wallet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializers = RegisterSerializer(data = request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializers = LoginSerializers(data=request.data)
    if serializers.is_valid():
        user = serializers.validated_data['user']
        tokens = get_token_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
