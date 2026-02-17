# -*- coding: utf-8 -*-
{
    'name': 'Custom Sales Export',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Export confirmed sales orders in CSV',
    'description': '''
Export confirmed sales orders to CSV format using account mapping from A3ConfigCuentas.xlsx.
    ''',
    'author': 'David Gonzalez',
    'website': 'https://www.yourcompany.com',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_sales_export_wizard_view.xml',
        'views/custom_sales_export_menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True
}