# coding=utf-8
from copy import copy
import json
import datetime
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import TaskSerializer, TaskSurfaceSerializer, TaskSurfacePorchSerializer, UserSerializer, \
    PorchSerializer, SurfacePhotoSerializer
from apps.adjuster.models import Adjuster, AdjusterTask, AdjusterTaskSurface, AdjusterTaskSurfacePorch, SurfacePhoto
from apps.city.models import Porch
from apps.surface.forms import SurfacePhotoForm
from core.common import str_to_bool
from core.models import User
# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('django.request')


__author__ = 'alexy'


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def task_list(request, format=None):
    logger.error(u'request: %s' % request)
    user = request.user
    try:
        adjuster = user.adjuster
    except Adjuster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    qs = AdjusterTask.objects.select_related().filter(adjuster=adjuster, is_closed=False)
    if not qs:
        return Response(status=status.HTTP_204_NO_CONTENT)
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
        for atsurface in task.adjustertasksurface_set.filter(is_closed=False):
            ats_context = {
                'id': atsurface.id,
                'address': atsurface.get_address(),
                'porch_count': atsurface.get_porch_count(),
                'coord': atsurface.get_coord(),
            }
            porch_list = []
            for atsporch in atsurface.adjustertasksurfaceporch_set.filter(is_closed=False):
                atsp_context = {
                    'id': atsporch.id,
                    'porch_id': atsporch.porch.id,
                    'porch_number': atsporch.porch.number,
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
        task.sent = True
        task.save()
    logger.error(u'user=%s task_list' % request.user)
    return Response(context)


@api_view(['GET', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def api_root(request, format=None):
    """
    Точка входа в Api.
    Получение данных авторизованного пользователя
    """
    user = request.user
    logger.error(user)
    if request.method == 'GET':
        try:
            Adjuster.objects.get(user=user)
        except Adjuster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            adjuster = Adjuster.objects.get(user=user)
            coord_x = request.query_params.get('coord_x')
            if ',' in coord_x:
                coord_x = coord_x.replace(',', '.')
            coord_y = request.query_params.get('coord_y')
            if ',' in coord_y:
                coord_y = coord_y.replace(',', '.')
            adjuster.coord_x = float(coord_x)
            adjuster.coord_y = float(coord_y)
            adjuster.save()
            return Response(status=status.HTTP_200_OK)
        except Adjuster.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# def task_list(request):
#     """
#     Получение списка задач авторизованного монтажника
#     """
#     user = request.user
#     if request.method == 'GET':
#         tasks = AdjusterTask.objects.filter(adjuster__user=user, is_closed=False)
#         if not tasks:
#             print len(tasks)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             serializer = TaskSerializer(tasks, many=True)
#             return Response(serializer.data)


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


@api_view(['GET', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def tasksurfaceporch_detail(request, pk):
    """
    Выполнение работы по поверхности
    """
    try:
        porch = AdjusterTaskSurfacePorch.objects.get(pk=pk)
        logger.error(u'User=%s, worked with porch %s' % (request.user, porch.id))
    except AdjusterTaskSurfacePorch.DoesNotExist:
        logger.error(u'User=%s, worked with porch. PORCH NOT FOUND' % request.user)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TaskSurfacePorchSerializer(porch)
        return Response(serializer.data)
    if request.method == 'PUT':
        try:
            is_closed = str_to_bool(request.query_params.get('is_closed'))
        except:
            is_closed = porch.is_closed
        porch.is_closed = is_closed
        porch.save()
        try:
            logger.error(u'user=%s, porch=%s, params=%s' % (request.user, porch.id, request.query_params))
        except:
            logger.error(u'user=%s, porch=%s' % (request.user, porch.id))
        serializer = TaskSurfacePorchSerializer(porch)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def porch_update(request, pk):
    try:
        porch = Porch.objects.get(pk=pk)
        logger.error(u'porch update request. Porch=%s' % porch.id)
    except Porch.DoesNotExist:
        logger.error(u'porch update request. DoesNotExist')
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PorchSerializer(porch)
        return Response(serializer.data)
    if request.method == 'PUT':
        # print request.query_params['broken_shield']
        try:
            broken_shield = str_to_bool(request.query_params['broken_shield'])
        except:
            broken_shield = porch.broken_shield
        try:
            broken_gib = str_to_bool(request.query_params['broken_gib'])
        except:
            broken_gib = porch.broken_gib
        try:
            no_glass = str_to_bool(request.query_params['no_glass'])
        except:
            no_glass = porch.no_glass
        try:
            replace_glass = str_to_bool(request.query_params['replace_glass'])
        except:
            replace_glass = porch.replace_glass
        try:
            against_tenants = str_to_bool(request.query_params['against_tenants'])
        except:
            against_tenants = porch.against_tenants
        try:
            no_social_info = str_to_bool(request.query_params['no_social_info'])
        except:
            no_social_info = porch.no_social_info
        porch.broken_shield = broken_shield
        porch.broken_gib = broken_gib
        porch.no_glass = no_glass
        porch.replace_glass = replace_glass
        porch.against_tenants = against_tenants
        porch.no_social_info = no_social_info
        porch.save()
        try:
            logger.error(u'User=%s, porch update request. request=%s' %  (request.user, request.query_params))
        except:
            logger.error(u'User=%s, porch update request. NOT QUERY_PARAMS' %  request.user)
        serializer = PorchSerializer(porch)
        return Response(serializer.data)
        # return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def Nphoto_add(request):
    if request.method == 'POST':
        try:
            porch = request.data.get('porch')
            adjuster = request.data.get('adjuster')
            date = datetime.date.today()
            image = request.data.get('image')
            is_broken = request.data.get('is_broken')
            # print is_broken
            # print type(is_broken)
            logger.error(u'request for upload photo user %s' % request.user)
            logger.error(u'request.data %s' % request.data)
            data = request.data
            if len(data['date'].split(' ')) == 1:
                date = data['date']
                time = datetime.datetime.now().strftime('%H:%M')
                data['date'] = u'%s %s' % (date, time)
            serializer = SurfacePhotoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # item = SurfacePhoto.objects.get(pk=serializer.instance.id)
                # if is_broken == u'true':
                #     item.is_broken = True
                #     item.save()
                #     print 'is_broken'
                #     n_serializer = SurfacePhotoSerializer(item)
                #     print n_serializer.instance.is_broken
                try:
                    logger.error(u'Photo add Success %s' % serializer.instance.id)
                except:
                    logger.error(u'Photo add Success')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(u'c user %s - RESET CONTENT. request=%s' % (request.user, request.data))
                return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
            # form = SurfacePhotoForm(
            #     request.data,
            #     request.FILES,
            #     initial={'date': date}
            # )
            # photo.save()
            # print form
            # if form.is_valid():
            #     print 'valid'
            #     print form
            # else:
            #     print 'invalid'
            #     print form
                # print form
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
