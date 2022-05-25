# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'hms',
    'description': "handles hms",
    'version' : '1.2',
    'summary': 'system for hospital',
    'sequence': 10,
    'depends':['crm'],
    'data': [
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
        'views/hms_logs_views.xml',
        'views/res_partner_inherit_view.xml'
    ],


    'license': 'LGPL-3',
}
