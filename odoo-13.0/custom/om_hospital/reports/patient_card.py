from odoo import models, api

class PatientCardReport(models.AbstractModel):
    _name='report.om_hospital.report_patient'
    _description = 'Custom Patient Card Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['hospital.management']
        docs = report_obj.browse(docids[0])
        print('docs =', docs)
        appointments = self.env['hospital.appoinment'].search([('patient_id', '=', docids[0])])
        appointment_list = []
        for val in appointments:
            dict = {
                'name': val.name,
                'patient_name' : val.patient_id.patient_name,
                'age' : val.age,
                'notes' : val.notes,
                'date' : val.date,
            }
            appointment_list.append(dict)

        print('appointment_list', appointment_list)
        return {
            'doc_ids': docids,
            'doc_model': 'hospital.management',
            'docs' : docs,
            'appointment_list' : appointment_list,
        }
