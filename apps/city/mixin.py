# coding=utf-8

from django.views.generic.base import ContextMixin

from apps.city.models import City


class CityListMixin(ContextMixin):
    """
    Миксин осуществляет добавление списка городов в контекст шаблона.
    """

    def get_context_data(self, **kwargs):
        context = super(CityListMixin, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            context.update({
                'city_list': City.objects.get_qs(user)
            })
        return context
