# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import sys, numbers, string
import json

limit = sys.getrecursionlimit()

_logger = logging.getLogger(__name__)

_logger.info('getrecursionlimit %s' % limit)
# Lista de acceso
class Acceso(models.Model):
    _name = 'gdu.acceso.logs'
    _description = 'GDU Acceso Logs'
    _rec_name = 'nombre'
    nombre = fields.Char(string="Nombre")
    pellidos = fields.Char(string="Apellidos")
    area = fields.Char(string="Apellidos")
    fecha_acceso = fields.Datetime('Fecha de acceso')
    hora_entrada = fields.Datetime('Hora de entrada')
    ci = fields.Char(string="CI", size=11)
    # new_field = fields.Char(string="", required=False, )


# Prueba de Escaneo
class Escaneo(models.Model):
    _name = 'gdu.acceso.escaner'
    _description = 'GDU Acceso Scan'
    # _rec_name ='cod_barras'
    cod_barras = fields.Char(string="Código de barras", size=11, store=False)
    nombre = fields.Char(string="Nombre:", readonly=True)
    tipo_persona = fields.Char(string="Tipo de persona:", readonly=True)


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
        _logger.info('Entro al onchange')
        for record in self:
            if str(record.cod_barras).isnumeric() and len(record.cod_barras)==11:
                _logger.info('Entro al if, cod_barras %s' % record.cod_barras)
                _logger.info('Count, cod_barras %s' % len(record.cod_barras))
                persona = self.env['gdu.base.persona'].search([('ci', '=', str(record.cod_barras))])
                record.nombre = persona.name
                record.tipo_persona = persona.tipo_persona
                self.env['gdu.acceso.logs'].create({'ci': record.cod_barras})
                record.cod_barras = ""
            else:
                record.nombre = ""
                record.tipo_persona = ""

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
