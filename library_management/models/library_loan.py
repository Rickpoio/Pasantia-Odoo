from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _inherit = ['mail.thread']
    _description = 'Registro de Préstamos'
    

    # Relaciones y Campos
    book_id = fields.Many2one(
        'library.book', 
        string='Libro', 
        required=True, 
        domain=[('is_available', '=', True)]
    )


    partner_id = fields.Many2one('res.partner', string='Socio', required=True)
    loan_date = fields.Date(string='Fecha de Préstamo', default=fields.Date.today())
    return_date = fields.Date(string='Fecha de Devolución')
    state = fields.Selection([
        ('ongoing', 'En Curso'),
        ('returned', 'Devuelto'),
        ('expired', 'Vencido')
    ], string='Estado', default='ongoing', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        
        for vals in vals_list:
            partner_id = vals.get('partner_id')
            if partner_id:
                active_loans = self.search_count([
                    ('partner_id', '=', partner_id),
                    ('state', '=', 'ongoing')
                ])
                if active_loans >= 5:
                    raise ValidationError(
                        "¡Regla de Negocio: El socio ya tiene 5 préstamos activos! "
                        "Debe devolver un libro antes de solicitar otro."
                    )
            
            
            book_id = vals.get('book_id')
            if book_id:
                book = self.env['library.book'].browse(book_id)
                if not book.is_available:
                    raise ValidationError(
                        "El libro seleccionado no está disponible en este momento."
                    )
                
                book.is_available = False
        
        
        return super(LibraryLoan, self).create(vals_list)

    def _cron_check_expired_loans(self):
        """
        Método llamado por la Acción Programada (Cron).
        Busca préstamos de más de 30 días y envía correos.
        """
        thirty_days_ago = fields.Date.today() - timedelta(days=30)
        # Buscar préstamos en curso creados hace más de 30 días
        expired_loans = self.search([
            ('state', '=', 'ongoing'),
            ('loan_date', '<', thirty_days_ago)
        ])
        
        for loan in expired_loans:
            loan.state = 'expired'
            # Enviar correo usando la plantilla 
            template = self.env.ref('library_management.email_template_loan_expired', raise_if_not_found=False)
            if template:
                loan.message_post_with_source(
                    template,
                    subtype_xmlid='mail.mt_comment',
                )
    
    def action_return_book(self):
        """
        Método manual de devolución que libera el cupo del socio
        y devuelve el libro al estado Disponible.
        """
        for record in self:
            if record.state == 'returned':
                continue
                
            record.write({
                'state': 'returned',
                'return_date': fields.Date.today()
            })
            # El libro vuelve a estar disponible para otros préstamos
            if record.book_id:
                record.book_id.is_available = True