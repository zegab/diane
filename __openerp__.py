# -*- coding: utf-8 -*-
{
    'name': "ISFATES DFHI Alumni Network",

    'summary': """ISFATES DFHI Extensions""",

    'description': """
        ISFATES DFHI Alumni Network Extensions
            - Extend Partner Model
            - My Account Page
            - Maps integration
            - Blog mods
    """,

    'author': "Gabriel Demmerle",
    'website': "http://www.isfates-dfhi-alumni.com",

    #'category': 'DIANE',
    'version': '0.1',

    'depends': ['base','website','contacts','crm','association','website_blog','mass_mailing'],

    'data': [
        'views/res_partner.xml',
        'views/association.xml',
        'views/website_blog.xml',
        'views/website_theme.xml',
        'views/website_menu.xml',
        'views/account_update.xml',
    ],
    'demo': [],

    'application': True,
}