{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión de biblioteca, socios y préstamos',
    'depends': ['base', 'contacts'], 
    'data': [
        #'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/library_book_views.xml',
        'views/library_menus.xml',
        # Ubicacion de vistas y elementos de seguridad
    ],
    'installable': True,
    'application': True,
}