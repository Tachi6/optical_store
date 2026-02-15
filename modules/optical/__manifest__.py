# -*- coding: utf-8 -*-
{
    'name': "Optometry Visits",

    'summary': "Manage optometry visits",

    'description': """
Create and manage optometry visits. Includes refraction.
    """,

    'author': "David Gonzalez",
    # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts'],

    # assets
    'assets': {
        'web.assets_backend': [
            'optical/static/src/js/add_plus_symbol_widget.js',
            'optical/static/src/js/add_degree_symbol_widget.js',
        ],
    },

    # always loaded
    'data': [
        'security/optical_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/optical_visit_view.xml',
        'views/menu.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}

