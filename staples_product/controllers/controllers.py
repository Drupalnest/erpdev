# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesProduct(http.Controller):
#     @http.route('/staples_product/staples_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_product/staples_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_product.listing', {
#             'root': '/staples_product/staples_product',
#             'objects': http.request.env['staples_product.staples_product'].search([]),
#         })

#     @http.route('/staples_product/staples_product/objects/<model("staples_product.staples_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_product.object', {
#             'object': obj
#         })
