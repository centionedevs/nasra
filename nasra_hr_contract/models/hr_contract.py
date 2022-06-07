from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HrContract(models.Model):
    _inherit = 'hr.contract'

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

    def _compute_employee_resource_id(self):
            self.resource_calendar_id = self.employee_id.resource_calendar_id