from odoo import models, fields


class HmsDoctors(models.Model):
    _name = "hms.doctors"
    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    patients = fields.Many2many('hms.patient')
