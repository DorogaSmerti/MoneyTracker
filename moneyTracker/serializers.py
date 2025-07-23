from rest_framework import serializers
from .models import Wallet, Transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
    
class TransactionSerializers(serializers.ModelSerializer):
    wallet = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'

class MoneySerializers(serializers.ModelSerializer):
    transactions = TransactionSerializers(many=True, read_only=True)
    class Meta:
        model = Wallet
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Пароль не совпадает')
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1']
        )
        return user

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Неправильный логин или пароль')
        data['user'] = user
        return data