from odoo import _, api, models, fields

class EmployeeInfo(models.Model):
   _name = 'employee.info'
   _description = 'Employee Information'

   _rec_name = 'reference_number'
   reference_number = fields.Char(string='Sequence',copy=False,default=lambda self:_("New"),readonly=True, required=True)
   emp_name = fields.Char()
   age = fields.Integer(string="Age")
   gender = fields.Selection(
       [('male', 'Male'), 
        ('female', 'Female'), 
        ('other', 'Other')
        ], string='Gender')   
   phone = fields.Char(string="Phone", help="Enter phone number in international format")   
   partner_email = fields.Char(string="Email")
   dob = fields.Date(string="DOB")
   joining_date = fields.Datetime(string="Joining Date")
   description = fields.Text(string="Description")
   employee_image = fields.Binary(string="Employee Image")
   employee_salary = fields.Integer( string='Employee Monthly income', required=True, tracking=True, help="Basic salary of the employee.")
   job_title = fields.Selection(
       [('software_dev','Software Developer'),
        ('software_test','Software tester'),
        ('hr','HR'),
        ('ai/ml','AI/ML'),
        ('odoo_professional','Odoo Professional')
        ] , string="job Title")
   work_location = fields.Selection(
       [('jaipur','Jaipur'),
        ('ahemdabad','Ahemdabad')
        ],string="Work Location")
   emergency_con = fields.Char(string="Emergency contact", help="Enter phone number in international format")
   emergency_con_name = fields.Char(string="Emergency contact name")
   emergency_con_relation = fields.Char(string="Relation with emergency contact")
   user_id = fields.Many2one('res.users',default=lambda self:self.env.user)

   @api.model_create_multi
   def create(self, vals_list):
       """Create records using provided values."""
       for vals in vals_list:
           if vals.get('reference_number', _('New')) == _('New'):
               vals['reference_number'] = self.env['ir.sequence'].next_by_code('employee.registration') or _('New')
       return super(EmployeeInfo,self).create(vals_list)