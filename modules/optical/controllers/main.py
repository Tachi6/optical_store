from odoo import http, exceptions, fields
from odoo.http import request
from odoo.tools import date_utils
import json
from ..models.optical_visit import VISITS_STATE

STATES = [state[0] for state in VISITS_STATE]
FIELDS = [
    'patient_id',
    'visit_datetime',
    'optometrist_id',
    'state',
    'notes',
    'od_sphere',
    'od_cylinder',
    'od_axis',
    'od_addition',
    'os_sphere',
    'os_cylinder',
    'os_axis',
    'os_addition',
]

class OpticalAPI(http.Controller):
    # Validate token
    def _check_auth(self):
        db_token = request.env['ir.config_parameter'].sudo().get_param('optical_api.static_token')
        user_token = request.httprequest.headers.get('Access-Token')
        
        if not user_token or user_token != db_token:
            raise exceptions.AccessDenied("Invalid or missing token")

    # Parse to JSON
    def json_response(self, data, status=200):
      return request.make_response(
          json.dumps(data, default=date_utils.json_default),
          headers=[('Content-Type', 'application/json')],
          status=status,
      )

    # Endpoint 1 — Search Visits
    @http.route('/api/optical/visits/search', type='http', auth='none', methods=['POST'], csrf=False)
    def search_visits(self, **kwargs):
        # Check valid token
        try:
            self._check_auth()
        except exceptions.AccessDenied:
            return self.json_response({'error': "Invalid or missing token"}, status=401)
        
        # Read raw data
        raw_data = request.httprequest.data
        data = json.loads(raw_data) if raw_data else {}

        # Filter data
        domain = []

        raw_state = kwargs.get('state')
        if raw_state:
            if raw_state in STATES:
                domain.append(('state', '=', raw_state))
        
        raw_optometrist_id = kwargs.get('optometrist_id')
        if raw_optometrist_id:
            try:
                optometrist_id = int(raw_optometrist_id)
                if optometrist_id > 0:
                    domain.append(('optometrist_id', '=', optometrist_id))
            except:
                pass

        patient_id = kwargs.get('patient_id')
        if patient_id:
            try:
                patient_id = int(patient_id)
                if patient_id > 0:
                    domain.append(('patient_id', '=', patient_id))
            except:
                pass

        limit = 10
        try:
            limit = max(1, int(kwargs.get('limit', 0)))
        except:
            pass

        # View fields on JSON response
        raw_fields = data.get('fields')
        fields = FIELDS
        if isinstance(raw_fields, list):
            fields = [field for field in raw_fields if field in FIELDS]
            if len(fields) == 0:
                fields = FIELDS
        
        # Obtain DB response
        visits = request.env['optical.visit'].sudo().search_read(
            domain=domain,
            fields=['id', 'display_name', *fields],
            limit=limit
        )

        # Manage JSON response
        patient = visits[0].pop('patient_id', False)
        if patient:
            visits[0].update({
                "patient": {
                    "id": patient[0],
                    "display_name": patient[1],
                },
            })

        optometrist = visits[0].pop('optometrist_id', False)
        if optometrist:
            visits[0].update({
                "optometrist": {
                    "id": optometrist[0],
                    "display_name": optometrist[1],
                },
            })

        return self.json_response(visits)

    # Endpoint 2 — Create Visit
    @http.route('/api/optical/visits/create', type='http', auth='none', methods=['POST'], csrf=False)
    def create_visit(self, **kwargs):
        # Check valid token
        try:
            self._check_auth()
        except exceptions.AccessDenied:
            return self.json_response({'error': "Invalid or missing token"}, status=401)
        
        # Read raw data
        try:
            raw_data = request.httprequest.data
            data = json.loads(raw_data) if raw_data else {}
        except Exception:
            return self.json_response({'error': 'Invalid JSON format'}, status=400)
        
        # Validate raw data
        required_fields = ['patient_id', 'optometrist_id']
        for field_key in required_fields:
            if field_key not in data:
                return self.json_response({'error': f'Missing field {field_key}'}, status=400)
            
            used_field = request.env['res.partner'] if field_key == 'patient_id' else request.env['res.users']
            
            exists_field_id = used_field.sudo().browse(data.get(field_key)).exists()

            if not exists_field_id:
                return self.json_response({'error': f'{field_key} not in DB'}, status=400)

        # Registry in odoo
        new_optical_visit = request.env['optical.visit'].sudo().create({
            'patient_id': data.get('patient_id'),
            'visit_datetime': fields.Datetime.now(),
            'optometrist_id': data.get('optometrist_id'),
            'state': data.get('state', 'draft'),
            'notes': data.get('notes', ''),
            'od_sphere': data.get('od_sphere', 0),
            'od_cylinder': data.get('od_cylinder', 0),
            'od_axis': data.get('od_axis', 0),
            'od_addition': data.get('od_addition', 0),
            'os_sphere': data.get('os_sphere', 0),
            'os_cylinder': data.get('os_cylinder', 0),
            'os_axis': data.get('os_axis', 0),
            'os_addition': data.get('os_addition', 0),
        })

        return_data = {
            'status': 'success',
            'message': 'Optical visit created',
            'id': new_optical_visit.id,
            'reference': new_optical_visit.name,
        }

        return self.json_response(return_data, status=201)
