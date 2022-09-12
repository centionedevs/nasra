from lxml import etree

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrContract(models.Model):
    _inherit = 'hr.contract'

    allowances_per_day = fields.Float('Allowances Per Day')
    variable = fields.Float(string="Variable", store=True)

    num_working_days_month = fields.Integer(default=30,
                                            help="Used as standard rate for overtime calculations regardless "
                                                 "the true working days")
    num_working_hours_day = fields.Integer(default=8,
                                           help="Used as standard rate for overtime calculations regardless "
                                                "the true working hours")
    resource_calendar_id = fields.Many2one(
        'resource.calendar', 'Working Schedule', compute='_compute_employee_resource_id', store=True, readonly=False, copy=False, index=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    @api.constrains('state')
    def constrain_state(self):
        employee_contracts = self.env['hr.contract'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
        if len(employee_contracts) > 1:
            error_message = "Multiple running contracts for employee: " + str(self.employee_id.name)
            raise UserError(error_message)

    @api.depends('employee_id.resource_calendar_id')
    def _compute_employee_resource_id(self):
            self.resource_calendar_id = self.employee_id.resource_calendar_id

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     # OVERRIDE to add the 'available_partner_bank_ids' field dynamically inside the view.
    #     # TO BE REMOVED IN MASTER
    #     res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
    #     if view_type == 'form':
    #         users = self.env['res.users'].sudo().search([])
    #         form_view = self.env.ref('hr_contract.hr_contract_view_form')
    #         for user in users:
    #             group = user.sudo().has_group('golden_fish_sale_order_product_report.group_cost_margin_report')
    #     return res
