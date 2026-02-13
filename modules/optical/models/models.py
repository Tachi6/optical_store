# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OpticalVisit(models.Model):
    _name = 'optical.visit'
    _description = 'Listado de visitas optometricas'

    name = fields.Char(string='Visita', required=True, copy=False, readonly=True, default='New')
    paciente_id = fields.Many2one('res.partner', string='Paciente', required=True)
    visit_datetime = fields.Datetime(required=True)
    optometrist_id = fields.Many2one(
        'res.users', string='Optometrista', required=True, default=lambda self: self.env.user)
    state = fields.Selection(
        [('draft', 'Borrador'), ('confirmed', 'Confirmado'), ('completed', 'Completado')], 
        string='Estado', default='draft', readonly=True)
    notes = fields.Text()

    # Prescription
    od_sphere = fields.Float(string='Esfera D.', default=0)
    od_cylinder = fields.Float(string='Cilindro D.', default=0)
    od_axis = fields.Integer(string='Eje D.', default=0)
    od_addition = fields.Float(string='Adición D.', default=0)
    oi_sphere = fields.Float(string='Esfera I.', default=0)
    oi_cylinder = fields.Float(string='Cilindro I.', default=0)
    oi_axis = fields.Integer(string='Eje I.', default=0)
    oi_addition = fields.Float(string='Adición I.', default=0)

    # Actions for change state
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_complete(self):
        for record in self:
            record.state = 'completed'

    # Validate axis between 0 and 180 degrees
    @api.constrains('od_axis', 'oi_axis')
    def _check_axis(self):
        for record in self:
            for field_name in ['od_axis', 'oi_axis']:
                if not 0 <= record[field_name] <= 180:
                    raise ValidationError('El eje debe estar entre 0º y 180º')
    
    # Create visit reference sequenced
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('optical.visit')

        return super().create(vals_list)

    DIOPTRE_FIELDS = ['od_sphere','oi_sphere','od_cylinder','oi_cylinder','od_addition','oi_addition']

    # Change dioptres in 0.25 multiples
    @api.onchange(*DIOPTRE_FIELDS)
    def _revise_dioptres(self):
        for field in self.DIOPTRE_FIELDS:
            value = getattr(self, field)
            if value % 0.25 != 0:
                setattr(self, field, round(value * 4) / 4)
        
    # Write in DB (not via web) dioptres with 0.25 multiples
    def write(self, vals):
        for field in self.DIOPTRE_FIELDS:
            if field in vals and vals[field] % 0.25 != 0:
                vals[field] = round(vals[field] * 4) / 4
        return super().write(vals)
        