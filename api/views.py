# coding=utf-8
import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import TaskSerializer, TaskSurfaceSerializer, TaskSurfacePorchSerializer, UserSerializer
from apps.adjuster.models import Adjuster, AdjusterTask, AdjusterTaskSurface, AdjusterTaskSurfacePorch
from core.models import User

__author__ = 'alexy'


@api_view(['GET'])
def test(request, format=None):
    qs = AdjusterTask.objects.all()
    context = []
    for task in qs:
        t_context = {
            'id': task.id,
            'date': task.date,
            'city': task.get_city_name(),
            'address_count': task.get_surface_count(),
            'porch_count': task.get_porch_count(),
            'type': task.get_type_display(),
            'comment': task.comment
        }
        address_list = []
        for atsurface in task.adjustertasksurface_set.all():
            ats_context = {
                'id': atsurface.id,
                'address': atsurface.get_address(),
                'porch_count': atsurface.get_porch_count(),
                'coord': atsurface.get_coord(),
            }
            porch_list = []
            for atsporch in atsurface.adjustertasksurfaceporch_set.all():
                atsp_context = {
                    'id': atsporch.id,
                    'porch_id': atsporch.porch.id,
                    'broken_shield': atsporch.broken_shield(),
                    'broken_gib': atsporch.broken_gib(),
                    'no_glass': atsporch.no_glass(),
                    'replace_glass': atsporch.replace_glass(),
                    'against_tenants': atsporch.against_tenants(),
                    'no_social_info': atsporch.no_social_info()
                }
                porch_list.append(atsp_context)
                ats_context.update({
                    'porch_list': porch_list
                })
            address_list.append(ats_context)
            t_context.update({
                'address_list': address_list
            })
        context.append(t_context)
    print context
    return Response(context)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_root(request, format=None):
    """
    Точка входа в Api.
    Получение данных авторизованного пользователя
    """
    user = request.user
    if request.method == 'GET':
        try:
            Adjuster.objects.get(user=user)
        except Adjuster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)


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
        if not tasks:
            print len(tasks)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
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
        print request.query_params
        print request.FILES.get('id')
        return Response(status=status.HTTP_200_OK)

