from openpyxl import load_workbook


class RowMapper:
    def __init__(self, row):
        for key, value in row.items():
            setattr(self, key, value)


class ExcelMapper:
    def __init__(self, path):
        # Load excel file
        workbook = load_workbook(path, data_only=True)

        self.counts = self._get_counts_config(workbook['Config Cuentas'])
        self.counts_values = self._get_counts_values_config(workbook['Config Cuentas Values'])

        # Close excel file
        workbook.close()

    # Map Config Cuentas with this structure 
    # {
    #   (Value of CON_Tienda): {
    #       'CON_Tienda': 9,
    #       'CON_FamUnic': 'S',
    #       'CON_FamUnicCuenta': '700500009',
    #       ...      
    #   }   
    # }
    def _get_counts_config(self, worksheet):
        labels = [cell.value for cell in worksheet[1]]
        label_index = labels.index('CON_Tienda')

        rules = {}
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            rules_key = row[label_index]
            rules[rules_key] = RowMapper(dict(zip(labels, row)))

        return rules

    # Map Config Cuentas Values with this structure (filtered by CONV_Value because is
    # more consistent than a CONV_Familia string label)
    # {
    #   (Value of CONV_Tienda): {
    #       (Value1 of CONV_Value): {
    #           "CONV_Id": 8, 
    #           "CONV_Type": "CON_FamUnic",
    #           ...
    #       },
    #       (Value2 of CONV_Value): {
    #           ...
    #       },
    #   }
    # }
    def _get_counts_values_config(self, worksheet):
        labels = [cell.value for cell in worksheet[1]]

        rules = {}
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            row_dict = dict(zip(labels, row))

            store_id = row_dict['CONV_Tienda']
            family = row_dict['CONV_Value']

            if store_id not in rules:
                rules[store_id] = {}

            rules[store_id][family] = RowMapper(row_dict)

        return rules

