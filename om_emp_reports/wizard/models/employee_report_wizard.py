import io
import base64
import xlsxwriter
from odoo import models, fields

class EmployeeReportWizard(models.TransientModel):
    _name = 'employee.report.wizard'
    _description = 'Employee Report Wizard'

    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel')
    ], string="Report Type", required=True)

    employee_id = fields.Many2one('employee.management', string="Employee")

    def action_generate_pdf(self):
        self.ensure_one()
        return self.env.ref('om_emp_reports.employee_pdf_report').report_action(self.employee_id)

    def action_generate_excel(self):
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Employees')

        sheet.write(0, 0, 'Name')
        sheet.write(0, 1, 'Email')
        sheet.write(0, 2, 'Phone')
        sheet.write(0, 3, 'Department')

        employees = self.env['employee.management'].search([])

        row = 1
        for emp in employees:
            sheet.write(row, 0, emp.name or '')
            sheet.write(row, 1, emp.work_email or '')
            sheet.write(row, 2, emp.work_phone or '')
            sheet.write(row, 3, emp.department_id.name or '')
            row += 1

        workbook.close()
        output.seek(0)
        
        file_data = base64.b64encode(output.read())
        
        attachment = self.env['ir.attachment'].create({
            'name': 'employees.xlsx',
            'datas': file_data,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (attachment.id),
            'target': 'self',
        }
