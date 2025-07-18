from django.shortcuts import get_object_or_404, render, redirect
from .serializers import TasksSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tasks

def todo_page(request):
    return render(request, 'todo/index.html')


@api_view(['GET', 'POST'])
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
def delete(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.delete()
    return Response(status=204)

@api_view(['PUT'])
def change_status(request, task_id):
    task = get_object_or_404(Tasks, id=task_id)
    task.completed = not task.completed
    task.save()
    serializer = TasksSerializers(task)
    return Response(serializer.data, status=200)