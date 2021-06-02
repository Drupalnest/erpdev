# -*- coding: utf-8 -*-
{
    'name': "Staples Sale",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Jothimani Rajagopal / Clearview Infotech",
    'website': "http://www.clearviewinfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'staples_base', 'staples_fob', 'staples_shipvia', 'staples_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        # 'views/templates.xml',
        # 'views/fob_views.xml',
        # 'views/ship_via_views.xml',
        'views/sale_views.xml',
        'views/account_views.xml',
        'views/res_partner_views.xml',
        'report/sale_report_templates.xml',
        # 'report/report_picking_operations.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
