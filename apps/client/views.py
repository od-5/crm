# coding=utf-8
from annoying.decorators import ajax_request
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from apps.cabinet.forms import UserAddForm
from apps.city.models import City
from core.models import User
from .models import Client

__author__ = 'alexy'

def client_add(request):
    user = request.user
    if user.type == 1:
        city_list = City.objects.all()
    elif user.type == 2:
        city_list = City.objects.filter(moderator=user.id)
    context = {
        'city_list': city_list
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            User.objects.get(email=email)
            context.update({
                'error': u'Такой пользователь уже зарегистрирован!'
            })
        except:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 and password2 and password1 == password2:
                pass
                new_user = User.objects.create_user(email, password1, type=3)
                context.update({
                    'success': u'Пользователь успешно создан!'
                })
                city_id = request.POST.get('city')
                city = City.objects.get(pk=int(city_id))
                legal_name = request.POST.get('legal_name')
                actual_name = request.POST.get('actual_name')
                inn = request.POST.get('inn')
                kpp = request.POST.get('kpp')
                legal_address = request.POST.get('legal_address')
                leader = request.POST.get('leader')
                leader_function = request.POST.get('leader_function')
                work_basis = request.POST.get('work_basis')
                client = Client.objects.create(
                    user=new_user,
                    city=city,
                    legal_name=legal_name,
                    actual_name=actual_name,
                    inn=inn,
                    kpp=kpp,
                    legal_address=legal_address,
                    leader=leader,
                    leader_function=leader_function,
                    work_basis=work_basis
                )
            else:
                context.update({
                    'error': u'Пароль и подтверждение пароля не совпадают!'
                })
    else:
        print 'NO ***'*5

    return render(request, 'client/user_form.html', context)


def client_update(request, pk):
    user = request.user
    client_id = int(pk)
    client = Client.objects.get(pk=client_id)

    if user.type == 1:
        city_list = City.objects.all()
    elif user.type == 2:
        city_list = City.objects.filter(moderator=user.id)
    context = {
        'object': client,
        'city_list': city_list
    }

    client_user = User.objects.get(client=client)

    if request.method == 'POST':
        success_message = u''
        msg = None
        city_id = int(request.POST.get('city'))
        city = City.objects.get(pk=city_id)
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        patronymic = request.POST.get('patronymic')
        legal_name = request.POST.get('legal_name')
        actual_name = request.POST.get('actual_name')
        inn = request.POST.get('inn')
        kpp = request.POST.get('kpp')
        legal_address = request.POST.get('legal_address')
        leader = request.POST.get('leader')
        leader_function = request.POST.get('leader_function')
        work_basis = request.POST.get('work_basis')
        if password1 and password2:
            if password1 == password2:
                client_user.set_password(password1)
                success_message += u'Пароль успешно изменен. '
            else:
                context.update({
                    'error': u'Пароль и подтверждение пароля не совпадают'
                })

        if client_user.email != email:
            client_user.email = email
            msg = u'Данные успешно изменены. '
        if client_user.last_name != last_name:
            client_user.last_name = last_name
            msg = u'Данные успешно изменены. '
        if client_user.first_name != first_name:
            client_user.first_name = first_name
            msg = u'Данные успешно изменены. '
        if client_user.patronymic != patronymic:
            client_user.patronymic = patronymic
            msg = u'Данные успешно изменены. '
        client_user.save()

        if client.legal_name != legal_name:
            client.legal_name = legal_name
            msg = u'Данные успешно изменены. '
        if client.actual_name != actual_name:
            client.actual_name = actual_name
            msg = u'Данные успешно изменены. '
        if client.inn != inn:
            client.inn = inn
            msg = u'Данные успешно изменены. '
        if client.kpp != kpp:
            client.kpp = kpp
            msg = u'Данные успешно изменены. '
        if client.legal_address != legal_address:
            client.legal_address = legal_address
            msg = u'Данные успешно изменены. '
        if client.leader != leader:
            client.leader = leader
            msg = u'Данные успешно изменены. '
        if client.leader_function != leader_function:
            client.leader_function = leader_function
            msg = u'Данные успешно изменены. '
        if client.work_basis != work_basis:
            client.work_basis = work_basis
            msg = u'Данные успешно изменены. '

        if client.city.id != city_id:
            client.city = city
            client.save()

        if msg:
            success_message += msg
        context.update({
            'success': success_message
        })
    return render(request, 'client/client_update.html', context)


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        user_id = self.request.user.id
        print user_id
        if self.request.user.type == 1:
            qs = Client.objects.all()
        elif self.request.user.type == 2:
            qs = Client.objects.filter(city__moderator=user_id)
        else:
            qs = None
        queryset = qs
        return queryset


class ClientCreateView(CreateView):
    model = User
    template_name = 'client/user_form.html'
    form_class = UserAddForm

    def get_initial(self):
        """
        Добавление request.user в форму, для ограничения
        в зависимости от уровня доступа пользователя
        """
        initial = super(ClientCreateView, self).get_initial()
        initial = initial.copy()
        initial['type'] = 3
        return initial
