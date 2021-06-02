from odoo import api, fields, models


class ShipVia(models.Model):
    _name = 'ship.via'

    name = fields.Char(required=True, string="Description")
    code = fields.Char(required=True)
    comment = fields.Text('Comments')
