# -*- coding: utf-8 -*-
{
    'name': "Nasra Hr Multi Approval Chain",
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','nasra_hr_self_service','nasra_hr_loan_correct','nasra_hr_holidays_multi_levels_approval'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_mission.xml',
        'views/hr_excuse.xml',
        'views/hr_loan.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
