# coding=utf-8
from django import template
from apps.adjuster.models import AdjusterTask
from apps.adjustertask.task_calendar import TaskCalendar

register = template.Library()


@register.simple_tag
def calendar(year, month):
    task_qs = AdjusterTask.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = TaskCalendar(task_qs, ('ru_RU', 'UTF-8')).formatmonth(year, month)
    return cal
