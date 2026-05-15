from odoo import models, fields, api
from datetime import date

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Catalogo de Libros'

    # Campos basicos para la ficha del libro
    name = fields.Char(string="Titulo", required=True)
    author_id = fields.Many2one('res.partner', string="Autor")
    isbn = fields.Char(string="ISBN")
    publication_date = fields.Date(string="Fecha de Publicacion")
    is_available = fields.Boolean(string="Disponible", default=True)
    
    # Campo calculado para almacenar los años transcurridos desde la publicacion
    years_since_publication = fields.Integer(
        string="Años desde publicacion", 
        compute="_compute_years_since_publication",
        store=True
    )

    @api.depends('publication_date')
    def _compute_years_since_publication(self):
        # Calcula la antiguedad restando el ano actual del ano de publicacion
        today = date.today()
        for record in self:
            if record.publication_date:
                record.years_since_publication = today.year - record.publication_date.year
            else:
                record.years_since_publication = 0