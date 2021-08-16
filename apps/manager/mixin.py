# coding=utf-8

from django.views.generic.base import ContextMixin

from .models import Manager


class ManagerListMixin(ContextMixin):
    """
    Миксин осуществляет добавление списка менеджеров в контекст шаблона.
    """

    def get_context_data(self, **kwargs):
        context = super(ManagerListMixin, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context.update({
                'manager_list': Manager.objects.get_qs(user).select_related('user')
            })
        return context
