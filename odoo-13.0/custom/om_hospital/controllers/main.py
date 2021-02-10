from odoo import http
from odoo.http import request

class HospitalPatientController(http.Controller):
    @http.route('/hospital/alamin/msg', website=True, auth='public')
    def hospital_controller(self):
        all_patients = request.env['hospital.management'].sudo().search([])
        # return 'Alamin is desperate for doing sex...'
        return request.render("om_hospital.patient_page_template", {'patients' : all_patients})


    @http.route('/get_patients', type='json', auth='user')
    def get_patients(self):
        all_patients = request.env['hospital.management'].search([])
        patient_list = []
        for patient in all_patients:
            vals = {
                "ID" : patient.id,
                "Sequence" : patient.name_seq,
                'Name' : patient.patient_name,
                'Age' : patient.patient_age,
            }
            patient_list.append(vals)
        data = {'response':patient_list}
        return data

    @http.route('/create_patient', auth='user', type='json')
    def create_patient(self, **rec):
        if request.jsonrequest:
            if rec['name'] and rec['age']:
                vals = {
                    "patient_name" : rec['name'],
                    "patient_age" : rec['age'],
                }
                new_patient = request.env['hospital.management'].sudo().create(vals)
                print('New Parient = ',new_patient)
                response = {"status":200, "message":"New Patient created successfully...", "new_patient_id":new_patient.id}
        return response

    @http.route('/update_patient', auth='user', type='json')
    def update_patient(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                print('update data = ',rec)
                existing_patient = request.env['hospital.management'].sudo().search([('id', '=', rec['id'])])
                print('existing_patient = ', existing_patient)
                if existing_patient:
                    existing_patient.sudo().write(rec)
                    print('existing_patient = ', existing_patient)
                    response = {"status": 200, "message": "New Patient updated successfully..."}
                else:
                    response = {"status": 404, "message": "No Patient Found With The Given 'Patient ID'..."}

        return response
