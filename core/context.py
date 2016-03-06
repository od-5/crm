import datetime
from .models import Setup

__author__ = 'alexy'


def site_setup(request):
    try:
        qss = Setup.objects.all().first()
    except:
        qss = None
    if request.path == '/':
        home = True
    else:
        home = False
    return {
        'SETUP': qss,
        'CURRENT_YEAR': datetime.datetime.now(),
        'HOME_PAGE': home,
    }


class SubdomainMiddleware:
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0]
            if (subdomain.lower() == 'www'):
                subdomain = None
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = None
            domain = request.get_host()

        request.subdomain = subdomain
        request.domain = domain
