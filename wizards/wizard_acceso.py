# -*- coding: utf-8 -*-

from odoo import api, fields, models
import re
import logging

_logger = logging.getLogger(__name__)
class WizardEscaneo(models.TransientModel):
    _name = "gdu.acceso.wizard"
    _description = "Gdu Control de Acceso Wizard"

    cod_barras_w = fields.Char('Entre el codigo')

    @api.onchange('cod_barras_w')
    def onchange_cod_barras_w(self):
        for record in self:
            barcode = str(record.cod_barras_w)
            if barcode.isdigit():
                self.env['gdu.acceso.escaner'].create({'cod_barras': record.cod_barras_w})
                self.cod_barras_w = str("aaa")
                #self.onchange_cod_barras_w(self)
                #return record.cod_barras_w = ""
            else:
                self.cod_barras_w = ""

    def f_cancel(self):
        persona = self.env['gdu.base.persona'].search([('ci', '=', '83022125063')])
        return {'warning': {'title': ("Warning"), 'message': (
            "The m2o field %s is required but declares its ondelete policy "
            "as being 'set null'. Only 'restrict' and 'cascade' make sense."
            % (persona.nombre)
        )}}
   