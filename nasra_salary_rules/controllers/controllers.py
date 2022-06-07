# -*- coding: utf-8 -*-
# from odoo import http


# class NasraSalaryRules(http.Controller):
#     @http.route('/nasra_salary_rules/nasra_salary_rules', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nasra_salary_rules/nasra_salary_rules/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nasra_salary_rules.listing', {
#             'root': '/nasra_salary_rules/nasra_salary_rules',
#             'objects': http.request.env['nasra_salary_rules.nasra_salary_rules'].search([]),
#         })

#     @http.route('/nasra_salary_rules/nasra_salary_rules/objects/<model("nasra_salary_rules.nasra_salary_rules"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nasra_salary_rules.object', {
#             'object': obj
#         })
