# -*- coding: utf-8 -*-
# from odoo import http


# class CentioneRepairLateEarlyPenality(http.Controller):
#     @http.route('/centione_repair_late_early_penality/centione_repair_late_early_penality/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/centione_repair_late_early_penality/centione_repair_late_early_penality/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('centione_repair_late_early_penality.listing', {
#             'root': '/centione_repair_late_early_penality/centione_repair_late_early_penality',
#             'objects': http.request.env['centione_repair_late_early_penality.centione_repair_late_early_penality'].search([]),
#         })

#     @http.route('/centione_repair_late_early_penality/centione_repair_late_early_penality/objects/<model("centione_repair_late_early_penality.centione_repair_late_early_penality"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('centione_repair_late_early_penality.object', {
#             'object': obj
#         })
