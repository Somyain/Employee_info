from odoo import _, api, models, fields 
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EmployeeInfo(models.Model):
    _name = 'employee.info'
    _description = 'Employee Information'

    _rec_name = 'reference_number'
    reference_number = fields.Char(string='Sequence',copy=False,default=lambda self:_("New"),readonly=True)
    _order = 'reference_number desc'
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
    
    def _send_birthday_followup(self):
        today = fields.Date.today()
        employees = self.search([
            ('date_of_birth', '!=', False),
            ('partner_email', '!=', False),
        ])
        template = self.env.ref(
            'my_custom_module.birthday_mail_template_abc',
        )
        if not template:
            return
        for employee in employees:
            dob = employee.date_of_birth
            if dob.day == today.day and dob.month == today.month:
                template.send_mail(
                    employee.id,
                    force_send=True
                )

    @api.constrains('partner_email')
    def _check_partner_email(self):
        for record in self:
            if not record.partner_email:
                continue
            email = record.partner_email
            if email != email.lower():
                raise UserError("Email must be lowercase")
            if email.count('@') != 1:
                raise UserError("Email must contain exactly one '@'")
            if ' ' in email:
                raise UserError("Email must not contain spaces")
            username_part, domain = email.split('@')
            valid_chars = set(".-_")
            if not username_part or not domain:
                raise UserError("Username and domain cannot be empty")
            if username_part[0].isdigit() or username_part[0] in valid_chars:
                raise UserError("Username cannot start with number or special character")
            if not all(ch.islower() or ch.isdigit() or ch in valid_chars for ch in username_part):
                raise UserError("Username contains invalid characters")
            if '.' not in domain:
                raise UserError("Domain must contain '.'")
            domain_parts = domain.split('.')
            domain_name = domain_parts[0]
            domain_ext = domain_parts[-1]
            if len(domain_ext) < 2:
                raise UserError("Invalid domain extension")
            if not domain_name.isalpha():
                raise UserError("Domain name must contain only letters")
            if domain.startswith('.') or domain.endswith('.'):
                raise UserError("Domain cannot start or end with '.'")
        
    # @api.model
    # def create_employee_via_api(self, vals):
    #     employee = self.create(vals)
    #     return {
    #         'id': employee.id,
    #         'reference_number': employee.reference_number,
    #         'name': employee.emp_name
    #     }

    @api.constrains('partner_email')
    def _check_unique_partner_email(self):
        for record in self:
            if not record.partner_email:
                continue

            duplicate = self.search([
                ('partner_email', '=', record.partner_email),
                ('id', '!=', record.id)
            ], limit=1)

            if duplicate:
                raise ValidationError(
                    _("An employee with email '%s' already exists.") 
                    % record.partner_email
                )