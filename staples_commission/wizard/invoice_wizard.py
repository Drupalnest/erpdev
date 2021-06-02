from odoo import models, fields, api, _


class MakeInvoiceWizard(models.TransientModel):
    _name = 'make.invoice.wizard'

    def _default_journal_id(self):
        return self.env["account.journal"].search([("type", "=", "purchase")])[:1]

    def _default_product_id(self):
        return self.env.ref('staples_commission.product_commission').id

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        required=True,
        domain="[('type', '=', 'purchase')]",
        default=_default_journal_id,
    )
    company_id = fields.Many2one(
        comodel_name="res.company", related="journal_id.company_id", readonly=True
    )
    product_id = fields.Many2one(
        string="Product for invoicing", comodel_name="product.product", required=True, default=_default_product_id,
        domain="[('type', '=', 'service')]"
    )

    def button_create(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        commission_release = self.env[active_model].browse(active_id)
        invoices = commission_release.make_invoices(self.journal_id, self.product_id)
        # go to results
        if len(invoices):
            return {
                "name": _("Created Invoices"),
                "type": "ir.actions.act_window",
                "views": [[False, "list"], [False, "form"]],
                "res_model": "account.move",
                "domain": [["id", "in", invoices.ids]],
            }
