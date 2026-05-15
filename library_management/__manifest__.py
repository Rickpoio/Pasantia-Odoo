{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión de biblioteca, socios y préstamos',
    'depends': ['base', 'contacts', 'mail','website'], 
    'data': [
        'security/ir.model.access.csv',
        'security/library_security.xml',
        'views/res_partner_views.xml',
        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/library_loan_templates.xml',
        'views/portal_templates.xml',
        'views/portal_menu_ext.xml',
        'views/library_menus.xml',
        'data/library_cron.xml'
         #'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}