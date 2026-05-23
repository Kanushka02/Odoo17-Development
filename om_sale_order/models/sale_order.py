from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    location_id = fields.Char(string="Location", required=True)

    approval_status = fields.Selection([
        ('pending', 'Pending Approval'),
        ('waiting', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Approval Status", default='pending', copy=False, tracking=True)

    def action_send_for_approval(self):
        for order in self:
            order.approval_status = 'waiting'
            approver_group = self.env.ref('om_sale_order.group_sale_order_approver', raise_if_not_found=False)

            if approver_group:
                for user in approver_group.users:
                    order.activity_schedule(
                        act_type_xmlid='mail.mail_activity_data_todo',
                        user_id=user.id,
                        summary='Approval Required',
                        note=f'Please review and accept Sales Order {order.name} for location {order.location_id}.'
                    )

    def action_approve(self):
        for order in self:
            order.approval_status = 'approved'
            activities = self.env['mail.activity'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', order.id),
                ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
            ])
            activities.action_done()
            if order.user_id:
                order.activity_schedule(
                    act_type_xmlid='mail.mail_activity_data_todo',
                    user_id=order.user_id.id,
                    summary='Order Approved!',
                    note=f'Your sales order {order.name} has been approved.'
                )

    def action_reject(self):
        for order in self:
            order.approval_status = 'rejected'
            activities = self.env['mail.activity'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', order.id),
                ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
            ])
            activities.action_done()
            if order.user_id:
                order.activity_schedule(
                    act_type_xmlid='mail.mail_activity_data_todo',
                    user_id=order.user_id.id,
                    summary='Order Rejected',
                    note=f'Please review. Sales order {order.name} was rejected.'
                )