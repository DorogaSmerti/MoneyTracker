from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.amount}'

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('entertaiment', 'Развлечение'),
        ('food', 'Еда'),
        ('shopping', 'Магазин'),
        ('other', 'Разное'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, blank=True, default='other')
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return dict(self.CATEGORY_CHOICES).get(self.name, self.name)