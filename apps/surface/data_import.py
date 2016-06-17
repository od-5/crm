# coding=utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import pyexcel
from apps.city.models import City, Area, Street, Surface, Porch
import pyexcel_xls
import pyexcel_xlsx

__author__ = 'alexy'


def address_list_import(request):
    if request.method == 'POST' and 'file' in request.FILES:
        filename = request.FILES['file'].name
        extension = filename.split(".")[1]
        sheet = pyexcel.load_from_memory(extension, request.FILES['file'].read())
        data = pyexcel.to_dict(sheet)
        for row in data:
            if row != 'Series_1':
                city = data[row][0]
                area = data[row][1]
                street = data[row][2]
                house_number = ''
                point_flag = False
                for i in unicode(data[row][3]):
                    if i == '.':
                        point_flag = True
                    if point_flag:
                        if i != '0' and i != '.':
                            house_number += i
                    else:
                        house_number += i

                try:
                    porch_list = [int(data[row][4])]
                except:
                    r_porch_list = data[row][4].strip().split(',')
                    porch_list = []
                    for porch in r_porch_list:
                        try:
                            porch_list.append(int(porch))
                        except:
                            pass
                try:
                    # пробуем получить город
                    city_instance = City.objects.get(name__iexact=city)
                    try:
                        # пробуем получить район
                        area_instance = Area.objects.get(city=city_instance, name__iexact=area)
                    except:
                        # создаём новый район
                        area_instance = Area(city=city_instance, name=area)
                        area_instance.save()
                    try:
                        # пробуем получить улицу
                        street_instance = Street.objects.get(city=city_instance, area=area_instance, name__iexact=street)
                    except:
                        # создаём новую улицу
                        street_instance = Street(city=city_instance, area=area_instance, name=street)
                        street_instance.save()
                    try:
                        # пробуем получить поверхность
                        surface_instance = Surface.objects.get(city=city_instance, street=street_instance,
                                                               house_number=house_number)
                    except:
                        # создаём поверхность
                        surface_instance = Surface(city=city_instance, street=street_instance, house_number=house_number)
                        surface_instance.save()
                    for i in porch_list:
                        # пробегаемся по списку подъездов
                        try:
                            Porch.objects.get(surface=surface_instance, number=i)
                        except:
                            porch = Porch(surface=surface_instance, number=i)
                            porch.save()
                except:
                    pass
                    # print u'Город не найден'
    return HttpResponseRedirect(reverse('surface:list'))
