# coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import ContextMixin, View
from django.views.generic.edit import FormMixin, ModelFormMixin, ProcessFormView
from django.views.generic.list import MultipleObjectTemplateResponseMixin, MultipleObjectMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from docxtpl import DocxTemplate

__author__ = '2mitrij'


# TODO: внедрить миксин
class RedirectlessFormMixin(FormMixin):
    """
    Миксин реализует поведение формы при котором после успешной валидации формы не производится редиректа.
    P.S. Такое поведение противоречит общепринятой модели PRG(Post/Redirect/Get) приложений.
    """
    def form_valid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


# TODO: внедрить миксин
class SendUserToFormMixin(FormMixin):
    """
    Миксин добавляет текущего пользователя в аргументы инициализации формы.
    """
    def get_form_kwargs(self):
        kwargs = super(SendUserToFormMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class PassGetArgsToCtxMixin(ContextMixin):
    """
    Миксин осуществляет проброс GET аргументов в контекст шаблона.
    Пробрасываемые аргументы должны быть перечислены в passed_get_args.
    К именам полей в контексте добавляется префикс 'r_'.
    """
    passed_get_args = None

    def get_context_data(self, **kwargs):
        context = super(PassGetArgsToCtxMixin, self).get_context_data(**kwargs)

        if self.passed_get_args:
            context.update(
                {'r_{}'.format(arg): self.request.GET.get(arg) for arg in self.passed_get_args})

        return context


# TODO: протестировать, внедрить
# TODO: context_object_name используется обоими сущностями, нужно разделить
# ListView
#     MultipleObjectTemplateResponseMixin
#         TemplateResponseMixin
#     BaseListView
#         MultipleObjectMixin
#             ContextMixin
#         View

# CreateView
#     SingleObjectTemplateResponseMixin
#         TemplateResponseMixin
#     BaseCreateView
#         ModelFormMixin
#             FormMixin
#                 ContextMixin
#             SingleObjectMixin
#                 ContextMixin
#         ProcessFormView
#             View

class ListWithCreateView(MultipleObjectTemplateResponseMixin, MultipleObjectMixin, ModelFormMixin, ProcessFormView):
    """
    Реализация класса, объединяющего ListView и CreateView.
    """
    def _check_allow_empty(self):
        # from BaseListView
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None and
                    hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                              % {'class_name': self.__class__.__name__})

    def get(self, request, *args, **kwargs):
        # from BaseListView
        self.object_list = self.get_queryset()
        self._check_allow_empty()

        # from BaseCreateView
        self.object = None

        return super(ListWithCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # from BaseListView
        self.object_list = self.get_queryset()
        self._check_allow_empty()

        # from BaseCreateView
        self.object = None

        return super(ListWithCreateView, self).post(request, *args, **kwargs)


class DocResponseMixin(object):
    """
    A mixin that can be used to render a doc file.
    """
    template_name = None
    filename = None
    content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def render_to_response(self, context, **response_kwargs):
        document = self.get_document()
        document.render(context)
        response = HttpResponse(content_type=self.content_type)
        response['Content-Disposition'] = 'attachment; filename=%s.docx' % (self.get_filename())
        document.save(response)
        return response

    def get_document(self):
        return DocxTemplate(self.get_template_name())

    def get_template_name(self):
        if self.template_name is None:
            raise ImproperlyConfigured(
                "DocResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_name()'")
        else:
            return settings.DOCX_TEMPLATE_DIR + self.template_name

    def get_filename(self):
        if self.filename is None:
            raise ImproperlyConfigured(
                "DocResponseMixin requires either a definition of "
                "'filename' or an implementation of 'get_filename()'")
        else:
            return self.filename


class BaseRemoveView(View):
    """
    Базовый класс удаления объектов
    """
    success_url = None
    model = False

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            return self.request.META['HTTP_REFERER']

    def get_queryset(self):
        chk_grp = self.request.POST.getlist('chk_grp[]')
        if chk_grp and self.model:
            return self.model.objects.filter(pk__in=[int(i) for i in chk_grp if i.isdigit()])
        return self.model.objects.none()

    def post(self, request):
        qs = self.get_queryset()
        print(qs)
        qs.delete()
        return HttpResponseRedirect(self.get_success_url())
