import re
from odoo import http
from odoo.http import request

class EmployeeWebsiteController(http.Controller):
    
    @http.route('/employee/info', type='http', auth='public', website=True)
    def employee_form(self, **kwargs):
        return request.render(
            'my_custom_module.employee_info_form_page',
            {
                'error': kwargs.get('error'),
                'success': kwargs.get('success'),
                'emp_name': kwargs.get('name'),
            }
        )

    @http.route('/employee/info/submit', type='http', auth='public', website=True, csrf=False)
    def submit_employee_info(self, **post):

        email = post.get('partner_email', '').strip()
        phone = post.get('phone', '').strip()

        email_regex = r'^[a-z][a-z0-9._-]*@[a-z]+\.[a-z]{2,}$'
        if not re.match(email_regex, email):
            return request.redirect('/employee/info?error=Invalid email format')

        if not phone.isdigit() or len(phone) != 10:
            return request.redirect('/employee/info?error=Phone must be exactly 10 digits')

        if not post.get('emp_name') or not post.get('employee_salary') or not post.get('gender'):
            return request.redirect('/employee/info?error=Please fill all required fields')

        if request.env['employee.info'].sudo().search(
            [('partner_email', '=', email)], limit=1
        ):
            return request.redirect('/employee/info?error=This email is already registered')

        request.env['employee.info'].sudo().create({
            'emp_name': post.get('emp_name'),
            'partner_email': email,
            'phone': phone,
            'gender': post.get('gender'),
            'job_title': post.get('job_title'),
            'employee_salary': post.get('employee_salary'),
            'description': post.get('description'),
        })

        return request.redirect(
            '/employee/info?success=1&name=%s' % post.get('emp_name')
        )