from odoo import models, fields

class EmployeeDepartment(models.Model):
    _name = 'employee.department'
    _description = 'Employee\'s Department'

    _rec_name = "dep_name"
    dep_name = fields.Char(required=True)