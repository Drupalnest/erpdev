# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportOpenCustomerOrder(models.AbstractModel):
    _name = 'report.staples_oco_report.report_open_customer_order'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            data['form'] = {}
            # raise UserError(_("Form content is missing, this report cannot be printed."))

        domain = []
        target_order = data['form'].get('target_order', 'all')

        if target_order and target_order != 'all':
            domain.append(('state', '=', target_order))

        # domain.append(('date_order', '>=', '2020-12-20 00:00:00'))

        if data['form'].get('date_from'):
            date_from = data['form'].get('date_from') + ' 00:00:00'
            domain.append(('date_order', '>=', date_from))

        if data['form'].get('date_to'):
            date_to = data['form'].get('date_to') + ' 00:00:00'
            domain.append(('date_order', '<=', date_to))

        orders = self.env['sale.order'].search(domain)

        # res = {}
        # for journal in data['form']['journal_ids']:
        #     res[journal] = self.with_context(data['form'].get('used_context', {})).lines(target_move, journal, sort_selection, data)
        return {
            'doc_ids': orders.ids,
            'doc_model': self.env['sale.order'],
            'data': data,
            'docs': orders,
            'time': time,
            'lines': orders.mapped('order_line').filtered(lambda l: not l.display_type and (l.product_uom_qty != l.qty_delivered)),
            # 'company_id': self.env['res.company'].browse(data['form']['company_id'][0]),
        }
