from odoo import api , fields ,models, _
from odoo.exceptions import UserError ,ValidationError

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']
    _description = "Patient Master"

    name = fields.Char(string="Name" , required=True , tracking=True)
    date_of_birth = fields.Date(string="DOB" , tracking=True)
    gender = fields.Selection([('male' , 'Male') , ('female' ,'Female')] , string="Gender" , tracking=True)

    tag_ids = fields.Many2many("patient.tag" , "patient_tag_rel" , "patient_id" , "tag_id" , string="Tags")

    # def unlink(self):
    #     # we can perform anything here
    #     for rec in self:
    #         domain = [('patient_id', '=', rec.id)]
    #         appoinments = self.env['hospital.appoinment'].search(domain)
    #         if appoinments:
    #             # raise ValidationError("You cannot delete a patient with appointments.")
    #             raise UserError("You cannot delete a patient with appointments.")
    #     return super().unlink()

    @api.ondelete(at_uninstall=False)
    def _check_patient_appointments(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appoinment'].search(domain)
            if appointments:
                raise ValidationError(_("You cannot delete the patient now.\nAppointments existing for this patient"))