# -*- coding: utf-8 -*-
# from odoo import http


# class GduAcceso(http.Controller):
#     @http.route('/gdu_acceso/gdu_acceso/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

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
