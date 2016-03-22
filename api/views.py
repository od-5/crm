# coding=utf-8
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import TaskSerializer, TaskSurfaceSerializer, TaskSurfacePorchSerializer
from apps.adjuster.models import Adjuster, AdjusterTask, AdjusterTaskSurface, AdjusterTaskSurfacePorch
__author__ = 'alexy'


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_list(request):
    """
    Получение списка задач авторизованного монтажника
    """
    if request.method == 'GET':
        tasks = AdjusterTask.objects.filter(adjuster__user=user, is_closed=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def adjustertask_detail(request, pk):
    """
    Получение списка адресов задачи
    """
    try:
        tasksurface_list = AdjusterTaskSurface.objects.filter(adjustertask__id=pk)
    except AdjusterTaskSurface.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TaskSurfaceSerializer(tasksurface_list, many=True)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = TaskSerializer(tasksurface_list, data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(
    #             serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # elif request.method == 'DELETE':
    #     tasksurface_list.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def adjustertasksurface_detail(request, pk):
    """
    Получение списка подъездов дома в задаче
    """
    try:
        porch_list = AdjusterTaskSurfacePorch.objects.filter(adjustertasksurface__id=pk)
    except AdjusterTaskSurfacePorch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TaskSurfacePorchSerializer(porch_list, many=True)
        return Response(serializer.data)
