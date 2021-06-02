# -*- coding: utf-8 -*-
{
    'name': "Staples Account",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Jothimani Rajagopal / Clearview Infotech",
    'website': "http://www.clearviewinfotech.com",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['sale', 'account', 'staples_web'],
    'data': [
        'views/account_views.xml',
        'views/templates.xml',
        'views/account_report.xml',
        'report/report_invoice.xml',
        'data/data.xml',
    ],
}
