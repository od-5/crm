# coding=utf-8
from django import template
from apps.adjuster.models import AdjusterTask
from apps.adjustertask.task_calendar import TaskCalendar
from apps.manager.models import Manager

register = template.Library()


@register.simple_tag
def calendar(user, year, month):
    task_qs = AdjusterTask.objects.order_by('date').filter(
        date__year=year, date__month=month, is_closed=False
    )
    if user.type == 2:
        task_qs = task_qs.filter(adjuster__city__moderator=user)
    elif user.type == 4:
        task_qs = task_qs.filter(adjuster__user=user)
    elif user.type == 5:
        manager = Manager.objects.get(user=user)
        task_qs = task_qs.filter(adjuster__city__moderator=manager.moderator)
    cal = TaskCalendar(task_qs, ('ru_RU', 'UTF-8')).formatmonth(year, month)
    return cal
