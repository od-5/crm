import datetime
from apps.landing.models import Setup

__author__ = 'alexy'


def paginator_link(request):
    get_data = request.GET.copy()
    filtered_url = '?'
    for i in get_data:
        if i != 'page':
            filtered_url += u'%s=%s&' % (i, get_data[i])
    return {
        'URL_WITH_FILTER': filtered_url
    }


def site_setup(request):
    if not request.subdomain:
        main_page = True
    else:
        main_page = False
    return {
        'CURRENT_YEAR': datetime.datetime.now(),
        'MAIN_PAGE': main_page,
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
