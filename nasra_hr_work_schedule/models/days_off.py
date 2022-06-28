from odoo import models, fields, api


class DaysOff(models.Model):
    _name = 'days.off'

    name = fields.Char('Name')