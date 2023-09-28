# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class GduAcceso(http.Controller):
    @http.route('/gdu_acceso/qr/', auth='public')
    def index(self, **kw):
        return "Verificación de Solapín mediante código QR."

    @http.route('/gdu_acceso/qr/<code>', auth='public')
    def QR_scaner2(self, code, **kw):
        try:
            persona = http.request.env['res.partner'].sudo().search_read(
                [('carne_id', '=', str(code)), ('active', 'in', [True, False])])[0]
            print(persona['carne_id'])
            id = persona.get('carne_id', 0)
            if id:
                print(f'tiene carne_id {persona["carne_id"]}')
                http.request.env['gdu.acceso.logs'].sudo().create(
                    {'ci': code, 'fullname': f"{persona['name']}"}
                )
                return request.render('gdu_acceso.qr_page', {'persona': persona, 'code': code})
            else:
                return request.render('gdu_acceso.qr_page', {'persona': None, 'code': code})
        except:
            return request.render('gdu_acceso.qr_page', {'persona': None, 'code': code})
