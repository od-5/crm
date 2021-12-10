import json
import logging
import urllib

from django.core.cache import caches


logger = logging.getLogger('apps')


def showNode(node, level):
    if type(node) == dict:
        for i in node.keys():
            if type(node[i]) in (dict, list, tuple):
                print(' '.join([' ' * 4 * level,
                                 i,
                                 str(type(node[i])),
                                ]))
            else:
                print(' '.join([' ' * 4 * level,
                                 i,
                                 str(type(node[i])),
                                 ': ',
                                 '%s' % node[i],
                                ]))
            showNode(node[i], level + 1)
    if type(node) in (list, tuple):
        for i in node:
            showNode(i, level + 1)


# It's implemented in Werkzeug as follows:
def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, bytes):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(path, '/%')
    qs = urllib.parse.quote_plus(qs, ':&=')
    return urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))


def getJSON(address, key):
    """Get latitude longitude from Yandex.maps service.
    """
    yandexGeotaggingApi = url_fix("http://geocode-maps.yandex.ru/1.x/" + \
            "?format=json&geocode=%s&apikey=%s" % (address, key))
    f = urllib.request.urlopen(yandexGeotaggingApi)
    return f.read()


def listGeoObject(address, key):
    response = getJSON(address, key)
    data = json.loads(response)['response']['GeoObjectCollection']
    if data['metaDataProperty']['GeocoderResponseMetaData']['found']:
        geoObjects = data['featureMember']
        for obj in geoObjects:
            yield obj['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    else:
        print('Nothing to find')


def getpointGeoObject(address, key):
    logger.debug(f'getpointGeoObject: receive response')
    response = getJSON(address, key)
    data = json.loads(response)['response']['GeoObjectCollection']
    logger.debug(f'response data: {response}')
    if data['metaDataProperty']['GeocoderResponseMetaData']['found']:
        geoObjects = data['featureMember']
        for obj in geoObjects:
            yield obj['GeoObject']['Point']['pos']
    else:
        logger.debug(f'Nothing to find')


def geocode(key, address):
    logger.debug(f'Start geocoding for "{address}"')
    cache = caches['yandex-map']
    pos = cache.get(address)
    if not pos:
        logger.debug(f'Cache not found, response to Yandex.Map')
        response = getpointGeoObject(address, key)
        pos = list(response)[0].split(' ')
        cache.set(address, pos, None)
    else:
        logger.debug(f'Get position from cache')
    return pos


if __name__ == '__main__':
    address = "Волгоград Богданова 28"
    key = "ANpUFEkBAAAAf7jmJwMAHGZHrcKNDsbEqEVjEUtCmufxQMwAAAAAAAAAAAAvVrub" + \
          "VT4btztbduoIgTLAeFILaQ=="
    print(geocode(key, address))
