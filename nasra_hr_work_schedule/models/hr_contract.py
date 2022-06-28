from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'


    @api.onchange('resource_calendar_id')
    def onchange_resource_hours(self):
        for rec in self:
            if rec.resource_calendar_id:
                rec.num_working_days_month = rec.resource_calendar_id.work_days_per_month
                rec.num_working_hours_day = rec.resource_calendar_id.hours_per_day