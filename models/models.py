# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import sys, numbers, string
import json

# Lista de acceso
class Acceso(models.Model):
    _name = 'gdu.acceso.logs'
    _description = 'GDU Acceso Logs'
    _rec_name = 'fullname'
    fullname = fields.Char(string="Nombre y Apellidos")
    #nombre = fields.Char(string="Nombre")
    #pellidos = fields.Char(string="Apellidos")
    area = fields.Char(string="Apellidos")
    #time_access = fields.Datetime('Fecha de acceso')
    hora_acceso = fields.Datetime('Hora de entrada', default=lambda self: fields.Datetime.now())
    ci = fields.Char(string="CI", size=11)
    # new_field = fields.Char(string="", required=False, )
    def f_search(self):
        persona = self.env['gdu.base.persona'].search([('ci', '=', str(self.cod_barras))])
        #res.update({'warning': {'title': 'Warning !', 'message': 'Nombre: ' + str(persona.nombre)}})
        #print('search()', persona, persona.nombre)
        title = "Codigo de Barras"
        message = "Persona encontrada: "+str(persona.nombre)
        self.nombre = persona.nombre
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
            }
        }

        #return{'warning': {'title': 'Warning !', 'message': 'Nombre: ' + persona.nombre}}

# Prueba de Escaneo
class Escaneo(models.TransientModel):
    _name = 'gdu.acceso.escaner'
    _description = 'GDU Acceso Scan'
    # _rec_name ='cod_barras'
    cod_barras = fields.Char(string="Código de barras", size=11, store=False)
    nombre = fields.Char(string="", readonly=True)
    tipo_persona = fields.Char(string="", readonly=True)
    html = fields.Html(readonly=True)
    #es_profesor = fields.Boolean('¿Es profesor?', readonly=True)


    def f_search(self):
        persona = self.env['gdu.base.persona'].search([('ci', '=', str(self.cod_barras))])
        #res.update({'warning': {'title': 'Warning !', 'message': 'Nombre: ' + str(persona.nombre)}})
        #print('search()', persona, persona.nombre)
        title = "Codigo de Barras"
        message = "Persona encontrada: "+str(persona.nombre)
        self.nombre = persona.nombre
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
            }
        }

        #return{'warning': {'title': 'Warning !', 'message': 'Nombre: ' + persona.nombre}}

    @api.onchange('cod_barras')
    def onchange_cod_barras(self):
        texthtml = ""

        for record in self:
            if str(record.cod_barras).isnumeric() and len(record.cod_barras)==11:
                #_logger.info('Entro al if, cod_barras %s' % record.cod_barras)
                #_logger.info('Count, cod_barras %s' % len(record.cod_barras))
                persona = self.env['res.partner'].search_read([('carne_id', '=', str(record.cod_barras)),('active', 'in', [True,False])]) or []
                active = False #if persona.active=="false" else True
                #id = persona[0].get('id', 0)
                #print(persona)
                #print(type(persona))
                if len(persona):
                    persona = persona[0]
                    texthtml += "<p class='text-secundary'>" + str(record.cod_barras) + "</p>"
                    texthtml += "<p class='text-success'><i class='fa fa-user fa-3x'></i><h4>"+str(persona['name'])+"</h4></p>"

                    if persona['is_student']:
                        texthtml += "<p class='text-secundary'> Estudiante, Año: "+str(persona['career_year'])+"</p>"
                    if persona['is_work']:
                        texthtml += "<p class='text-secundary'> Trabajador </p>"
                    if persona['is_professor']:
                        texthtml += "<p class='text-secundary'> Profesor </p> "

                    if persona['career_id']:
                        print(persona['career_id'])
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-book text-info'></i> "+str(persona['career_id'][1])+"</h5>"
                    if persona['active']:
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-check-circle-o text-success'></i> Activo</h5>"
                    else:
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-ban text-danger'></i> Baja </h5>"
                    if persona['is_scholarship']:
                         texthtml += "<h5 class ='channel_name'><i class ='fa fa-check-circle-o text-success'></i> Becado </h5>"


                    record.html = texthtml
                    if persona['active']:
                        self.env['gdu.acceso.logs'].create({'ci': record.cod_barras, 'fullname': f"{persona['name']}"})
                    #record.nombre = persona.name
                else:
                    texthtml += "<p>ID:"+str(record.cod_barras)+"</p>"
                    texthtml += "<p class='text-danger h3'><i class='fa fa-ban'> ¡Usuario no identificado!</p>"
                    record.html = texthtml
                record.cod_barras = ""
            else:
                record.nombre = ""
                record.tipo_persona = ""
                record.cod_barras = ""


    def limpia_cod_barras(self):
        self.cod_barras = "ahh bueno!"



# @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


