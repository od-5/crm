# coding=utf-8

__author__ = 'alexy'

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': u'CMS',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    'MENU_EXCLUDE': ('auth.group',),
    'MENU': (
        'sites',
        {'label': u'Перейти на сайт', 'icon': 'icon-eye-open', 'url': '/'},
        {'label': u'Пользователи', 'icon': 'icon-user', 'models': ('core.user',)},
        {'label': u'Настройки', 'icon': 'icon-cog', 'models': ('landing.setup',)},
        {'label': u'Заявки', 'icon': 'icon-user', 'models': ('ticket.ticket', 'ticket.excurseticket', 'ticket.groupticket')},
        {'label': u'Продажи', 'icon': 'icon-user', 'models': ('ticket.sale',)},
        {'label': u'Города', 'app': 'city',},
        {'label': u'Клиенты', 'app': 'client',},
        {'label': u'Монтажники', 'app': 'adjuster',},
    ),
}
