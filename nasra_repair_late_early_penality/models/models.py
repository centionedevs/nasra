# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LateEarlyTimeInterval(models.Model):
    _inherit = 'late.early.time.interval'

    early_resource_calendar_id = fields.Many2one('resource.calendar')


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    early_leave_penalty_line_ids = fields.One2many('late.early.time.interval', 'early_resource_calendar_id')
