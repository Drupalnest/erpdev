# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    # change "salesperson" to "current user"
    invoice_user_id = fields.Many2one('res.users', copy=False, tracking=True,
                                      string='Current User',
                                      default=lambda self: self.env.user)
    port_no = fields.Char('Port No.')

    def _get_sale_order(self):
        if self.invoice_origin:
            if self.invoice_origin[:2] != 'PO':
                return self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)

    def _get_date_shipped(self):
        order = self._get_sale_order()
        return order and (order.date_delivered or order.commitment_date) or ''

    def _get_cust_ord_no(self):
        order = self._get_sale_order()
        return order and order.client_order_ref or ''

    @api.model
    def create_xmlrpc(self, data, file_name):
        move_obj = self.env['account.move'].sudo()
        payment_obj = self.env['account.payment'].sudo()
        count = 1
        total = len(data)
        errors = {'IC': {}, 'IP': {}, 'PC': {}, 'PP': {}, }
        for x in data:
            _logger.info("%s of %s - %s, %s" % (count, total, file_name, x))
            count += 1
            move_id = move_obj.search([('name', '=', x)], limit=1)
            # payment = data[x]['payment']
            # data[x].pop('payment')
            # data[x].pop('exist')
            if not move_id:
                try:
                    move_id = move_obj.create(data[x])
                except Exception as e:
                    errors['IC'][x] = {'action': 'IC', 'exception': str(e)}
                    _logger.error("IC: %s, %s" % (x, e))
                finally:
                    try:
                        move_id.action_post()
                    except Exception as e:
                        errors['IP'][x] = {'action': 'IP', 'exception': str(e)}
                        _logger.error("IP: %s, %s" % (x, e))

                if payment_obj.search([('communication', '=', x)]):
                    continue

                # if payment and move_id:
                #     payment.pop('exist')
                #     payment['invoice_ids'] = [(6, 0, [move_id.id])]
                #     try:
                #         payment_id = payment_obj.create(payment)
                #     except Exception as e:
                #         errors['PC'][x] = {'action': 'PC', 'exception': str(e)}
                #         _logger.error("PC: %s, %s" % (x, e))
                #     finally:
                #         try:
                #             payment_id.post()
                #         except Exception as e:
                #             errors['PP'][x] = {'action': 'PP', 'exception': str(e)}
                #             _logger.error("PP: %s, %s" % (x, e))
        if errors['IC'] or errors['IP'] or errors['PC'] or errors['PP']:
            with open('/home/jothimani/Dropbox/CLEAR_VIEW_INFOTECH/Staples/IMPORT_ERRORS/ERRORS_%s.json' % file_name, 'w') as outputfile:
                json.dump(errors, outputfile)
        return True

    def xmlrpc_reset(self):
        self.button_draft()
        return True

    def xmlrpc_post(self):
        self.post()
        return True

    def xmlrpc_button_draft(self):
        self.button_draft()
        return True

    def xmlrpc_draft_and_post(self):
        self.button_draft()
        self.post()
        return True

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_qty_ordered(self):
        if self.sale_line_ids:
            return sum(self.sale_line_ids.mapped('product_uom_qty')) or 0
        # if self.purchase_line_ids:
        #     return sum(self.purchase_line_ids.mapped('product_qty')) or 0
        else:
            return self.quantity or 0

    def _get_qty_delivered(self):
        if self.sale_line_ids:
            return sum(self.sale_line_ids.mapped('qty_delivered')) or 0
        # if self.purchase_line_ids:
        #     return sum(self.purchase_line_ids.mapped('qty_received')) or 0
        else:
            return self.quantity or 0


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.model
    def xmlrpc_create(self, vals):
        count = len(vals)
        i = 1
        for val in vals:
            print("%s of %s" % (i, count))
            self.create(val)
            i += 1

    def xmlrpc_draft(self):
        self.action_draft()
        return True

    def xmlrpc_post(self):
        self.post()
        return True

    def xmlrpc_draft_and_post(self):
        self.action_draft()
        self.post()
        return True

# class AccountReconciliation(models.AbstractModel):
#     _inherit = 'account.reconciliation.widget'
#
#     @api.model
#     def xmlrpc_get_data_for_manual_reconciliation(self, res_type, res_ids=None, account_type=None):
#         data = self.get_data_for_manual_reconciliation(res_type, res_ids, account_type)
#         return data
