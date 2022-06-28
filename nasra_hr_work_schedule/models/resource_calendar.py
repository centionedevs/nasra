# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    days_off_ids = fields.Many2many('days.off','day_of_relation',string='Days off')
    work_days_per_month = fields.Char('Work Days Per Month')
    hour_limit = fields.Float('Hour Limit')


