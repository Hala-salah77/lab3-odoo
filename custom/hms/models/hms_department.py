from odoo import models, fields
from  . import  hms_patient
class HmsDepartment(models.Model):
    _name = 'hms.department'
    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients_id = fields.One2many(comodel_name='hms.patient', inverse_name='department_id')
