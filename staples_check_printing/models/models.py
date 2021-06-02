import datetime

from odoo import models, fields, api, _
from odoo.tools.misc import formatLang, format_date


class Payment(models.Model):
    _inherit = 'account.payment'

    def _check_make_stub_line(self, invoice):
        res = super(Payment, self)._check_make_stub_line(invoice)
        payables = invoice.line_ids.filtered(lambda l: l.account_internal_type == 'payable')
        discount_amount = 0.0
        if len(payables) > 1:
            payable = payables and payables[-1]
            if (invoice.invoice_date != payable.date_maturity) and self.payment_date <= payable.date_maturity:
                discount_amount = abs(payable.price_total)
                res['amount_paid'] = formatLang(self.env, invoice.amount_total - discount_amount, currency_obj=self.currency_id)

        res.update({'invoice_date': invoice.invoice_date, 'discount_amount': formatLang(self.env, discount_amount, currency_obj=self.currency_id)})
        return res
