import csv
import base64
import io


class CsvGenerator:
    def __init__(self, csv_data):
        self.csv_data = csv_data
        self.csv_file = self._generate_csv() 
  
    def _generate_csv(self):
        # Create space in memory
        buffer = io.StringIO()
        # Create writer of csv
        writer = csv.writer(buffer, delimiter=';')
        
        # Obtain csv headers
        headers = (self.csv_data[0].keys())
        
        # Write headers
        writer.writerow(headers)

        # Write rows
        for row in self.csv_data:
            writer.writerow([row.get(header, '') for header in headers])

        # Convert
        csv_content = buffer.getvalue().encode('utf-8')
        buffer.close()

        # Encode to base64
        return base64.b64encode(csv_content)
