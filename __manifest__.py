{
    'name': "Odoo",
    'version': '1.0.0',
    'category': 'Software Developer',
    'description': """ 
                    Working at codetrade.io as Software Developer Intern
    """,
    'depends': ['base'],
    'data': [
        'security/ir_rule.xml',
        'security/employee_field_security_groups.xml',
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/ir_sequence_data.xml',
    ],
    'author': "Somya",
    'installation':True,
    'appliation' :True,
    'auto-install':False,
}