from odoo import models, api, fields

class Lab(models.Model):
    _name = 'hospital.lab'
    _description = 'Lab records'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    user_id = fields.Many2one('res.users', string="Responsible")