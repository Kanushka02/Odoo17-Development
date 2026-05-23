{
    "name" : "Sale Order Management System" ,
    "author" : "cygnus one" ,
    "license" : "LGPL-3" ,
    "version" : "17.0.1.0" ,
    "depends" : [
        'base','sale'
    ],
    "data" : [
        "security/sale_order_security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/menu.xml",
    ],
    'installable': True,
    'application': False,
}

