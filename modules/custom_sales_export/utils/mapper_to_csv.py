class MapperToCsv:
    def __init__(self, sales_data, config_data):
        self.sales_data = sales_data
        self.config_data = config_data

        self.sales_orders_csv = self._create_sales_order_csv()
        self.sales_orders_lines_csv = self._create_sales_order_lines_csv()

    def _get_client_code(self, company_id):
        # If store_id(company_id) don't exist I use store 9 because seems to be generic store
        count_config = self.config_data.counts.get(company_id) or self.config_data.counts.get(9)
        
        # If store_id exist in excel return CON_ClientsUnicCuenta
        if count_config.CON_ClientsUnic.upper() == 'S':
            return count_config.CON_ClientsUnicCuenta

        # If isn't unic account, return base account because i don't have privileges to create accounts
        return self.config_data.counts.get(9).CON_ClientsUnicCuenta

    def _get_product_family(self, company_id, category_id):
        # If store_id(company_id) don't exist I use store 9 because seems to be generic store
        count_config = self.config_data.counts.get(company_id) or self.config_data.counts.get(9)
        family_config = self.config_data.counts_values.get(company_id) or self.config_data.counts_values.get(9)
        # If product_family don't exist i use product_id 14 because seems to be generic product
        # I use product_id because name is an inconsistent field (OTROS, OTROS ALCALDE ,...)
        family_line = family_config.get(category_id) or family_config.get(14)

        # If store_id exist in excel return CON_FamUnicCuenta and family label
        if count_config.CON_FamUnic.upper() == 'S':
            return {
                'family_line': family_line.CONV_Familia,
                'revenue_account_code': count_config.CON_FamUnicCuenta
            }

        # If CON_FamUnic == 'N', I return CONV_Mask and family label
        return {
            'family_line': family_line.CONV_Familia,
            'revenue_account_code': family_line.CONV_Mask
        }

    def _create_sales_order_csv(self):
        csv_data = []
        for sale in self.sales_data:
            row = {}

            row['external_id'] = sale.name
            row['order_date'] = sale.date_order.strftime('%d/%m/%Y')
            row['customer_name'] = sale.partner_id.name
            row['customer_vat'] = sale.partner_id.vat if sale.partner_id.vat else ''
            row['customer_account_code'] = self._get_client_code(sale.company_id.id)
            row['currency'] = sale.currency_id.name
            row['amount_untaxed'] = sale.amount_untaxed if sale.amount_untaxed else ''
            row['amount_tax'] = sale.amount_tax if sale.amount_tax else ''
            row['amount_total'] = sale.amount_total if sale.amount_total else ''
            row['state'] = sale.state

            csv_data.append(row)

        return csv_data

    def _create_sales_order_lines_csv(self):
        csv_data = []
        for sale in self.sales_data:
            for line in sale.order_line:
                row = {}

                row['order_external_id'] = sale.name
                row['line_id'] = line.id
                row['product_code'] = line.product_id.id
                row['product_name'] = line.product_id.name
                row['product_family'] = self._get_product_family(
                    sale.company_id.id, line.product_id.categ_id.id
                )['family_line']
                row['revenue_account_code'] = self._get_product_family(
                    sale.company_id.id, line.product_id.categ_id.id
                )['revenue_account_code']
                row['qty'] = line.product_uom_qty
                row['unit_price'] = line.price_unit
                row['discount'] = line.discount
                row['subtotal'] = line.price_subtotal
                row['total'] = line.price_total

                csv_data.append(row)

        return csv_data
