{
    "name" : "Hospital Management System" ,
    "author" : "cygnus one" ,
    "license" : "LGPL-3" ,
    "version" : "17.0.1.0" ,
    "depends" : [
        "mail",
        "product",
        "account",
        "hr"
    ],
    "data" : [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml" ,
        "views/patient_views.xml",
        "views/employee_view.xml",
        "views/patient_readonly_views.xml",
        "views/appoinment_views.xml",
        "views/appoinment_line_views.xml",
        "views/patient_tag_views.xml",
        "views/account_move_views.xml",
        "views/menu.xml",
    ]
}
