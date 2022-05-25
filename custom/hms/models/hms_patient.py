from odoo import models, fields, api
from  . import  hms_department
import re
from odoo.exceptions import ValidationError
import time
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

class HmsPatient (models.Model):
    _name = "hms.patient"
    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    department_id = fields.Many2one('hms.department', 'Department Name')
    History = fields.Html()
    cr_ratio = fields.Float()
    Blood_type = fields.Selection([('a','A'),('b' , 'B'),('o' ,'O'),('AB','ab')],default='a')
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="compute_age", store=True)
    dep_capacity = fields.Integer(related="department_id.capacity")
    doctors = fields.Many2many('hms.doctors', 'hms_patient_doctors')
    dep_is_opened = fields.Boolean(related="department_id.is_opened")
    email = fields.Char()
    status = fields.Selection([
        ("undetermined", 'undetermined'),
        ("good", "good"),
        ("fair", "fair"),
        ("serious", "serious")
    ], default="undetermined")
    logs = fields.One2many(comodel_name="hms.logs", inverse_name="patient_id")

    def change_status(self):
        if self.status == "undetermined":
            self.status = "good"
        elif self.status == "good":
            self.status = "fair"
        elif self.status == "fair":
            self.status = "serious"
        elif self.status == "serious":
            self.status = "undetermined"
        self.logs.create({
            "patient_id": self.id,
            "description": self.first_name + " status has changed to " + self.status,
        })


    @api.depends("birth_date")
    def compute_age(self):
        for rec in self:
            if rec.birth_date:
                dob = fields.Date.from_string(rec.birth_date)
                today = date.today()
                relative_data = relativedelta(today, dob)
                rec.age = int(relative_data.years)

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30 and self.age != 0:
            self.pcr = True
            return {
                'warning': {
                    'message': 'PCR has been checked'
                }
            }
    @api.constrains("email")
    def check_email(self):
        for rec in self:
            if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", str(rec.email)):
                    raise ValidationError("Invalid Email!")


    _sql_constraints = [
            ("email_unique", 'unique(email)', "the email you inserted already exists")
    ]
