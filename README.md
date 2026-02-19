# Optical Store

## Prerequisites (tested on these versions)

- Python v3.11.9
- PIP v24.0
- Git v2.50.0
- PostgreSQL v18.2

## Installation Guide

1.  Clone Optical Store (based in Odoo 17.0 branch with production commits only)
    `git clone --branch production --single-branch --depth 19 https://github.com/Tachi6/optical_store.git`

2.  Navigate to the project folder
    `cd optical_store`

3.  Create and activate a Python virtual environment (recommended):
    - Windows
      `python -m venv venv`
      `venv\Scripts\activate`
    - macOS/Linux:
      `source venv/bin/activate`

4.  Install required Python packages
    `pip install setuptools wheel`
    `pip install -r requirements.txt`

5.  Configure PostgreSQL Role via pgAdmin
    - In PostgreSQL, go to Object > Create > Login/Group Role.
    - Role Name: odoo
    - Definition tab: Set password to odoo.
    - Privileges tab: Toggle Can login and Superuser to Yes.
    - Click Save.

6.  Launch Odoo initializing DB
    `python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d optical_store -i base`

7.  Enter credentials
    - User: admin
    - Password: admin

8.  Go to Apps menu, and install this modules
    - Sales
    - Custom Sales Export
    - Optical Visit

9.  Go to Settings => General Settings => Users => Manage Users
    - Select your active user
    - In technical, give Optical User permissions
    - Save settings

10. Go to Settings => Technical => Parameters => System Parameters
    - Create new entry for password for API calls
    - Key: optical_api.static_token
    - Password: test_secret_token_123456
    - Save new entry

11. Close Odoo session via terminal (Crtl + C or Cmd + C)

12. Restart Odoo with this default command to open
    `python odoo-bin -r odoo -w odoo --addons-path="addons,modules" -d optical_store`

13. Optical Store is ready to use

## Optical Visit module

### Estructura

Aquest mòdul permet crear i manipular visites optomètriques desde web o desde petició API. Està creat com un mòdul independentment de Odoo. Depèn dels addons oficials "base" i "contacts". Està estructurat seguint la base dels mòduls de Odoo, amb la següent estructura i carpetes:

- models (optical.visit)
  - Basic fields (cal omplir sempre patient_id i optometrist_id)
    - name: Crea una referència única seqüencial del tipus VISIT/000000001.
    - patient_id: És un Many2one de res.partner, on seleccionar els clients existents.
    - visit_datetime: Automàticament guarda la data actual en crear la visita, pero es pot modificar.
    - optometrist_id: És un Many2one de res.users, on seleccionar els usuaris existents, per defecte selecciona el usuari utilitzat.
    - state: Per defecte és "draft" en guardar, però només permet "draft", "confirmed" o "completed".
  - Prescription fields (tots opcionals)
    - sphere, cylinder and addition: Per defecte són 0 i s'arrodoneixen a multiples de 0.25 i sempre mostren el signe +/-.
    - axis: Sempre mostres el caràcter dels graus (º).
  - Validacions:
    - axis: sempre han d'estar entre 0 i 180, sinó llença error de validació.
    - addition: sempre ha de ser positiva, sinó llença error de validació.
  - Accions:
    - state: 3 accions per canviar entre els 3 estats disponibles.

- views
  - Menus
    - Una vista per al selector d'apps, que obre el mòdul.
    - Una vista dins la barra d'estat, que ens obre el formulari.
  - Vistas
    - Un formulari amb el seu header (botons de creació, buscador i filtres), la taula amb les visites òptiques i l'acció per obrir aquest formulari.

- controllers
  - Un controlador per gestionar les peticions http des de fora de Odoo.

- data
  - Un arxiu xml necessari per crear la seqüencia del field name.

- security
  - Un arxiu csv amb els permisos per poder utilitzar aquest mòdul.
  - Un arxiu xml per crear el nou rang d'usuari necessari.

- static
  - Un arxiu per visualment mostrar el símbol de graus (º), no es guarda a la base de dades.
  - Un arxiu per visualment mostrar +/- en els fields de diòptries, no es guarda el + a la base de dades.

- utils
  - Una clase auxiliar per crear nous registres a DB desde l'API.
  - Una clase auxiliar per crear la demanda de dades a la DB desde l'API.

- constants.py: Inclou les variables que no canviaran mai durant l'execució.

### Funcionament

#### Vista principal

El mòdul segueix la funcionalitat estàndard dels mòduls de Odoo. La vista del formulari és una taula amb filtres i buscador per veure totes les visites resumides. Amb el botó "New" podem crear una nova visita.

#### Vista nova visita

Per crear una nova visita realment només requereix omplir el camp del pacient i de l'optometrista, encara que aquest últim selecciona per defecte l'usuari actual. Tots els camps de prescripció són opcionals perquè pot ser que hi hagi prescripcions que siguin 0. No deixa guardar la prescripció si no es compleixen les validacions respectives:

- L'eix de tots 2 ulls ha d'estar entre 0º i 180º.
- El pacient ha d'estar seleccionat.
- L'adició ha de ser sempre positiva.

Tambè inclou els botons respectius per canviar l'estat de la visita, i mostra en quin estat està la visita.

### Peticions HTTP

Es poden fer peticions http per obtenir les dades de DB (search) i per crear noves graduacions (create). Està configurat amb el tipus http, per permetre la utilització dels paràmetres query, i aixi s'asembli mes a l'utilització més comú de les API. Totes 2 comproven que el token d'acces sigui correcte i que el body sigui un objecte vàlid (i obligatori en la petició create). Per utilitzar totes 2 requerim d'aquests **Headers**:

- Content-Type: application/json
- Access-Token: test_secret_token_123456

La contrasenya l'hem creat a l'instal·lació perquè és molt més segur que tenir-la al codi, i s'ha de ser administrador per canviar-la.

#### Search

La petició search utilitza aquesta **base** (localhost perquè ara només esta en local i el port que utilitzeu):
`http://localhost:8069/api/optical/visits/search`

Admet els seguents paramètres **query** que es poden combinar (la resta són ignorats):

- state (admet draft, confirmed, completed, si no es cap dels 3 retorna tots):
  `http://localhost:8069/api/optical/visits/search?state=draft`
- patient_id (comprova que el id existeixi a la DB i sigui int, sino retorna tots els pacients):
  `http://localhost:8069/api/optical/visits/search?patient_id=1`
- optometrist_id (comprova que el id existeixi a la DB i sigui int, sino retorna tots els optometristes):
  `http://localhost:8069/api/optical/visits/search?optometrist_id=1`
- limit (comprova que sigui int i positiu, sino per defecte retorna 10):
  `http://localhost:8069/api/optical/visits/search?limit=10`

En el **body** d'aquesta petició http podem adjuntar un objecte amb la clau **fields** que contingui una llista amb les propietats que volem veure a la resposta que ens retorna. Per defecte retorna totes les propietats. Les que són opcionals son od_sphere, os_sphere, od_cylinder, os_cylinder, od_addition, os_addition, od_axis i os_axis. Comprova que sigui una llista i vàlida. Si aquesta llista conté propietats que no són de la prescripció les omet i si al final no hi ha cap de vàlida retorna totes les propietats.

`{
  "fields": ["od_sphere", "os_sphere"]
}`

#### Create

La petició search utilitza aquesta **base** (localhost perquè ara només esta en local i el port que utilitzeu):
`http://localhost:8069/api/optical/visits/create`

Aqui els paràmetres **query** són ignorats.

Necessita un **body** i amb l'estructura d'objecte correcte i amb els camps obligatoris patient_id i optometrist_id. Aquests altres es poden afegir, però sinò son autogenerats: state, od_sphere, od_cylinder, od_axis, od_addition, os_sphere, os_cylinder, os_axis, os_addition. El camp notes es pot afegir pero no es autogenerat sinò s'afegueix. El **body** ha de tenir una estructura com aquesta per ser vàlid.

`{
  "patient_id": 1,
  "optometrist_id": 2,
  "od_sphere": -1.55,
  "os_sphere": -1.95
}`

Aquest té totes aquestes validacions:

- Valida que quehi hagi el patient_id i el optometrit_id.
- Valida els axis entre 0º i 180º.
- Valida les addition que siguin positives.
- Adjusta els valors de diòptries en multiples de 0.25.

## Custom Export Sales module

### Estructura

Aquest mòdul permet exportar en un fitxer csv les vendes que estiguin a l'estat "sale" ("done" no existeix a sales) entre 2 dates seguint les regles d'un arxiu excel adjunt. Està creat com un mòdul independentment de Odoo per afegir funcionalitat al addon "sale" i depèn d'ell mitjançant un wizard, un mòdul transitori per crear dialegs interactius. Està estructurat amb la següent estructura i carpetes:

- wizard (custom.sales.export.wizard: model que s'exten de "TransientModel" per fer la funcionalitat de wizard)
  - date_from: Data d'inici de la consulta de vendes a la base de dades (obligatoria).
  - date_to: Data de final de la consulta de vendes a la base de dades (obligatoria).
  - file_sales_orders: Field on generar posteriorment un dels arxius csv.
  - name_sales_orders: Name per arxiu anterior.
  - file_sales_orders_lines: Field on generar posteriorment un dels arxius csv.
  - name_sales_orders_lines: Name per arxiu anterior.
  - file_patch: Paquet propi de Odoo per importar l'arxiu.
  - env.search: Per obtenir les dades de la BD entre les 2 dates.
  - action_export_to_csv: Acció per exportar a csv amb validació de dates i de que l'arxiu existeixi.

- views
  - Menus
    - Una vista dins la barra d'estat de Sales (creat aqui dins perque queda més integrat a Sales), abans dels Settings de Sales, i que obre el wizard.
  - Vistas
    - Un formulari interactiu amb el selector de dates i els botons d'exportar. Un cop generats els arxius csv surten tambè en aques formulari, per descarregar o esborrar independenment un de l'altre.

- security
  - Un arxiu csv amb els permisos per poder utilitzar aquest mòdul, el pot utilitzar tothom.

- data
  - Conte l'excel amb les regles per exportar a csv.

- utils
  - Una clase auxiliar per mapejar el excel.
  - Una clase auxiliar per mapejar dades i crear la base pel generador de csv.
  - Una clase auxiliar per generar els fitxers csv.

### Funcionament

#### Botó i vistes

El funcionament és molt simple, dins de la vista de Sales, amb el botó "Export to CSV" se'ns obre una nova finestra amb un selector de dates. Escollim les dates i generem els arxius amb el botó "Export". Ens apareixeran 2 arxius al formulari que podrem descarregar o esborrar. Odoo al cap d'una estona de tancar la finestra ell sol els esborra. Si la data d'inici és posterior a la de final en llençarà un Validation Error.

### Mapejos

#### Config Cuentas

La fulla "Config Cuentas" del excel l'he mapejat per crear una estructura com aquesta:

`{
  (Value of CON_Tienda): {
      'CON_Tienda': 9,
      'CON_FamUnic': 'S',
      'CON_FamUnicCuenta': '700500009',
      ...      
  }   
}`

Aquest valor "Value of CON_Tienda" és el que hem permet enllaçar-ho amb la base de DB de "sale". A la DB de "sale" he considerat que la referència per una botiga dins d'una empresa seria el "company_id" i seria la que aniria a buscar al excel mapejat.

#### Config Cuentas Values

La fulla "Config Cuentas Values" del excel l'he mapejat per crear una estructura com aquesta:

`{
  (Value of CONV_Tienda): {
      (Value1 of CONV_Value): {
          "CONV_Id": 8, 
          "CONV_Type": "CON_FamUnic",
          ...
      },
      (Value2 of CONV_Value): {
          ...
      },
  }
}`

Aquest valor "Value of CONV_Tienda" segueix el mateix patró que el "Value of CON_Tienda" anterior. La següent agrupació de famílies per a cada botiga ha sigut pel "CONV_Value," que he considerat que seria el id de la família, ja que a cada botiga el id era el mateix i només afegia el nom de la botiga a la descripció de la família. Aquest id de família he considerat que seria a la DB el "product_id.categ_id" i seria el segon que aniria a buscar al excel mapejat.

#### CSV create_sales_order

A l'hora de crear les dades per aquest csv, en la columna que s'havia de calcular (customer_account_code), si aquell "company_id" no existís en l'excel, l'he assignat el que em semblava que era el id genèric de botiga, el 9 (estava marcat en groc i conté les famílies de productes per defecte). Si requeria que fos botiga amb el mateix codi de compte retornava el codi de compte corresponent de l'excel, sinó retornava el codi genèric, perquè no soc de comptabilitat ni tinc poders per crear codis de comptes nous. La resta de dades pel csv són els valors demanats que corresponen als mateixos en la DB de Odoo. Com a consideració, a les dades que no eren obligatòries en la DB de Odoo els he assignat un string buit si no existien, i la data l'he transformat a un format més adient.

#### CSV create_sales_order_lines

Per crear les dades per aquest csv, havia de calcular 2 columnes, "product_family" i "revenue_account_code". Totes 2 van lligades de la mà. Igual que al csv anterior, si aquell "company_id" no existís en l'excel, l'he assignat el que em semblava que era el id genèric de botiga, el 9, tant per la fulla "Config Cuentas" com per la "Config Cuentas Values". A la fulla "Config Cuentas Values", he considerat que si el "product_id.categ_id" no existís, utilitzaria el que m'ha semblat genèric, el 14, pel mateix motiu que la secció anterior.
Si aquella botiga requeria un codi de compte de família únic, assignava el que deia el excel a la columna "CON_FamUnicCuenta", i pel "product_family" assignava el "CONV_Familia" que coincidia i sinó "CONV_Familia" genèric (14). Si no requeria un codi de compte de família únic, utilitzava el "CONV_Mask" respectiu i sinó existís el "CONV_Mask" genèric (14), i pel "product_family" igual que abans.
