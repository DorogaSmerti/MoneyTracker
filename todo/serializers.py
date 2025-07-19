from rest_framework import serializers
from .models import Tasks
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class TasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id','title', 'completed', 'created']

class RegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
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
            raise serializers.ValidationError('Неверное имя или пароль')
        data['user'] = user
        return data