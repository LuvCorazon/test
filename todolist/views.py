from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskDetailSerializer
from rest_framework import status

@api_view(['GET', 'POST'])
def task_view(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(is_active=True)

        data = TaskSerializer(tasks, many=True).data

        return Response(data=data,
                        status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_view(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:

        return Response(data={'message': 'Product not found'},
                    status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = TaskDetailSerializer(task).data
        return Response(data=data,)
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = TaskDetailSerializer(task).data
        serializer = TaskDetailSerializer(task, data=request.data,
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

