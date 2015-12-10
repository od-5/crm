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
                print '*'*10
                print city, legal_name, actual_name, inn, kpp, legal_address, leader, leader_function, work_basis
                print '*'*10
            else:
                context.update({
                    'error': u'Пароль и подтверждение пароля не совпадают!'
                })
    else:
        print 'NO ***'*5

    return render(request, 'client/user_form.html', context)


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

    # def get_context_data(self, **kwargs):
    #     context = super(ExcurseListView, self).get_context_data(**kwargs)
    #     qs = Excurse.objects.all()
    #     context.update(
    #         qs.aggregate(Min('price'))
    #     )
    #     context.update(
    #         qs.aggregate(Max('price'))
    #     )
    #     context.update({
    #         'excurse_section_list': ExcurseSection.objects.all()
    #     })
    #     return context


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


# class SurfaceUpdateView(UpdateView):
#     model = Surface
#     # template_name = 'cabinet/profile.html'
#     form_class = SurfaceAddForm
#
#     # def get_object(self, queryset=None):
#     #     print self.request.user
#     #     return self.request.user
#
#     def get_initial(self):
#         """
#         Добавление request.user в форму, для ограничения
#         в зависимости от уровня доступа пользователя
#         """
#         initial = super(SurfaceUpdateView, self).get_initial()
#         user = self.request.user
#         initial = initial.copy()
#         initial['user'] = self.request.user
#         return initial
