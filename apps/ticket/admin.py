# coding=utf-8
from django.contrib import admin
from .models import Ticket
from django.forms import ModelForm
from suit.widgets import EnclosedInput, AutosizedTextarea


class TicketAdminForm(ModelForm):
    class Meta:
        widgets = {
            'comment': AutosizedTextarea,
            'ticket_comment': AutosizedTextarea,
        }


class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created', 'ticket_status', 'ticket_comment')
    list_filter = ['email', 'created', 'ticket_status']
    search_fields = ['email', ]
    date_hierarchy = 'created'
    fields = ('name', 'email', 'comment', 'sale', 'ticket_status', 'ticket_comment')
    form = TicketAdminForm

    def get_queryset(self, request):
        return self.model.objects.filter(sale=False)

    def suit_row_attributes(self, obj, request):
        css_class = {
            1: 'success',
            0: 'warning',
            2: 'error',
        }.get(obj.ticket_status)
        if css_class:
            return {'class': css_class, 'data': obj.name}


class Sale(Ticket):
    class Meta:
        proxy = True
        verbose_name = u'Продажа'
        verbose_name_plural = u'Продажи'


class SaleAdminForm(ModelForm):
    class Meta:
        widgets = {
            'price': EnclosedInput(append=u'руб.'),
            'comment': AutosizedTextarea,
            'sale_comment': AutosizedTextarea,
        }


class SaleAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        return self.model.objects.filter(sale=True)

    def has_add_permission(self, request, obj=None):
        return False

    def suit_row_attributes(self, obj, request):
        css_class = {
            2: 'success',
            1: 'warning',
            0: 'error',
        }.get(obj.sale_status)
        if css_class:
            return {'class': css_class, 'data': obj.name}

    list_display = ('name', 'email', 'price', 'sale_status', 'sale_comment')
    list_filter = ['sale_status',]
    search_fields = ['email', ]
    fields = ('name', 'email', 'comment', 'sale', 'sale_status', 'sale_comment', 'price')
    form = SaleAdminForm

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Sale, SaleAdmin)
