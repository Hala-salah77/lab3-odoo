from odoo import models, fields, exceptions, api
from odoo.exceptions import UserError


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one("hms.patient", string="Patients")
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise exceptions.UserError(
                    'Cannot delete record because he is related to a patient')
        return super(ResPartnerInherit, self).unlink()

    @api.constrains('related_patient_id')
    def check_email(self):
        for record in self:
            if record.related_patient_id.email != record.email:
                if self.env['hms.patient'].search([('email', '=', record.email)]):
                    raise UserError("E-mail already taken")
