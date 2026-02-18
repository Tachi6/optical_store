from odoo import fields
from odoo.http import request


class CreateNewRegister:
    def __init__(self, data):
        self.data = data
        self.new_optical_visit = self._create_new_register()

    def _create_new_register(self):
        return request.env['optical.visit'].sudo().create({
            'patient_id': self.data.get('patient_id'),
            'visit_datetime': fields.Datetime.now(),
            'optometrist_id': self.data.get('optometrist_id'),
            'state': self.data.get('state', 'draft'),
            'notes': self.data.get('notes', ''),
            'od_sphere': self.data.get('od_sphere', 0),
            'od_cylinder': self.data.get('od_cylinder', 0),
            'od_axis': self.data.get('od_axis', 0),
            'od_addition': self.data.get('od_addition', 0),
            'os_sphere': self.data.get('os_sphere', 0),
            'os_cylinder': self.data.get('os_cylinder', 0),
            'os_axis': self.data.get('os_axis', 0),
            'os_addition': self.data.get('os_addition', 0),
        })
