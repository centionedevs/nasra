from odoo import models, fields, api, _


class HrVariableAllowanceDeduction(models.Model):
    _name = 'hr.variable.allowance.deduction'

    employee_id = fields.Many2one('hr.employee')
    contract_id = fields.Many2one('hr.contract', compute='_get_contract_id', store=True)
    date = fields.Date()
    amount = fields.Float(compute='get_amount', store=True)
    add_amount = fields.Float('Add Amount', store=True)
    type = fields.Many2one('hr.variable.allowance.deduction.type')
    payslip_id = fields.Many2one('hr.payslip')

    @api.depends('employee_id')
    def _get_contract_id(self):
        running_contracts = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id),
                                                            ('state', '=', 'open')])
        if running_contracts:
            self.contract_id = running_contracts[0].id

    @api.onchange('type', 'add_amount')
    def _set_amount(self):
        per_day = float(self.employee_id.resource_calendar_id.work_days_per_month)
        per_hour = self.employee_id.resource_calendar_id.hours_per_day
        if self.type and self.contract_id:
            if self.type.calculation_method == 'fixed':
                self.amount = self.type.fixed_amount
                self.amount = -1 * self.add_amount
            elif self.type.calculation_method == 'percentage':
                self.amount = self.contract_id.wage * self.add_amount * 0.01
            elif self.type.calculation_method == 'work_day':
                # self.amount = (self.contract_id.wage / self.employee_id.resource_calendar_id.hours_per_day) * self.type.work_day_amount
                self.amount = (self.contract_id.wage / per_day) * self.add_amount
            elif self.type.calculation_method == 'work_hour':
                # self.amount = (self.contract_id.wage / (per_day * per_hour)) * self.type.work_hour_amount
                self.amount = (self.contract_id.wage / (per_day * per_hour)) * self.add_amount
            if self.type.type == 'deduction':
                self.amount *= -1

    @api.depends('add_amount', 'type.percentage_amount', 'contract_id.variable')
    def get_amount(self):
        for r in self:
            if r.type.calculation_method == 'percentage':
                r.amount = ((r.add_amount * r.type.percentage_amount) / 100) * r.contract_id.variable
            else:
                r.amount = 0
