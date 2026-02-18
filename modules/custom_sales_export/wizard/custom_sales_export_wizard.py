from odoo import models, fields
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

    file_sales_orders = fields.Binary('CSV sales orders')
    name_sales_orders = fields.Char()
    file_sales_orders_lines = fields.Binary('CSV sales orders lines')
    name_sales_orders_lines = fields.Char()

    # Get file from specific path
    def _get_config_path(self):
        return file_path('custom_sales_export/data/a3_counts_config.xlsx')

    # Get sales DB between 2 dates
    def _get_sales_data(self):
        return self.env['sale.order'].search([
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
            ('state', 'in', ['sale']) # 'done' isn't a state of sale.order
        ])

    # Action for export button
    def action_export_to_csv(self):
        # Validate init and end date
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError("Init date can't be bigger than end date.")

        # Validate excel file
        path = self._get_config_path()
        if not path:
            raise UserError("Error: Config file not found.")

        # Obtein DB data
        sales_data = self._get_sales_data()
        # Obtain Excel data mapped
        config_data = ExcelMapper(path)
        # Obtain CSV data mapped
        csv_data = MapperToCsv(sales_data, config_data)
        
        # Create CSV file
        self.file_sales_orders = CsvGenerator(csv_data.sales_orders_csv).csv_file
        self.name_sales_orders = 'sales_orders.csv'

        self.file_sales_orders_lines = CsvGenerator(csv_data.sales_orders_lines_csv).csv_file
        self.name_sales_orders_lines = 'sales_orders_lines.csv'

        # Refresh browser to show new files created
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'custom.sales.export.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
