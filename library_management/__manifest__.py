{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Gestión de biblioteca, socios y préstamos',
    'depends': ['base', 'contacts', 'mail'], 
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/library_book_views.xml',
        'views/library_loan_views.xml',
        'views/library_loan_templates.xml',
        'views/library_menus.xml',
        'data/library_cron.xml'
         #'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}