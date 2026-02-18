from odoo import http, exceptions, fields
from odoo.http import request
from odoo.tools import date_utils
import json
from ..constants import BASIC_FIELDS, DIOPTRE_FIELDS
from ..utils.recorset_for_db import RecorsetForDB
from ..utils.api_validations import CreateNewRegister

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

        # Create recordset for read DB
        recorset_for_db = RecorsetForDB(kwargs, data)
        
        # Obtain DB response
        visits = request.env['optical.visit'].sudo().search_read(
            domain=recorset_for_db.domain,
            fields=['id', 'display_name', *BASIC_FIELDS, *recorset_for_db.fields],
            limit=recorset_for_db.limit
        )
        
        # Manage JSON response
        patient = visits[0].pop('patient_id', False)
        visits[0].update({
            "patient": {
                "id": patient[0],
                "display_name": patient[1],
            },
        })

        optometrist = visits[0].pop('optometrist_id', False)
        visits[0].update({
            "optometrist": {
                "id": optometrist[0],
                "display_name": optometrist[1],
            },
        })

        return self.json_response(visits)

    # Endpoint 2 — Create Visit
    @http.route('/api/optical/visits/create', type='http', auth='none', methods=['POST'], csrf=False)
    def create_visit(self):
        # Check valid token
        try:
            self._check_auth()
        except exceptions.AccessDenied:
            return self.json_response({'error': "Invalid or missing token"}, status=401)
        
        # Read raw data
        try:
            data = json.loads(request.httprequest.data)
        except Exception:
            return self.json_response({'error': 'JSON object required'}, status=400)

        if not isinstance(data, dict):
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

        # Validate axis between 0 and 180 degrees
        if not (0 <= data.get('od_axis', 0) <= 180) or not (0 <= data.get('os_axis', 0) <= 180):
            return self.json_response({'error': 'Axis must be between 0º and 180º'}, status=400)

        # Validate addition is always positive
        if data.get('od_addition', 0) < 0 or data.get('os_addition', 0) < 0:
            return self.json_response({'error': 'Addition must be positive.'}, status=400)

        # Change dioptres to 0.25 multiples
        for field in DIOPTRE_FIELDS:
            value = data.get(field, 0)
            if value % 0.25 != 0:
                data[field] = round(value * 4) / 4

        # Registry in odoo
        new_optical_visit = CreateNewRegister(data).new_optical_visit

        # Manage JSON response
        return_data = {
            'status': 'success',
            'message': 'Optical visit created',
            'id': new_optical_visit.id,
            'reference': new_optical_visit.name,
        }

        return self.json_response(return_data, status=201)
