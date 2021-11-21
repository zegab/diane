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
    'version': '0.2',

    'depends': ['base','website','crm','association','website_blog','mass_mailing','hr_recruitment','website_hr_recruitment','mail','auth_signup'],


    'data': [
        'data/portal_data.xml',
        'data/job_notification.xml',
        'views/res_partner.xml',
##        'views/website_blog.xml',
        'views/website_menu.xml',
        'views/account_update.xml',
#        'views/alumni_search.xml',
#        'data/alumni_contact.xml',
#        'views/alumni_message.xml',
#        'views/alumni_map.xml',
#        'views/website_jobs.xml',
        'views/hr_recruitment.xml',
#        'views/signup_template.xml',
         'security/ir.model.access.csv',
    ],
    'demo': [],
    'assets': {
        'web.assets_frontend': [
            'diane/static/src/js/sorttable.js',
            'diane/static/src/js/messaging.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}