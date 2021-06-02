# -*- coding: utf-8 -*-
# from odoo import http


# class StaplesShipvia(http.Controller):
#     @http.route('/staples_shipvia/staples_shipvia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/staples_shipvia/staples_shipvia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('staples_shipvia.listing', {
#             'root': '/staples_shipvia/staples_shipvia',
#             'objects': http.request.env['staples_shipvia.staples_shipvia'].search([]),
#         })

#     @http.route('/staples_shipvia/staples_shipvia/objects/<model("staples_shipvia.staples_shipvia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('staples_shipvia.object', {
#             'object': obj
#         })
