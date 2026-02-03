from odoo import models, fields , api

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

    @api.model
    def search(self ,employee , domain = None):
        domain = list(domain or [])
        if employee and employee.name:
            domain.append(('name', 'ilike', employee.name))
        result = self.env['employee.info'].search(domain)
        return result