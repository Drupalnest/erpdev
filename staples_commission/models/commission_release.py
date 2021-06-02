# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tests.common import Form


class CommissionRelease(models.Model):
    _name = "commission.release"
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, states={'new': [('readonly', False)]},
                       index=True, default=lambda self: _('New'))
    date_from = fields.Date(string="Date From", required=True, readonly=True, states={'new': [('readonly', False)]})
    date_to = fields.Date(string="Date to", required=True, readonly=True, states={'new': [('readonly', False)]})
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company, readonly=True,
                                 states={'new': [('readonly', False)]})
    currency_id = fields.Many2one("res.currency", related='company_id.currency_id')
    state = fields.Selection([('new', 'New'),
                              ('confirmed', 'Confirmed'),
                              ('invoice', 'Invoiced'),
                              ('cancel', 'Cancelled')], default="new")
    line_ids = fields.One2many("commission.release.line", "release_id", string="Settlements")

    def button_confirm(self):
        """ Confirm the commission and update the invoice between from and to with paid status """
        if self.search(['|', '&', ('date_from', '<=', self.date_from), ('date_to', '>=', self.date_from), '&',
                        ('date_from', '<=', self.date_to), ('date_to', '>=', self.date_to)]) - self:
            raise ValidationError(_('You cannot run the commission release, check your periods.'))

        ## to avoid issues of imported payments on jan 21, 2021
        payments = self.env['account.payment'].search(
            [('payment_date', '>=', self.date_from), ('payment_date', '<=', self.date_to)])
        reconciled_moves = payments.mapped('move_line_ids.matched_debit_ids.debit_move_id.move_id') \
                           + payments.mapped('move_line_ids.matched_credit_ids.credit_move_id.move_id')
        reconciled_invoice_ids = reconciled_moves.filtered(lambda move: move.is_invoice())
        commissioned_invoices = reconciled_invoice_ids.filtered(lambda move: move.partner_id.agent_id.commission)

        agents = {}
        for inv in commissioned_invoices:
            agents.setdefault(inv.partner_id.agent_id.id, [])
            agents[inv.partner_id.agent_id.id].append(inv.id)

        vals = []
        for k, v in agents.items():
            vals.append((0, 0, {
                'agent_id': k,
                'commission_invoice_ids': [(6, 0, v)],
            }))
        self.line_ids = False
        self.line_ids = vals
        self.write({"state": "confirmed"})

    ## original function
    # vals = []
        # for agent in self.env["res.partner"].search([("agent", "=", True)]):
        #     query = """
        #         select	move.id
        #         from	account_move move
        #         join	account_move_line line on line.move_id = move.id
        #         join	account_partial_reconcile part ON part.debit_move_id = line.id
        #         join	res_partner p on p.id = move.partner_id
        #         join	res_partner agent on agent.id = p.agent_id
        #         where	move.company_id = %s
        #             and move.type = 'out_invoice'
        #             and move.amount_commission > 0
        #             and move.invoice_payment_state='paid'
        #             and line.account_internal_type='receivable'
        #             and part.create_date::date >= %s
        #             and part.create_date::date <= %s
        #             and agent.id = %s
        #         group by	move.id
        #     """
        #     params = (self.company_id.id, str(self.date_from), str(self.date_to), agent.id)
        #     self._cr.execute(query, params)
        #     query_res = self._cr.fetchall()
        #     if query_res:
        #         vals.append((0, 0, {
        #             'agent_id': agent.id,
        #             'commission_invoice_ids': [(6, 0, [mv[0] for mv in query_res])],
        #         }))
        # self.line_ids = False
        # self.line_ids = vals
        # self.write({"state": "confirmed"})

    def action_invoice(self):
        """ Create invoice from commssion """
        action = self.env.ref('staples_commission.action_commission_make_invoices')
        return action.read()[0]

    def cancel(self):
        """ Cancel the record """
        if self.state in ("confirmed,new"):
            return self.write({"state": "cancel"})
        else:
            raise ValidationError(_('You cannot cancel the comission'))

    def set_to_draft(self):
        """ draft the record """
        if self.state == "cancel":
            return self.write({"state": "new", 'line_ids': False})
        else:
            raise ValidationError(_('Only Cancelled records will be set to draft'))

    def print_record(self):
        """ print the record """
        if not self.state == "confirmed":
            raise ValidationError(
                _('You are not allowed to print the record in this stage /n Only Confirmed records able to print'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('commission.release') or _('New')
        return super(CommissionRelease, self).create(vals)

    def unlink(self):
        for statement in self:
            if statement.state == 'invoice':
                raise UserError(
                    _('Can''t delete invoiced commission release.'))
        return super(CommissionRelease, self).unlink()

    def make_invoices(self, journal, product):
        invoices = self.line_ids._prepare_invoice(journal, product)
        invoices.action_post()
        self.write({"state": "invoice"})
        return invoices


class CommissionReleaseLines(models.Model):
    _name = "commission.release.line"

    release_id = fields.Many2one("commission.release")
    agent_id = fields.Many2one("res.partner", domain="[('agent', '=', True)]", required=True)
    commission_invoice_ids = fields.One2many("account.move", "commission_release_line_id")
    bill_id = fields.Many2one("account.move")
    overall_commission_amount = fields.Float(string="Total", compute="_compute_commission_from_lines", store=True)

    @api.depends('commission_invoice_ids')
    def _compute_commission_from_lines(self):
        """ Calculate the commission total from lines """
        for rec in self:
            rec.overall_commission_amount = sum(rec.commission_invoice_ids.mapped('amount_commission'))

    def print_line(self):
        return self.env.ref('staples_commission.action_report_commission').report_action(self)

    def _prepare_invoice(self, journal, product):
        invoices = self.env['account.move']
        for settlement in self:
            total = sum(settlement.commission_invoice_ids.mapped('amount_commission'))
            move_type = "in_invoice" if total >= 0 else "in_refund"
            move_form = Form(self.env["account.move"].with_context(default_type=move_type))
            move_form.invoice_date = fields.Date.today()
            move_form.partner_id = settlement.agent_id
            move_form.journal_id = journal
            with move_form.invoice_line_ids.new() as line_form:
                line_form.product_id = product
                line_form.quantity = 1
                line_form.price_unit = abs(total)
                # Put period string
                partner = settlement.agent_id
                lang = self.env["res.lang"].search(
                    [("code", "=", partner.lang or self.env.context.get("lang", "en_US"))]
                )
                date_from = fields.Date.from_string(settlement.release_id.date_from)
                date_to = fields.Date.from_string(settlement.release_id.date_to)
                line_form.name += "\n" + _("Period: from %s to %s") % (
                    date_from.strftime(lang.date_format),
                    date_to.strftime(lang.date_format),
                )
            vals = move_form._values_to_save(all_fields=True)
            invoice = invoices.create(vals)
            self.bill_id = invoice.id
            invoices += invoice
        return invoices


class AccountMove(models.Model):
    _inherit = "account.move"

    commission_release_line_id = fields.Many2one("commission.release.line")
    commission = fields.Float(related="partner_id.agent_id.commission", string="Commission %", store=True)
