# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'

    upsaccountnum = fields.Char("UPS Account No.")
    fedexaccountnum = fields.Char("FedEx Account No.")
    ref = fields.Char("Reference")
    prefix = fields.Char("Prefix")


class Partner(models.Model):
    _inherit = 'res.partner'

    freight_account = fields.Char("Freight Account")
    user_id = fields.Many2one('res.users', string='Current User',
                              help='The internal user in charge of this contact.')
    credit_notes = fields.Text()