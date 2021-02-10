{
    'name': 'Hospital Management',
    'version': '13.0.1.5.0',
    'category': 'Extra Tools',
    'summary': 'Module for managing hospitals',
    'sequence': '10',
    'License': 'AGPL-3',
    'author': 'Alamin Islam',
    'Maintainer': 'Alamin Islam',
    'website': 'alamin.com',
    'depends': ['base', 'mail', 'sale', 'board'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'wizards/create_appointment.xml',

        'views/appoinment.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/template.xml',
        'views/sale_order_views.xml',
        'views/dashboard.xml',
        'views/setting.xml',
        'views/server_action.xml',
        'views/inherited.xml',

        'reports/patient_card.xml',
        'reports/appointments.xml',
        'reports/report.xml',
        'reports/patient_badge_from_employee.xml',

        'data/email_template.xml',
        'data/sequence.xml',
        'data/data.xml',
        'data/corn_job.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
