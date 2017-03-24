# coding=utf-8
from functools import partial, wraps

from nested_formset import BaseNestedFormset

from django import forms
from django.forms.formsets import BaseFormSet


class BlockedModelFormMixin(forms.ModelForm):
    """
    Миксин реализует модельную форму, содержимое которой может быть недоступно для редактирования.

    Форма блокируется если в конструктор передан аргумент blocked.
    """
    def __init__(self, *args, **kwargs):
        self.blocked = kwargs.pop('blocked', False)
        if self.blocked:
            kwargs.pop('data', None)
            kwargs.pop('files', None)

        super(BlockedModelFormMixin, self).__init__(*args, **kwargs)

        if self.blocked:
            for field in self.fields.values():
                field.widget.attrs['disabled'] = 'disabled'


class FormKwargsFormsetMixin(BaseFormSet):
    """
    Миксин расширяет функционал наборов форм, позволяя передавать дополнительные аргументы в конструктор форм формсета.

    Аргументы форм необходимо передать в конструктор формсета как аргумент form_kwargs в виде словаря.
    P.S. реализовано в Django 1.9.
    """
    def __init__(self, *args, **kwargs):
        self.form_kwargs = kwargs.pop('form_kwargs', None)
        if self.form_kwargs is not None:
            self.form = wraps(self.form)(partial(self.form, **self.form_kwargs))

        super(FormKwargsFormsetMixin, self).__init__(*args, **kwargs)


class FormKwargsNestedFormsetMixin(BaseNestedFormset, FormKwargsFormsetMixin):
    """
    Версия предыдущего миксина для формсета с вложенными формсетами.

    Осуществляет "прокидывание" аргумента form_kwargs во вложенные формсеты.

    """
    def add_fields(self, form, index):

        # allow the super class to create the fields as usual
        super(BaseNestedFormset, self).add_fields(form, index)

        if hasattr(self, 'form_kwargs'):
            form.nested = self.nested_formset_class(
                instance=form.instance,
                data=form.data if form.is_bound else None,
                files=form.files if form.is_bound else None,
                prefix='%s-%s' % (
                    form.prefix,
                    self.nested_formset_class.get_default_prefix(),
                ),
                form_kwargs=self.form_kwargs
            )
        else:
            form.nested = self.nested_formset_class(
                instance=form.instance,
                data=form.data if form.is_bound else None,
                files=form.files if form.is_bound else None,
                prefix='%s-%s' % (
                    form.prefix,
                    self.nested_formset_class.get_default_prefix(),
                ),
            )
