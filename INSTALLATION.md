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
