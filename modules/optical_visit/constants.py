VISITS_STATE = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('completed', 'Completed')]


STATES = [state[0] for state in VISITS_STATE]


FIELDS = [
    'patient_id',
    'visit_datetime',
    'optometrist_id',
    'state',
    'notes',
    'od_sphere',
    'od_cylinder',
    'od_axis',
    'od_addition',
    'os_sphere',
    'os_cylinder',
    'os_axis',
    'os_addition',
]


DIOPTRE_FIELDS = [
    'od_sphere',
    'os_sphere',
    'od_cylinder',
    'os_cylinder',
    'od_addition',
    'os_addition',
    'od_axis',
    'os_axis',
]


BASIC_FIELDS = [
    'patient_id',
    'visit_datetime',
    'optometrist_id',
    'state',
    'notes',
]