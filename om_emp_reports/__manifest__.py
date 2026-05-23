{
    'name': 'Employee Reports',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['om_hospital'], 
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'wizard/views/employee_report_wizard_view.xml',
        'reports/views/employee_report.xml',
    ],
    'installable': True,
}