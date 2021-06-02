# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class Picking(models.Model):
    _inherit = "stock.picking"

    amount_delivery = fields.Float("Delivery Amount", copy=False)

    def action_done(self):
        res = super(Picking, self).action_done()
        for pick in self:
            if pick.amount_delivery:
                pick.sale_id._create_delivery_line(pick.amount_delivery, pick.name)
        return res


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # delivery_set = fields.Boolean(compute='_compute_delivery_state')
    amount_delivery = fields.Monetary(string='Delivery Cost', compute='_compute_amount_delivery')

    @api.depends('order_line')
    def _compute_amount_delivery(self):
        product_id = self.env['ir.config_parameter'].sudo().get_param('staples_delivery.delivery_charge_default_product_id')
        for order in self:
            order.amount_delivery = sum([l.price_total for l in order.order_line if l.product_id.id == int(product_id)])

    # @api.depends('order_line')
    # def _compute_delivery_state(self):
    #     for order in self:
    #         order.delivery_set = any(line.is_delivery for line in order.order_line)
    #
    # def _remove_delivery_line(self):
    #     self.env['sale.order.line'].search([('order_id', 'in', self.ids), ('is_delivery', '=', True)]).unlink()

    # @api.model
    # def set_delivery_line_xmlrpc(self, orders):
    #     for order_name, amount in orders.items():
    #         order = self.env['sale.order'].search([('name', '=', order_name)])
    #         if order:
    #             order._create_delivery_line(amount)
    #     return True
    #
    # def set_delivery_line(self, amount, ref):
    #
    #     # Remove delivery products from the sales order
    #     # self._remove_delivery_line()
    #
    #     for order in self:
    #         order._create_delivery_line(amount, ref)
    #     return True

    # def action_open_delivery_amount_wizard(self):
    #     view_id = self.env.ref('staples_delivery.add_delivery_amount_view_form').id
    #     if self.env.context.get('update'):
    #         name = _('Update shipping cost')
    #     else:
    #         name = _('Add a shipping cost')
    #
    #     return {
    #         'name': name,
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'add.delivery.amount',
    #         'view_id': view_id,
    #         'views': [(view_id, 'form')],
    #         'target': 'new',
    #         'context': {
    #             'default_order_id': self.id,
    #         }
    #     }

    def _create_delivery_line(self, price_unit, ref):
        SaleOrderLine = self.env['sale.order.line']
        product_id = self.env['ir.config_parameter'].sudo().get_param('staples_delivery.delivery_charge_default_product_id')
        if not product_id:
            raise Warning(
                _('No product defined delivery charges, please define through Sales > Configuration > Settings'))
        product = self.env['product.product'].browse(int(product_id))

        # # Apply fiscal position
        # taxes = product.taxes_id.filtered(lambda t: t.company_id.id == self.company_id.id)
        # taxes_ids = taxes.ids
        # if self.partner_id and self.fiscal_position_id:
        #     taxes_ids = self.fiscal_position_id.map_tax(taxes, product, self.partner_id).ids

        # Create the sales order line
        so_description = '%s' % product.name_get()[0][1] + (' %s' % ref)
        values = {
            'order_id': self.id,
            'name': so_description,
            'product_uom_qty': 1,
            'product_uom': product.uom_id.id,
            'product_id': product.id,
            'price_unit': price_unit,
            # 'tax_id': [(6, 0, taxes_ids)],
        }
        if self.order_line:
            values['sequence'] = self.order_line[-1].sequence + 1
        # sol = self.order_line.filtered(lambda l: l.is_delivery)
        # if sol:
        #     sol = sol.sudo().write(values)
        # else:
        sol = SaleOrderLine.sudo().create(values)
        return sol


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     is_delivery = fields.Boolean(string="Is a Delivery", default=False)
#
#     def _is_delivery(self):
#         self.ensure_one()
#         return self.is_delivery

    # def _prepare_invoice_line(self):
    #     # OVERRIDE
    #     res = super(SaleOrderLine, self)._prepare_invoice_line()
    #     res.update({
    #         'is_delivery': self.is_delivery
    #     })
    #     return res


class Move(models.Model):
    _inherit = 'account.move'
    amount_delivery = fields.Monetary(string='Delivery Cost', compute='_compute_amount_delivery')

    @api.depends('invoice_line_ids')
    def _compute_amount_delivery(self):
        product_id = self.env['ir.config_parameter'].sudo().get_param('staples_delivery.delivery_charge_default_product_id')
        for inv in self:
            inv.amount_delivery = sum([l.price_total for l in inv.invoice_line_ids if l.product_id.id == int(product_id)])


# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#
#     is_delivery = fields.Boolean(string="Is a Delivery", default=False)
#
#     def _is_delivery(self):
#         self.ensure_one()
#         return self.is_delivery
