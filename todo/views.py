from django.shortcuts import get_object_or_404
from .serializers import TasksSerializers, RegisterSerializers, LoginSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tasks
from rest_framework import status
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def main_todo(request):
    if request.method == 'GET':
        comleted = request.GET.get('completed')
        tasks = Tasks.objects.all().order_by('-created')
        if comleted:
            tasks = tasks.filter(completed=True)
        serializers = TasksSerializers(tasks, many=True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        task = TasksSerializers(data = request.data)
        if task.is_valid():
            task.save()
            return Response(task.data, status=201)
        return Response(task.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.delete()
    return Response(status=204)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_status(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.completed = not task.completed
    task.save()
    serializer = TasksSerializers(task)
    return Response(serializer.data, status=200)

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def register(request):
    new_user = RegisterSerializers(data = request.data)
    if new_user.is_valid():
        new_user.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def post(request):
    serializers = LoginSerializers(data=request.data)
    if serializers.is_valid():
        user = serializers.validated_data['user']
        tokens = get_token_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
