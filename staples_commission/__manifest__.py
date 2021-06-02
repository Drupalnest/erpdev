# -*- coding: utf-8 -*-
{
    'name': "staples_commission",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sales_team'],

    # always loaded
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/commission_release_seq.xml',
        'views/staples_commission_view.xml',
        'views/product_views.xml',
        'views/res_partner_view.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
        'views/commission_view.xml',
        'views/report_commission.xml',
        'wizard/invoice_wizard_views.xml',
    ],
}
