# -*- coding: utf-8 -*-
{
    'name': "staples_stock",
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
    'depends': ['staples_web', 'staples_sale', 'stock'],
    'data': [
        'views/templates.xml',
        'views/stock_picking_views.xml',
        'views/report_stockpicking_operations.xml',
    ],
}
