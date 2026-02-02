from odoo import models, fields

class EmployeeSkill(models.Model):
    _name = 'employee.skill'
    _description = 'Employee skills'
    
    skill_name = fields.Char(string="Skill Name",required = True)
    skill_level = fields.Selection(
        [('beginner','Beginner'),
         ('intermediate','Intermediate'),
         ('expert','Expert')],
         string="Skill level"
    )
    employee_id = fields.Many2one('employee.info',string="Employee")