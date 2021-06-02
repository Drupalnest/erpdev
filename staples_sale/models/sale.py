# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fob_id = fields.Many2one('fob', string="FOB")
    shipvia_id = fields.Many2one('ship.via', string="Ship via")
    service_code = fields.Char(related="shipvia_id.service_code", string="Ship via code", store=True)
    sc_1 = fields.Char(compute='_compute_service_code_digits', store=True)
    sc_2 = fields.Char(compute='_compute_service_code_digits', store=True)
    sc_3 = fields.Char(compute='_compute_service_code_digits', store=True)
    # discount_id = fields.Many2one('sale.discount', string="Discount")
    date_delivered = fields.Date('Date Shipped')
    # amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_amount_discount')
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('parent_id', '=', partner_id)]",)
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="['&', '|', ('company_id', '=', False), ('company_id', '=', company_id), ('parent_id', '=', partner_id)]",)
    port_no = fields.Char('Port No.')


    # Ship From
    sf_name = fields.Char(related="company_id.name", store=True)
    sf_street = fields.Char(related="company_id.street", store=True)
    sf_street2 = fields.Char(related="company_id.street2", store=True)
    sf_city = fields.Char(related="company_id.city", store=True)
    sf_zip = fields.Char(related="company_id.zip", store=True)
    sf_state_code = fields.Char(related="company_id.state_id.code", store=True)
    sf_state_name = fields.Char(related="company_id.state_id.name", store=True)
    sf_country_code = fields.Char(related="company_id.country_id.code", store=True)
    sf_country_name = fields.Char(related="company_id.country_id.name", store=True)
    sf_phone = fields.Char(related="company_id.phone", store=True)
    sf_mobile = fields.Char(related="company_id.partner_id.mobile", store=True)
    sf_fax = fields.Char(related="company_id.fax", store=True)
    sf_email = fields.Char(related="company_id.email", store=True)
    sf_title = fields.Char(related="company_id.partner_id.title.shortcut", store=True)
    sf_ref = fields.Char(related="company_id.partner_id.ref", store=True)
    sf_upsaccountnum = fields.Char(related="company_id.upsaccountnum", store=True)
    sf_fedexaccountnum = fields.Char(related="company_id.fedexaccountnum", store=True)

    # Ship To
    st_name = fields.Char(related="partner_shipping_id.name", store=True)
    st_street = fields.Char(related="partner_shipping_id.street", store=True)
    st_street2 = fields.Char(related="partner_shipping_id.street2", store=True)
    st_city = fields.Char(related="partner_shipping_id.city", store=True)
    st_zip = fields.Char(related="partner_shipping_id.zip", store=True)
    st_state_code = fields.Char(related="partner_shipping_id.state_id.code", store=True)
    st_state_name = fields.Char(related="partner_shipping_id.state_id.name", store=True)
    st_country_code = fields.Char(related="partner_shipping_id.country_id.code", store=True)
    st_country_name = fields.Char(related="partner_shipping_id.country_id.name", store=True)
    st_phone = fields.Char(related="partner_shipping_id.phone", store=True)
    st_mobile = fields.Char(related="partner_shipping_id.mobile", store=True)
    st_fax = fields.Char(related="partner_shipping_id.fax", store=True)
    st_email = fields.Char(related="partner_shipping_id.email", store=True)
    st_title = fields.Char(related="partner_shipping_id.title.shortcut", store=True)
    st_ref = fields.Char(related="partner_shipping_id.ref", store=True)
    st_freight_account = fields.Char(related="partner_shipping_id.freight_account", store=True)
    fedex_account_no = fields.Char(string='FedEx Account No.', compute='_compute_fedex_account_no', store=True)
    ups_account_no = fields.Char(string='UPS Account No.', compute='_compute_fedex_account_no', store=True)

    @api.depends('sc_2')
    def _compute_fedex_account_no(self):
        for rec in self:
            if rec.sc_2 == '1':
                rec.fedex_account_no = rec.sf_fedexaccountnum
                rec.ups_account_no = rec.sf_upsaccountnum
            elif rec.sc_2 == '2':
                rec.fedex_account_no = rec.st_freight_account
                rec.ups_account_no = rec.st_freight_account
            else:
                rec.fedex_account_no = False
                rec.ups_account_no = False

    # @api.depends('order_line.amount_discount')
    # def _amount_discount(self):
    #     for o in self:
    #         o.amount_discount = sum(o.order_line.mapped('amount_discount'))

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'fob_id': self.fob_id,
            'shipvia_id': self.shipvia_id,
            'port_no': self.port_no,
            # 'discount_id': self.discount_id,
        })
        return invoice_vals

    @api.onchange('partner_shipping_id')
    def _onchange_partner_id(self):
        self.fob_id = self.partner_shipping_id and self.partner_shipping_id.fob_id or False
        self.shipvia_id = self.partner_shipping_id and self.partner_shipping_id.shipvia_id or False

    @api.depends('service_code')
    def _compute_service_code_digits(self):
        for rec in self:
            if rec.service_code and len(rec.service_code) == 3:
                rec.sc_1 = rec.service_code[0]
                rec.sc_2 = rec.service_code[1]
                rec.sc_3 = rec.service_code[2]
            else:
                rec.sc_1 = False
                rec.sc_2 = False
                rec.sc_3 = False

    # @api.model
    # def create(self, values):
    #     if values.get('name', _('New')) == _('New'):
    #         seq_date = None
    #         if 'date_order' in values:
    #             seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(values['date_order']))
    #         if 'company_id' in values:
    #             company = self.env['res.company'].browse(values['company_id'])
    #             values['name'] = 'CO' + '-' + company.prefix + self.env['ir.sequence'].with_context(force_company=values['company_id']).next_by_code(
    #                 'sale.order', sequence_date=seq_date) or _('New')
    #         else:
    #             values['name'] = 'CO' + '-' + self.env.user.company_id.prefix + self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')
    #     return super(SaleOrder, self).create(values)

    # def action_confirm(self):
    #     res = super(SaleOrder, self).action_confirm()
    #     for rec in self:
    #         for l in rec.order_line:
    #             if not l.qty_delivered:
    #                 l.qty_delivered = l.product_uom_qty
    #     return res


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_id')
    def _check_product_id(self):
        product_id = self.env['ir.config_parameter'].sudo().get_param('staples_delivery.delivery_charge_default_product_id')
        for l in self:
            if len(l.order_id.order_line.filtered(lambda x: x.product_id.id != int(product_id) and x.product_id.id == l.product_id.id)) > 1:
                raise ValidationError(_('An order cannot have twice the same product.'))
