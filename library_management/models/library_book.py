from odoo import models, fields, api
from datetime import date

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Catálogo de Libros'

    name = fields.Char(string="Título", required=True)
    author_id = fields.Many2one('res.partner', string="Autor", domain=[('is_company', '=', False)])
    isbn = fields.Char(string="ISBN")
    publication_date = fields.Date(string="Fecha de Publicación")
    is_available = fields.Boolean(string="Disponible", default=True)
    
    # REQUERIMIENTO: Cálculo de Antigüedad
    years_since_publication = fields.Integer(
        string="Años desde publicación", 
        compute="_compute_years_since_publication",
        store=True
    )

    @api.depends('publication_date')
    def _compute_years_since_publication(self):
        today = date.today()
        for record in self:
            if record.publication_date:
                # Calculamos la diferencia de años
                record.years_since_publication = today.year - record.publication_date.year
            else:
                record.years_since_publication = 0