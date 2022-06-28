# -*- coding: utf-8 -*-
{
    'name': "Nasra Work Schedule",

    'summary': """
    module for customzation of work schedule and salary rule on late early absence
    """,

    # any module necessary for this one to work correctly
    'depends': ['base','hr','resource','nasra_hr_late_early_absence'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/resource_calendar.xml',
        'views/days_off.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
