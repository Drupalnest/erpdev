from odoo import api, fields, models


class FOB(models.Model):
    _name = 'fob'

    name = fields.Char(required=True, string="Description")
    code = fields.Char(required=True)
    comment = fields.Text('Comments')
