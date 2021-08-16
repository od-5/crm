# coding=utf-8
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyexcel
from apps.city.models import City
from apps.incoming.models import IncomingClient, IncomingClientManager, IncomingClientContact
import pyexcel_xls
import pyexcel_xlsx

__author__ = 'alexy'


def client_list_import(request):
    if request.method == 'POST' and 'file' in request.FILES:
        filename = request.FILES['file'].name
        extension = filename.split(".")[1]
        sheet = pyexcel.load_from_memory(extension, request.FILES['file'].read())
        data = pyexcel.to_dict(sheet)
        user = request.user
        error = []
        success = []
        i = 1
        for row in data:
            if row != 'Series_1':
                city = data[row][0]
                name = data[row][1]
                kind_of_activity = data[row][2]
                actual_address = data[row][3]
                site = data[row][4]
                contact_name = data[row][5]
                contact_function = data[row][6]
                contact_phone = data[row][7]
                contact_email = data[row][8]
                try:
                    # проверяем город
                    city_instance = City.objects.get(name__iexact=city)
                    try:
                        incomingclient = IncomingClient.objects.get(name__iexact=name)
                        error.append(u'Строка: %s .Клиент %s уже есть в системе' % (i, incomingclient.name))
                    except:
                        incomingclient = IncomingClient(
                            city=city_instance,
                            name=name,
                            manager=user.manager,
                        )
                        if kind_of_activity:
                            incomingclient.kind_of_activity = kind_of_activity
                        if actual_address:
                            incomingclient.actual_address = actual_address
                        if site:
                            incomingclient.site = site
                        incomingclient.save()
                        success.append(u'Клиент %s добавлен в систему' % name)
                        if contact_name:
                            incomingcontact = IncomingClientContact(
                                incomingclient=incomingclient,
                                name=contact_name
                            )
                        if contact_email:
                            incomingcontact.email = contact_email
                        if contact_phone:
                            incomingcontact.phone = contact_phone
                        if contact_function:
                            incomingcontact.function = contact_function
                        incomingcontact.save()
                        incomingclientmanager = IncomingClientManager(
                            manager=user.manager,
                            incomingclient=incomingclient
                        )
                        incomingclientmanager.save()
                except:
                    error.append(u'Строка %s, Город %s не доступен для модератора %s' % (i, city, user.manager.moderator))
            i += 1
        context = {
            'error_list': error,
            'error_count': len(error),
            'success_list': success,
            'success_count': len(success)
        }
        return render(request, 'incoming/import_error.html', context)
    else:
        return HttpResponseRedirect(reverse('incoming:list'))
