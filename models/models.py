# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging


_logger = logging.getLogger(__name__)

# Lista de acceso
class Acceso(models.Model):
    _name = 'gdu.acceso.lista'
    _description = 'GDU Acceso'
    _rec_name = 'nombre'
    nombre = fields.Char(string="Nombre")
    pellidos = fields.Char(string="Apellidos")
    area = fields.Char(string="Apellidos")
    fecha_acceso = fields.Datetime('Fecha de acceso')
    hora_entrada = fields.Datetime('Hora de entrada')
    # new_field = fields.Char(string="", required=False, )


# Prueba de Escaneo
class Escaneo(models.Model):
    _name = 'gdu.acceso.escaner'
    _description = 'Escaneo del código de barras'
    # _rec_name ='cod_barras'
    cod_barras = fields.Char(string="Código de barras", required=True)


    @api.onchange('cod_barras')
    def onchange_cod_barras(self):
        _logger.info('Entro al onchange')
        for record in self:
            if record.cod_barras:
                _logger.info('Entro al if, cod_barras %s' % record.cod_barras)
                self.env['gdu.acceso.escaner'].create({'cod_barras': record.cod_barras})
                self.limpia_cod_barras()
                self.onchange_cod_barras()

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
