## Use venv

.\venv\Scripts\activate

## Launch Odoo

python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d mydb

## Launch Odoo with refreshing xml view

python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d mydb -u optical --dev xml

## Need to give Optical User permissions to edit optical visit

## API

- Create taken via web in optical_api.static_token
- Endpoint: http://localhost:8069/api/optical/visits/search
- Endpoint: http://localhost:8069/api/optical/visits/create
- Headers: 'Content-Type': 'application/json'
  'Access-Token': 'token'
- Body
