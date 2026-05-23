# from email.policy import default

from odoo import api , fields ,models
# from odoo.odoo.api import ondelete


class HospitalAppoinment(models.Model):
    _name = "hospital.appoinment"
    _inherit = ['mail.thread']
    _description = "Hospital Appoinment"
    _rec_name = "patient_id"

    reference = fields.Char(string="Reference" , default="New")
    # patient_id = fields.Many2one('hospital.patient', string="Patient", required=False, ondelete='cascade')
    # patient_id = fields.Many2one('hospital.patient' , string="Patient" , required=False ,ondelete='restrict')
    patient_id = fields.Many2one('hospital.patient' , string="Patient" , required=False ,ondelete='set null')
    date_appoinment = fields.Date(string="Date")
    note = fields.Text(string="Note")
    state = fields.Selection([('draft' , 'Draft') , ('confirmed' , 'Confirmed') , ('ongoing' , 'Ongoing') , ('done' , 'Done') , ('cancel' , 'Cancel')] , default="draft" ,tracking=True)
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appoinment_line_ids = fields.One2many('hospital.appoinment.line' , 'appoinment_id' , string="Appoinment Lines")

    total_qty = fields.Float(compute="_compute_total_qty" , string="Total Quantity" , store=True)
    date_of_birth = fields.Date(related='patient_id.date_of_birth' , string="DOB" , store=True , groups="om_hospital.group_hospital_doctors")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals.get('reference') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appoinment')
        return super().create(vals_list)

    @api.depends('appoinment_line_ids' , 'appoinment_line_ids.qty')
    def _compute_total_qty(self):
        for rec in self:
            rec.total_qty = sum(rec.appoinment_line_ids.mapped('qty'))

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

class HospitalAppoinmentLine(models.Model):
    _name = "hospital.appoinment.line"
    _description = "Appoinment Line"

    appoinment_id = fields.Many2one('hospital.appoinment', string="Appoinment")
    product_id = fields.Many2one('product.product' , string="Product" , required=True)
    qty = fields.Float(string="Quantity")
