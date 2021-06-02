from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    fob_id = fields.Many2one('fob', string="FOB")
    shipvia_id = fields.Many2one('ship.via', string="Ship via")
    # discount_id = fields.Many2one('sale.discount', string="Discount")
