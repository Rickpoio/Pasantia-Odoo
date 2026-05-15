from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Campo para identificar si es socio
    is_library_member = fields.Boolean(string="Es Socio de Biblioteca", default=False)
    
    #Campo que indique la fecha de alta
    membership_date = fields.Date(
        string = "Fecha de alta",
        default=fields.Date.context_today,
        help="Fecha de afiliacion a la biblioteca"
    )

    #Campo que contendra el codigo unico para un socio
    library_member_code = fields.Char(
        string="Codigo de Socio",
       readonly=True,
       copy=False,
       default="Nuevo"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_library_member') and vals.get('library_member_code', 'Nuevo') == 'Nuevo':
                vals['library_member_code'] = self.env['ir.sequence'].next_by_code('res.partner.library.seq') or 'LIB-TEMP'
        return super(ResPartner, self).create(vals_list)

    # Campo calculado para contar préstamos activos
    active_loan_count = fields.Integer(
        string="Préstamos Activos", 
        compute="_compute_active_loans"
    )

    def _compute_active_loans(self):
        for record in self:
            # Aquí contaremos los registros de préstamos que no estén devueltos
            # Por ahora lo dejamos en 0 hasta crear el modelo de préstamos
            record.active_loan_count = 0