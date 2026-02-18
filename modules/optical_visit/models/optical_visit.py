from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..constants import DIOPTRE_FIELDS, VISITS_STATE


class OpticalVisit(models.Model):
    _name = 'optical.visit'
    _description = 'Optometry visits list'

    # Basic fields
    name = fields.Char(string='Visit reference', required=True, copy=False, default='New')
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)
    visit_datetime = fields.Datetime(string='Visit date', required=True, default=fields.Datetime.now)
    optometrist_id = fields.Many2one(
        'res.users', string='Optometrist', required=True, default=lambda self: self.env.user)
    state = fields.Selection(VISITS_STATE, string='State', default='draft', readonly=True)
    notes = fields.Text(string='Notes')

    # Prescription
    od_sphere = fields.Float(string='OD Sphere', default=0)
    od_cylinder = fields.Float(string='OD Cylinder', default=0)
    od_axis = fields.Integer(string='OD Axis', default=0)
    od_addition = fields.Float(string='OD Addition', default=0)
    os_sphere = fields.Float(string='OS Sphere', default=0)
    os_cylinder = fields.Float(string='OS Cylinder', default=0)
    os_axis = fields.Integer(string='OS Axis', default=0)
    os_addition = fields.Float(string='OS Addition', default=0)    

    # Actions for change state
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_complete(self):
        for record in self:
            record.state = 'completed'

    def action_reset(self):
        for record in self:
            record.state = 'draft'
    
    # Validations and visit sequences
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Validate axis between 0 and 180 degrees
            if not (0 <= vals.get('od_axis', 0) <= 180) or not (0 <= vals.get('os_axis', 0) <= 180):
                raise ValidationError('Axis must be between 0º and 180º')
            
            # Validate addition is always positive
            if vals.get('od_addition', 0) < 0 or vals.get('os_addition', 0) < 0:
                raise ValidationError('Addition must be positive.')

            # Create visit reference sequenced
            if not vals.get('name') or vals.get('name') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('optical.visit')

        return super().create(vals_list)

    # Change dioptres to 0.25 multiples
    @api.onchange(*DIOPTRE_FIELDS)
    def _revise_dioptres(self):
        for field in DIOPTRE_FIELDS:
            value = getattr(self, field)
            if value % 0.25 != 0:
                setattr(self, field, round(value * 4) / 4)
        