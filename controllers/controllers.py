# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class GduAcceso(http.Controller):
    @http.route('/gdu_acceso/gdu_acceso/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/gdu_acceso/qr/<code>', auth='public')
    def QR_scaner(self, code, **kw):
        try:
            persona = http.request.env['gdu.base.persona'].sudo().search_read([('ci', '=', str(code)),('active', 'in', [True,False])])[0]
            print(persona['id'])
            print(f'tiene id {persona["id"]}')
            id = persona.get('id', 0)
            print(id)
            if id:
                print(f'tiene id {persona["id"]}')
                http.request.env['gdu.acceso.logs'].sudo().create({'ci': code, 'fullname': f"{persona['nombre']} {persona['apellidos']}"})
                return f"Universidad de Oriente<br />Verificación por Código QR <br />ID: {code} <br /> {persona['nombre']} {persona['apellidos']}"
            else:
                return f"Universidad de Oriente<br />Verificación por Código QR <br />ID: {code} <br /> ¡Ningún usuario encontrado!"
        except:
            return f"Universidad de Oriente<br />Verificación por Código QR <br />ID: {code} <br /> <span class='text-danger' style='color:red'>¡<i class='fa fa-ban'></i>Usuario ageno al centro!</span>"


    @http.route('/gdu_acceso/qr2/<code>', auth='public')
    def QR_scaner2(self, code, **kw):
        try:
            persona = http.request.env['gdu.base.persona'].sudo().search_read(
                [('ci', '=', str(code)), ('active', 'in', [True, False])],
                ['id','name','active','nombre','apellidos','es_profesor'])[0]
            print(persona['id'])
            print(f'tiene id {persona["id"]}')
            id = persona.get('id', 0)
            print(id)
            if id:
                print(f'tiene id {persona["id"]}')
                http.request.env['gdu.acceso.logs'].sudo().create(
                    {'ci': code, 'fullname': f"{persona['nombre']} {persona['apellidos']}"})
                return request.render('gdu_acceso.qr_page', {'persona': persona})
            else:
                return request.render('gdu_acceso.qr_page', {'persona': None, 'code': code})
        except:
            return request.render('gdu_acceso.qr_page', {'persona': None, 'code': code})
            #return f"Universidad de Oriente<br />Verificación por Código QR <br />ID: {code} <br /> <span class='text-danger' style='color:red'>¡<i class='fa fa-ban'></i>Usuario ageno al centro!</span>"

#     @http.route('/gdu_acceso/gdu_acceso/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gdu_acceso.listing', {
#             'root': '/gdu_acceso/gdu_acceso',
#             'objects': http.request.env['gdu_acceso.gdu_acceso'].search([]),
#         })

#     @http.route('/gdu_acceso/gdu_acceso/objects/<model("gdu_acceso.gdu_acceso"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gdu_acceso.object', {
#             'object': obj
#         })
