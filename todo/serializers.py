from rest_framework import serializers
from .models import Tasks
from django.contrib.auth.models import User

class TasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id','title', 'completed', 'created']
    