# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_discount_free = fields.Boolean('Discount Free')


class Discount(models.Model):
    _name = 'sale.discount'

    name = fields.Char(string='Code')
    discount_percent = fields.Float()
    description = fields.Char()
    comment = fields.Text()


class Partner(models.Model):
    _inherit = 'res.partner'

    discount_id = fields.Many2one('sale.discount', string="Discount")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_id = fields.Many2one('sale.discount', string="Discount Code")
    discount_percent = fields.Float(string='Discount Percent', store=True, related='discount_id.discount_percent')
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount_discount')

    @api.depends('order_line.amount_discount')
    def _compute_amount_discount(self):
        for order in self:
            order.amount_discount = sum(
                order.order_line.filtered(lambda l: not l.product_id.is_discount_free).mapped('amount_discount'))

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.discount_id = self.partner_id and self.partner_id.discount_id or False

    @api.onchange('discount_id')
    def _onchange_discount_id(self):
        disc_percent = self.discount_id.discount_percent or 0.0
        self.order_line.filtered(lambda l: not l.product_id.is_discount_free).discount = disc_percent

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_id': self.discount_id,
        })
        return invoice_vals


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    # discount = fields.Float(string='Discount (%)', digits='Discount', related="order_id.discount_id.discount_percent",
    #                         store=True)
    amount_discount = fields.Monetary(compute="_compute_amount_discount", store=True)

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit
            if not line.product_id.is_discount_free:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

    @api.depends('discount', 'price_unit', 'product_uom_qty')
    def _compute_amount_discount(self):
        for l in self:
            if not l.product_id.is_discount_free:
                l.amount_discount = l.price_unit * l.product_uom_qty * (l.discount / 100.00)


class Move(models.Model):
    _inherit = "account.move"

    discount_id = fields.Many2one('sale.discount', string="Discount Code")
    discount_percent = fields.Float(string='Discount Percent', store=True, related='discount_id.discount_percent')
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount_discount')

    @api.onchange('partner_id')
    def _onchange_partner(self):
        self.discount_id = self.partner_id and self.partner_id.discount_id or False

    @api.onchange('discount_id')
    def _onchange_discount_id(self):
        lines = self.invoice_line_ids.filtered(lambda l: not l.product_id.is_discount_free)
        lines.discount = self.discount_percent
        lines._onchange_price_subtotal()
        self._recompute_dynamic_lines()
        # self.invoice_line_ids.filtered(lambda l: not l.product_id.is_discount_free)._onchange_price_subtotal()

    @api.depends('invoice_line_ids.amount_discount')
    def _compute_amount_discount(self):
        for inv in self:
            inv.amount_discount = sum(
                inv.invoice_line_ids.filtered(lambda l: not l.product_id.is_discount_free).mapped('amount_discount'))


class MoveLine(models.Model):
    _inherit = 'account.move.line'

    # discount = fields.Float(string='Discount (%)', digits='Discount', related="move_id.discount_id.discount_percent",
    #                         store=True)
    amount_discount = fields.Monetary(compute="_compute_amount_discount", store=True)

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes,
                                            move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        price_unit_wo_discount = price_unit
        if not product.is_discount_free:
            price_unit_wo_discount = price_unit * (1 - (discount / 100.0))

        subtotal = quantity * price_unit_wo_discount

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.compute_all(price_unit_wo_discount,
                                                  quantity=quantity, currency=currency, product=product,
                                                  partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        # In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res

    @api.depends('discount', 'price_unit', 'quantity')
    def _compute_amount_discount(self):
        for l in self:
            if not l.product_id.is_discount_free:
                l.amount_discount = l.price_unit * l.quantity * (l.discount / 100.00)
