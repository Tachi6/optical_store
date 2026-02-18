{
    'name': 'Optometry Visits',
    'version': '17.0.1.0.0',
    'category': 'Services/Healthcare',
    'summary': 'Manage optometry visits',
    'description': '''
Create and manage optometry visits. Includes refraction.
    ''',
    'author': 'David Gonzalez',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'assets': {
        'web.assets_backend': [
            'optical/static/src/js/add_plus_symbol_widget.js',
            'optical/static/src/js/add_degree_symbol_widget.js',
        ],
    },
    'data': [
        'security/optical_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/optical_visit_view.xml',
        'views/optical_visit_menu.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}

