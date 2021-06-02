# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    fob_id = fields.Many2one('fob', string="FOB")
    shipvia_id = fields.Many2one('ship.via', string="Ship via")
    service_code = fields.Char(related="shipvia_id.service_code", string="Ship via code", store=True)
    collect = fields.Selection(related="shipvia_id.collect", store=True)
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('parent_id', '=', partner_id)]",
        help="Delivery address for current invoice.")

    @api.onchange('partner_shipping_id')
    def _onchange_partner_id(self):
        self.fob_id = self.partner_shipping_id and self.partner_shipping_id.fob_id or False
        self.shipvia_id = self.partner_shipping_id and self.partner_shipping_id.shipvia_id or False
