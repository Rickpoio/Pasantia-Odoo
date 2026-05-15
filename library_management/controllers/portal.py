from odoo import http
from odoo.http import request

class LibraryPortal(http.Controller):

    @http.route(['/my/loans'], type='http', auth="user", website=True)
    def portal_my_loans(self):
        # Obtenemos los préstamos del socio actual (usuario logueado)
        partner = request.env.user.partner_id
        loans = request.env['library.loan'].search([
            ('partner_id', '=', partner.id)
        ], order='loan_date desc')
        
        return request.render("library_management.portal_my_loans_template", {
            'loans': loans,
            'page_name': 'my_loans',
        })

    @http.route(['/my/loans/renew/<model("library.loan"):loan>'], type='http', auth="user", website=True)
    def portal_loan_renew(self, loan):
        # Lógica de renovación: solo si no está vencido
        if loan.state == 'ongoing':
            # Extendemos la fecha (por ejemplo, 7 días más desde hoy)
            from datetime import timedelta
            loan.loan_date = loan.loan_date + timedelta(days=7)
            return request.redirect('/my/loans?message=success')
        return request.redirect('/my/loans?message=error')