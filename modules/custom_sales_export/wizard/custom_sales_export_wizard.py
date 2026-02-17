from odoo import models, fields
# For import config in excel file
from odoo.tools import file_path
from odoo.exceptions import UserError, ValidationError
from ..utils.excel_mapper import ExcelMapper
from ..utils.mapper_to_csv import MapperToCsv
from ..utils.csv_generator import CsvGenerator


class CustomSalesExportWizard(models.TransientModel):
    _name = 'custom.sales.export.wizard'
    _description = 'Sales Export Wizard'

    date_from = fields.Date(string='Date from', required=True)
    date_to = fields.Date(string='Date to', required=True)

    file_sales_orders = fields.Binary('CSV Sales orders')
    file_sales_orders_lines = fields.Binary('CSV Sales orders lines')
    name_sales_orders = fields.Char('CSV Sales orders')
    name_sales_orders_lines = fields.Char('CSV Sales orders lines')

    def _get_config_path(self):
        return file_path('custom_sales_export/data/a3_counts_config.xlsx')

    def _get_sales_data(self):
        return self.env['sale.order'].search([
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
            ('state', 'in', ['sale']) # 'done' isn't a state of sale.order
        ])

    def action_export_to_csv(self):
        # Validate init and end date
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError("Init date can't be bigger than end date.")

        # Validate excel file
        path = self._get_config_path()
        if not path:
            raise UserError("Error: Config file not found.")

        # DB data
        sales_data = self._get_sales_data()
        # Excel data
        config_data = ExcelMapper(path)
        # CSV data
        csv_data = MapperToCsv(sales_data, config_data)
        # CSV file
        self.file_sales_orders = CsvGenerator(csv_data.sales_orders_csv).csv_file
        self.name_sales_orders = 'sales_orders.csv'

        self.file_sales_orders_lines = CsvGenerator(csv_data.sales_orders_lines_csv).csv_file
        self.name_sales_orders_lines = 'sales_orders_lines.csv'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'custom.sales.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
