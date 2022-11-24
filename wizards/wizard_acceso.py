# -*- coding: utf-8 -*-

from odoo import api, fields, models

class WizardEscaneo(models.TransientModel):
    _name = "gdu.acceso.wizard"
    _description = "Gdu Control de Acceso Wizard"

    cod_barras_w = fields.Char('Entre el codigo')

    @api.onchange('cod_barras_w')
    def onchange_cod_barras_w(self):
        for record in self:
            if record.cod_barras_w:
                self.env['gdu.acceso.escaner'].create({'cod_barras': record.cod_barras_w})
                self.cod_barras_w = ""
                record.cod_barras_w = ""


   