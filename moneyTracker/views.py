from django.shortcuts import get_object_or_404
from .serializers import MoneySerializers, RegisterSerializer, LoginSerializers, TransactionSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from .models import Wallet, Transaction
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny

class WalletListApiView(generics.ListAPIView):
    serializer_class = TransactionSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['created', 'category']
    ordering = ['-created']

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(wallet__user = user)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def main_page(request):

    if request.method == 'POST':
        wallet = MoneySerializers(data=request.data, context={'request': request})
        if wallet.is_valid():
            wallet.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(wallet.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_wallet(request, wallet_id):
    wallet = get_object_or_404(Wallet, id=wallet_id, user=request.user)
    wallet.delete()
    return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def patch_money(request):

    wallet = Wallet.objects.filter(user=request.user).first()
    if not wallet:
        return Response({'detail': 'Кошелек не найден'}, status=status.HTTP_404_NOT_FOUND)
    serializers = TransactionSerializers(data=request.data)
    if serializers.is_valid():
        transaction = serializers.save(wallet=wallet)

        wallet.amount += transaction.amount
        wallet.save()
        
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if transaction.wallet.user != request.user:
        return Response({'detail': 'Нет прав удалить эту транзакцию'}, status=status.HTTP_403_FORBIDDEN)
    transaction.delete()
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
