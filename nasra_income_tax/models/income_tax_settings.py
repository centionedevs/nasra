# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging

LOGGER = logging.getLogger(__name__)


class IncomeTaxSettings(models.Model):
    _name = 'income.tax.settings'

    name = fields.Char(string="Name", required=False, )
    line_ids = fields.One2many(comodel_name="income.tax.settings.line", inverse_name="income_tax_id",
                               string="Taxes Divisions", required=False, ondelete='cascade')
    is_functional_exempt = fields.Boolean(string="Function Exemption")
    functional_exempt_value = fields.Float(string="Functional Exemption Value", required=False, digits=(12, 6))
    class_ids = fields.One2many('income.tax.class', inverse_name='income_tax_id', string='Taxes Classes',
                                ondelete='cascade')

    # @api.constrains('line_ids')
    # def check_line_ids(self):
    #     if self.line_ids:
    #         prev = self.line_ids[0].max_value
    #         for line in self.line_ids[1:]:
    #             # if abs(prev - line.min_value) > 0.0001:
    #             #     raise ValidationError('Tax Division Is Missing')
    #             prev = line.max_value

    def rule_val_inpayslips_since_date(self, employee, current_payslip_id, rule_code, start_date, end_date):
        last_payslip_lines = self.env['hr.payslip.line'].search([
            ('slip_id', '!=', current_payslip_id),
            ('slip_id.employee_id', '=', employee.id),
            ('code', '=', rule_code),
            ('slip_id.date_from', '>=', start_date),
            ('slip_id.date_to', '<', end_date),
        ])

        if last_payslip_lines:
            return sum(last_payslip_lines.mapped('total'))
        else:
            return 0

    def category_val_inpayslips_since_date(self, employee, current_payslip_id, category_code, start_date, end_date):
        last_payslip_lines = self.env['hr.payslip.line'].search([
            ('slip_id', '!=', current_payslip_id),
            ('slip_id.employee_id', '=', employee.id),
            ('category_id.code', '=', category_code),
            ('slip_id.date_from', '>=', start_date),
            ('slip_id.date_to', '<', end_date),
        ])

        if last_payslip_lines:
            return sum(last_payslip_lines.mapped('total'))
        else:
            return 0

    def calc_income_tax(self, tax_pool, payslip):
        first_day_in_current_year = datetime.now().date().replace(month=1, day=1)
        payslip = payslip.dict

        # current one in payslip, and last months during current year + previous tax pool from contract
        tax_pool += self.category_val_inpayslips_since_date(payslip.employee_id, payslip.id, 'BASIC',
                                                            first_day_in_current_year, payslip.date_from) + \
                    self.category_val_inpayslips_since_date(payslip.employee_id, payslip.id, 'ALW',
                                                            first_day_in_current_year, payslip.date_from)

        # current one in payslip, and last months during current year
        total_social_insurance = self.rule_val_inpayslips_since_date(payslip.employee_id,
                                                                                           payslip.id,
                                                                                           'SIC',
                                                                                           first_day_in_current_year,
                                                                                           payslip.date_from)

        # last months value of income tax during current year
        total_income_tax = self.rule_val_inpayslips_since_date(payslip.employee_id, payslip.id,
                                                               'INCTAX', first_day_in_current_year,
                                                               payslip.date_from)

        # subtrct social insurance from taxpool
        tax_pool = tax_pool - abs(total_social_insurance)
        month_count = 0
        # if payslip.date_to.year == payslip.contract_id.date_start.year:
        month_count = payslip.date_to.month - payslip.contract_id.date_start.month + 1
        # else:
        #     month_count = payslip.date_to.month
        tax_pool /= month_count

        tax_pool *= 12

        # starting income tax applying segments
        income_tax_settings = self.env.ref('nasra_income_tax.income_tax_settings0')
        functional_exemption = income_tax_settings.is_functional_exempt and income_tax_settings.functional_exempt_value or 0
        effective_salary = 0
        income_tax = 0.0
        income_tax_after_exemption = 0.0
        starting_beginning_segment_sequence = 0

        # cases of taxpool
        if tax_pool < 600000:
            tax_pool /= 12
            effective_salary = tax_pool - functional_exemption
            starting_beginning_segment_sequence = 1

        elif tax_pool < 700000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 2

        elif tax_pool < 800000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 3

        elif tax_pool < 900000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 4
        elif tax_pool < 1000000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 5

        elif tax_pool < 1100000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 6

        elif tax_pool > 1100000:
            tax_pool /= 12
            effective_salary = tax_pool
            starting_beginning_segment_sequence = 7

        for class_seg in income_tax_settings.class_ids:
            if class_seg.value_from <= effective_salary <= class_seg.value_to:
                starting_beginning_segment_sequence = class_seg.rank
                break

        sorted_lines = income_tax_settings.line_ids.search(
            [('sequence', '>=', starting_beginning_segment_sequence)]).sorted(lambda x: x.sequence)

        for line in sorted_lines:
            if line.diff_value:
                if effective_salary <= line.diff_value:
                    income_tax += (line.tax_ratio / 100.0) * effective_salary
                    income_tax_after_exemption = (100 - line.discount_ratio) / 100.0 * income_tax
                    break
                elif effective_salary > line.diff_value:
                    effective_salary -= line.diff_value
                    income_tax += (line.tax_ratio / 100.0) * line.diff_value

            else:
                income_tax += (line.tax_ratio / 100.0) * effective_salary
                break
        result = (income_tax_after_exemption * month_count) - abs(total_income_tax)
        return result

    def calc_next_tax(self, tax_pool, employee, payslip):
        previous_tax = 0
        previous_tax_pool = 0
        salary_slips = self.env['hr.payslip'].search([
            ('state', '=', 'done'),
            ('date_to', '<=', payslip.date_to),
            ('date_from', '>=', payslip.date_from),
            ('employee_id', '=', employee.id)], order='date_to desc')
        salary_slips_filtered = salary_slips.filtered(
            lambda x: 'INCTAX' in x.line_ids.mapped('code') or 'NXTTAX' in x.line_ids.mapped('code'))
        for salary_slip in salary_slips_filtered:
            for line in salary_slip.line_ids:
                if line.code in ['INCTAX', 'NXTTAX']:
                    previous_tax += abs(line.total)
                    break
                elif line.category_id.code in ['BASIC', 'ALW', 'DED']:
                    previous_tax_pool += line.total

        tax_amount = (self.calc_income_tax(tax_pool ,payslip) + previous_tax_pool) - previous_tax
        return tax_amount

    def get_attendance_rate(self, payslip, contract):
        no_of_days = (contract.date_start - payslip.date_from).days
        return no_of_days / (payslip.date_to - payslip.date_from).days

    def check_date(self, payslip, contract):
        if fields.Date.from_string(payslip.date_from).month == fields.Date.from_string(
                contract.date_start).month and fields.Date.from_string(
            payslip.date_from).year == fields.Date.from_string(contract.date_start).year:
            return True
        return False


class IncomeTaxSettingsLine(models.Model):
    _name = 'income.tax.settings.line'
    _order = 'min_value asc'

    income_tax_id = fields.Many2one(comodel_name="income.tax.settings", string="Income Tax Settings", required=False, )
    max_value = fields.Float(string="Maximum Value", required=False, digits=(12, 6))
    diff_value = fields.Float(string="Difference Value", required=False, compute='compute_diff_value', digits=(12, 6))
    tax_ratio = fields.Float(string="Tax Ratio %", required=False, digits=(12, 6))
    discount_ratio = fields.Float(string="Discount Ratio %", required=False, digits=(12, 6))

    sequence = fields.Integer(string="Sequence", required=False)
    min_value = fields.Float(string="Minimum Value", required=False, digits=(12, 6))

    beginning_segment_sequence = fields.Integer(default=1)

    @api.depends('max_value', 'max_value')
    def compute_diff_value(self):
        for rec in self:
            if rec.max_value:
                rec.diff_value = rec.max_value - rec.min_value
            else:
                rec.diff_value = 0

    @api.constrains('max_value', 'max_value', 'discount_ratio', 'tax_ratio')
    def check_all_values(self):
        if self.max_value and self.min_value and self.max_value < self.min_value:
            raise ValidationError('Minimum Value Can not be greater than maximum value')
        if self.tax_ratio < 0 or self.tax_ratio > 100:
            raise ValidationError('Tax Ratio Must Be Between 0 and 100')
        if self.discount_ratio < 0 or self.discount_ratio > 100:
            raise ValidationError('Discount Ratio Must Be Between 0 and 100')


class IncomeTaxClass(models.Model):
    _name = 'income.tax.class'

    income_tax_id = fields.Many2one(comodel_name="income.tax.settings", string="Income Tax Settings", required=False, )
    value_from = fields.Float(string='From')
    value_to = fields.Float(string='To')
    rank = fields.Integer(string='Rank')
