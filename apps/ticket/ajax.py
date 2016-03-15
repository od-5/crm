# coding=utf-8
from annoying.decorators import ajax_request
from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from apps.city.models import City
from apps.landing.models import Setup
from .forms import TicketForm

__author__ = 'alexy'


@ajax_request
@csrf_exempt
def ticket(request):
    # try:
    #     email = Setup.objects.all()[0].email
    # except:
    # email = 'od-5@yandex.ru'
    subdomain = request.subdomain
    email = None
    if subdomain:
        city = get_object_or_None(City, slug=subdomain)
        try:
            email = Setup.objects.get(city=city).email
            if not email:
                email = Setup.objects.filter(city__isnull=True).first().email
        except:
            email = Setup.objects.filter(city__isnull=True).first().email
    else:
        email = Setup.objects.filter(city__isnull=True).first().email
    print 'step 1'
    if request.method == "POST":
        form = TicketForm(data=request.POST)
        print form
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.type = 0
            ticket.save()
            theme = request.POST.get('theme')
            mail_title_msg = u'На nadomofone.ru оставлено сообщение: %s' % theme
            if ticket.text:
                if ticket.city:
                    message = u'Имя: %s\nТелефон: %s\nГород: %s\nСообщение: %s\n' % (ticket.name, ticket.phone, ticket.city, ticket.text)
                else:
                    message = u'Имя: %s\nТелефон: %s\nСообщение: %s\n' % (ticket.name, ticket.phone, ticket.text)
            else:
                if ticket.city:
                    message = u'Имя: %s\nТелефон: %s\nГород: %s' % (ticket.name, ticket.text, ticket.city)
                else:
                    message = u'Имя: %s\nТелефон: %s\n' % (ticket.name, ticket.text)
            if email:
                send_mail(
                    mail_title_msg,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email, ]
                )
            return {
                'success': 'Message send'
            }
        else:
            return {
                'error': 'Error!! Not send'
            }
        print 'step 2'
    else:
        return {
            'error': 'request.method not post'
        }
