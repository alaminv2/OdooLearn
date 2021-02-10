from odoo import models


class Patient_s_Appointments(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patient_data):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 14, 'align': 'vleft'})
        sheet = workbook.add_worksheet('report_patient_xlsx')
        sheet.write(0, 0, 'Name', format1)
        sheet.write(0, 1, patient_data.patient_name, format1)
        sheet.write(2, 0, 'Age', format2)
        sheet.write(2, 1, patient_data.patient_age, format2)
