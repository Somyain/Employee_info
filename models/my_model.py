from odoo import _, api, models, fields 
from odoo.exceptions import UserError

class EmployeeInfo(models.Model):
    _name = 'employee.info'
    _description = 'Employee Information'

    _rec_name = 'reference_number'
    reference_number = fields.Char(string='Sequence',copy=False,default=lambda self:_("New"),readonly=True)
    emp_name = fields.Char(required=True)
    gender = fields.Selection(
        [('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
        ], string='Gender')
    phone = fields.Char(string="Phone", help="Enter phone number in international format")
    partner_email = fields.Char(string="Email")
    date_of_birth = fields.Date('Date of Birth')
    age = fields.Integer('Age', compute='_compute_age', store=False)
    joining_date = fields.Datetime(string="Joining Date")
    description = fields.Text(string="Description")
    employee_image = fields.Binary(string="Employee Image")
    employee_salary = fields.Integer( string='Employee Monthly income', required=True, tracking=True, help="Basic salary of the employee.")
    per_month_salary = fields.Integer('Salary per/month',compute = '_compute_salary',store=False)
    job_title = fields.Selection(
        [('software_dev','Software Developer'),
        ('software_test','Software tester'),
        ('hr','HR'),
        ('ai/ml','AI/ML'),
        ('odoo_professional','Odoo Professional'),
        ('none','None'),
        ] , string="job Title")
    work_location = fields.Selection(
        [('jaipur','Jaipur'),
        ('ahemdabad','Ahemdabad')
        ],string="Work Location")
    emergency_con = fields.Char(string="Emergency contact", help="Enter phone number in international format")
    emergency_con_name = fields.Char(string="Emergency contact name")
    emergency_con_relation = fields.Char(string="Relation with emergency contact")
    user_id = fields.Many2one('res.users',default=lambda self:self.env.user)

    department_id = fields.Many2one('employee.department',string="Department")
    employee_skill_ids = fields.One2many('employee.skill', 'employee_id', string="Employee Skills")


    @api.model_create_multi
    def create(self, vals_list):
        """Create records using provided values."""
        for vals in vals_list:
            if vals.get('reference_number', _('New')) == _('New'):
                vals['reference_number'] = self.env['ir.sequence'].next_by_code('employee.info') or _('New')
        return super(EmployeeInfo,self).create(vals_list)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0

    @api.onchange('employee_salary')
    def _compute_salary(self):
        for record in self:
            if record.employee_salary:
                record.per_month_salary = record.employee_salary / 12
            else :
                record.per_month_salary = 0

    def copy(self, default=None):
        default = dict(default or {})
        default['emp_name'] = ''
        default['partner_email'] = ''
        return super().copy(default)
    
    def write(self, vals):
        if 'job_title' in vals:
            vals['description'] = f"Job title updated to {vals['job_title']}"
        return super(EmployeeInfo, self).write(vals)

    def unlink(self):
        for record in self:
            if record.job_title != 'none':
                raise UserError(_(f"Record cannot be delete,\nContains a Job Title {self.job_title}"))
        return super(EmployeeInfo ,self).unlink()