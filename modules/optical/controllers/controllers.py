# -*- coding: utf-8 -*-
# from odoo import http


# class Optical(http.Controller):
#     @http.route('/optical/optical', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/optical/optical/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('optical.listing', {
#             'root': '/optical/optical',
#             'objects': http.request.env['optical.optical'].search([]),
#         })

#     @http.route('/optical/optical/objects/<model("optical.optical"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('optical.object', {
#             'object': obj
#         })

