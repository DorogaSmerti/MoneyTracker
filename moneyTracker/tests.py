from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Wallet, Transaction
from decimal import Decimal

class WalletAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_and_get_wallet(self):
        responce = self.client.post('/api/', {'amount': 100})
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(Wallet.objects.first().amount, 100)

        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(Decimal(response.data[0]['amount']), Decimal(100.00))

    def test_create_and_get_transaction(self):
        self.wallet = Wallet.objects.create(user=self.user, amount=0)
        response = self.client.post('/api/transaction/1/', {"name": "Жизнь", "description": "Ресторан Абу", "amount": 50, "category": "other"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().category, "other") 

        response = self.client.get('/api/transaction/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data[0]['name'], 'Жизнь')
        self.assertEqual(data[0]['description'], 'Ресторан Абу')
        self.assertEqual(data[0]['category'], 'other')
        self.assertEqual(Decimal(data[0]['amount']), Decimal(50.00))
