from odoo import api, fields, models

class EmployeeManagement(models.Model):
    _name = "employee.management"
    _description = "Employee Manager"

    employee_id = fields.Char(string="Employee ID", required=True, default="New")
    name = fields.Char(string="Employee Name", required=True)
    work_address = fields.Char(string="Work Address")
    work_email = fields.Char(string="Work Email")
    work_phone = fields.Char(string="Work Phone")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", required=True)
    date_of_birth = fields.Date(string="DOB", required=True)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    job_id = fields.Many2one('hr.job', string="Job", required=True)
    private_address = fields.Char(string="Private Address")
    private_email = fields.Char(string="Private Email")
    private_phone = fields.Char(string="Private Phone")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('employee_id') or vals.get('employee_id') == 'New':
                vals['employee_id'] = self.env['ir.sequence'].next_by_code('employee.management')
        return super().create(vals_list)