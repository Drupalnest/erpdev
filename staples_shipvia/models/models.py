from odoo import api, fields, models


class ShipVia(models.Model):
    _name = 'ship.via'

    name = fields.Char(required=True, string="Code")
    description = fields.Char(required=True)
    service_code = fields.Char()
    collect = fields.Selection([('1', 'Shipper'), ('2', 'Receiver'), ('3', 'Third Party'), ('4', 'Collect')])
    comment = fields.Text('Comments')
