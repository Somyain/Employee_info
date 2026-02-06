{
    'name': "Odoo",
    'version': '1.0.0',
    'category': 'Software Developer',
    'description': """ 
                    Working at codetrade.io as Software Developer Intern
    """,
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/employee_field_security_groups.xml',

        'views/ir_sequence_data.xml',

        'data/employee.info.csv',
        'data/employee_data.xml',
        'data/employee_department.xml',

        'views/employee_menu.xml',
        'views/employee_views.xml',
    ],
    'author': "Somya",
    'installation':True,
    'appliation' :True,
    'auto-install':False,
}