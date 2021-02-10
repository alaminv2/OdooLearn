from odoo import models, fields, api, _
import datetime

class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.management', string="Patient", ondelete='cascade')
    date_of_appoint = fields.Datetime(string='Date of Appointment', default=datetime.datetime.now())

    def create_appointment(self):
        vals = {
            'patient_id' : self.patient_id.id,
            'date' : self.date_of_appoint,
        }
        self.patient_id.message_post(body="Appointment created successfully...")
        new_appointment = self.env['hospital.appoinment'].create(vals)
        cntxt = dict(self.env.context)
        cntxt['form_view_initial_mode'] = 'edit'
        return {
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'hospital.appoinment',
            'res_id' : new_appointment.id,
            'context' : cntxt,
        }

    def get_data(self):
        appointments = self.env['hospital.appoinment'].search([('patient_id', '=', self.patient_id.id)])
        for rec in appointments:
            print(rec.name)
        return {
            'type' : 'ir.actions.do_nothing',
        }

    def delete_patient_appointment(self):
        for rec in self:
            print(rec.patient_id)
            rec.patient_id.unlink()
        return {
            'type' : 'ir.actions.do_nothing',
        }


    def print_patient_appointments(self):
        for rec in self:
            if rec.patient_id:
                docs = self.env['hospital.appoinment'].search([('patient_id', '=', rec.patient_id.id)])
                return self.env.ref('om_hospital.report_appointment_card').report_action(docs)
