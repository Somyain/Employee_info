from odoo import models, fields

class PatientInfo(models.Model):
   _name = 'employee.info'
   _description = 'Employee Information'

   emp_name = fields.Char()
   age = fields.Integer(string="Age")
   gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender')   
   phone = fields.Char(string="Phone", help="Enter phone number in international format")   
   partner_email = fields.Char(string="Email")
   dob = fields.Date(string="DOB")
   joining_date = fields.Datetime(string="Joining Date")
   description = fields.Text(string="Description")
   employee_image = fields.Binary(string="Employee Image")
   job_title = fields.Char(string="job Title")
   work_location = fields.Selection([('jaipur','Jaipur'),('ahemdabad','Ahemdabad')],string="Work Location")
   emergency_con = fields.Char(string="Emergency contact", help="Enter phone number in international format")
   emergency_con_name = fields.Char(string="Emergency contact name")
   emergency_con_relation = fields.Char(string="Relation with emergency contact")