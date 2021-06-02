# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_commission_free = fields.Boolean('Commission Free')


class Partner(models.Model):
    _inherit = 'res.partner'

    agent = fields.Boolean("Agent?")
    commission = fields.Float()
    agent_id = fields.Many2one("res.partner", string="Salesman", domain="[('agent', '=', True)]")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one(related="partner_id.agent_id", string="Salesman", store=True)
    amount_commission = fields.Monetary(string='Commission', store=True, readonly=True, compute="_amount_all")

    @api.depends('partner_id')
    def _amount_all(self):
        res = super(SaleOrder, self)._amount_all()
        for order in self:
            amount_commission = 0.0
            if order.partner_id.agent_id and order.partner_id.agent_id.commission:
                amount_commission = sum(order.order_line.filtered(lambda l: not l.product_id.is_commission_free).mapped(
                    'price_subtotal')) * (order.partner_id.agent_id.commission / 100.0)
            order.update({
                'amount_commission': amount_commission,
            })
        return res


class Move(models.Model):
    _inherit = 'account.move'

    agent_id = fields.Many2one(related="partner_id.agent_id", string="Salesman", store=True)
    amount_commission = fields.Monetary(string='Commission', store=True, readonly=True, compute="_compute_amount")
    # settlement_id = fields.Many2one('sale.commission.settlement',
    #                                 help="Settlement that generates this invoice",
    #                                 copy=False,
    #                                 )
    settled = fields.Boolean()

    @api.depends('partner_id')
    def _compute_amount(self):
        res = super(Move, self)._compute_amount()
        for move in self:
            if move.partner_id.agent_id and move.partner_id.agent_id.commission:
                move.amount_commission = sum(
                    move.invoice_line_ids.filtered(lambda l: not l.product_id.is_commission_free).mapped(
                        'price_subtotal')) * (move.partner_id.agent_id.commission / 100.0)
                # move.amount_total += move.amount_commission
            else:
                move.amount_commission = 0.0
        return res
