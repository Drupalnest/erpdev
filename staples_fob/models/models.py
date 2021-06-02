from odoo import api, fields, models


class FOB(models.Model):
    _name = 'fob'

    name = fields.Char(required=True, string='Code')
    description = fields.Char()
    comment = fields.Text('Comments')
