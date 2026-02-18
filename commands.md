## Use venv

.\venv\Scripts\activate

## Launch Odoo

python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d mydb

## Launch Odoo with refreshing xml view

python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d mydb -u optical --dev xml

## Need to give Optical User permissions to edit optical visit

## API

Para volver a crear o regenerar este token, tienes dos opciones: una manual desde la interfaz de Odoo (la más sencilla) y una automática mediante código si el token no existe.

Opción 1: Manualmente (Desde la Interfaz)
El método get_param busca en una tabla específica de Odoo llamada Parámetros del sistema. Sigue estos pasos:

Activa el Modo Desarrollador (Ajustes -> Activar modo desarrollador).

Ve a Ajustes > Técnico > Parámetros > Parámetros del sistema.

Busca en la lista la clave: optical_api.static_token.

Si existe: Edita el valor y escribe el nuevo token.

Si no existe: Haz clic en Nuevo, en "Clave" pon optical_api.static_token y en "Valor" pega tu token.

- Create taken via web in optical_api.static_token
- Endpoint: http://localhost:8069/api/optical/visits/search
- Endpoint: http://localhost:8069/api/optical/visits/create
- Headers: 'Content-Type': 'application/json'
  'Access-Token': 'token'
- Body
