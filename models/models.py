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
                persona = self.env['gdu.base.persona'].search_read([('ci', '=', str(record.cod_barras)),('active', 'in', [True,False])])
                active = False #if persona.active=="false" else True
                print(persona)
                persona=persona[0]
                print(persona)
                print(type(persona))
                if(len(persona['name'])>1):
                    texthtml += "<p class='text-secondary'>ID: " + str(record.cod_barras) + "</p>"
                    texthtml += "<p class='text-success'><i class='fa fa-user fa-2x'></i>"+str(persona['name'])+"</p>"

                    if persona['codigo_persona']==1:
                        texthtml += "<p class='text-secondary'> Estudiante, Año: "+str(persona['estudiante_anno'])+"</p>"
                    if "persona['codigo_persona']==2":
                        texthtml += "<p class='text-secondary'> Trabajador </p>"
                    if "persona['codigo_persona']==3":
                        texthtml += "<p class='text-secondary'> Trabajador(Estudia) </p> "
                    if "persona['codigo_persona'] in [4,6]":
                        texthtml += "<p class='text-secondary'> Profesor </p> "
                    if "persona['codigo_persona']==5":
                        texthtml += "<p class='text-secondary'> Profesor(Estudia) </p> "

                    if persona['estudiante_carrera']:
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-book text-info'></i>persona['estudiante_carrera']</h5>"
                    if persona['active']:
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-check-circle-o text-success'></i> Activo</h5>"
                    else:
                        texthtml += "<h5 class ='channel_name'><i class='fa fa-ban text-danger'></i> Baja </h5>"
                    if persona['becado']:
                         texthtml += "<h5 class ='channel_name'><i class ='fa fa-check-circle-o text-success'></i> Becado </h5>"


                    record.html = texthtml
                    if persona['active']:
                        self.env['gdu.acceso.logs'].create({'ci': record.cod_barras, 'fullname': f"{persona['nombre']} {persona['apellidos']}"})
                    #record.nombre = persona.name
                else:
                    texthtml += "ID:"+str(record.cod_barras)
                    texthtml += "<span class='text-danger'><i class='fa fa-ban'>¡Sin identificación!</span>"
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


