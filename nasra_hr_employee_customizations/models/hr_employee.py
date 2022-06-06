# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    bank_name = fields.Char('Bank Name')
    branch_number = fields.Char('branch number')
    customer_number = fields.Char('Coustmer Number')
    account_number = fields.Char('Account Number')
    payment_method = fields.Char('Payment Method')
    travel_to = fields.Char('Travel To')
    embassy_name = fields.Char('Embassy Name')
    social_insure_no = fields.Char('Social Insurance No')
    social_insure_office = fields.Char('Social Insurance Office')
    
    social_insure_start = fields.Date('Insurance Start Date')
    social_insure_end = fields.Date('Insurance End Date')
    social_insure_vac_date = fields.Date('Social Insurance Date For Vacation Balance')
    religion = fields.Selection([('muslim','Muslim'),('christian','Christian')],string='Religion')
    private_address = fields.Char('Private adddress')
    private_new_email = fields.Char('Private email')
    private_mobile = fields.Char('Private Mobile Phone')
    hiring_date = fields.Date('Hiring Date')
    graduation_year = fields.Char('Graduation Year')
    study_school = fields.Char("University", groups="hr.group_hr_user", tracking=True)

