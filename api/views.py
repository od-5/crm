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
    user = request.user
    if request.method == 'GET':
        tasks = AdjusterTask.objects.filter(adjuster__user=user, is_closed=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_detail(request, pk):
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
def tasksurface_detail(request, pk):
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


@api_view(['GET', 'PATCH'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def tasksurfaceporch_detail(request, pk):
    """
    Получение детализации состояня подъезда
    """
    try:
        print u'Пробуем получить подъезд'
        porch = AdjusterTaskSurfacePorch.objects.get(pk=pk)
        print u'Законичили получение'
    except AdjusterTaskSurfacePorch.DoesNotExist:
        print u'Нет такого подъезда'
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        print u'Метод = GET'
        serializer = TaskSurfacePorchSerializer(porch)
        return Response(serializer.data)
    if request.method == 'PATCH':
        print request.query_params['broken_shield']
        return Response(status=status.HTTP_200_OK)

