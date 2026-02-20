from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class EmployeeAPI(http.Controller):

    @http.route('/api/employees',
                type='http',
                auth='user',
                methods=['GET'],
                csrf=False)
    def get_employees(self):

        employees = request.env['employee.info'].search([])

        data = [{
            "id": e.id,
            "reference": e.reference_number,
            "name": e.emp_name,
            "email": e.partner_email,
            "job_title": e.job_title,
            "salary": e.employee_salary,
        } for e in employees]

        return request.make_json_response(data)

    @http.route('/api/employees',
                type='http',
                auth='user',
                methods=['POST'],
                csrf=False)
    def create_employee(self):

        try:
            data = json.loads(request.httprequest.data or "{}")

            employee = request.env['employee.info'].create(data)

            return request.make_json_response({
                "status": "success",
                "id": employee.id,
                "reference": employee.reference_number
            }, status=201)

        except Exception:
            _logger.exception("Create Employee API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)

    @http.route('/api/employees/<int:employee_id>',
                type='http',
                auth='user',
                methods=['PUT'],
                csrf=False)
    def update_employee(self, employee_id):

        try:
            data = json.loads(request.httprequest.data or "{}")

            employee = request.env['employee.info'].browse(employee_id)

            if not employee.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Employee not found"
                }, status=404)

            employee.write(data)

            return request.make_json_response({
                "status": "success",
                "message": "Employee updated"
            })

        except Exception:
            _logger.exception("Update Employee API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)


    @http.route('/api/employees/<int:employee_id>',
                type='http',
                auth='user',
                methods=['DELETE'],
                csrf=True)
    def delete_employee(self, employee_id):

        try:
            employee = request.env['employee.info'].browse(employee_id)

            if not employee.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Employee not found"
                }, status=404)

            employee.unlink()

            return request.make_json_response({
                "status": "success",
                "message": "Employee deleted"
            })

        except Exception:
            _logger.exception("Delete Employee API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)