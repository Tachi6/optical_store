from ..constants import DIOPTRE_FIELDS, STATES


class RecorsetForDB:
    def __init__(self, kwargs, data):
        self.data = data
        self.kwargs = kwargs

        self.domain = self._obtain_domain()
        self.limit = self._obtain_limit()
        self.fields = self._obtain_fields()

    def _obtain_domain(self):
        domain = []

        raw_state = self.kwargs.get('state')
        # Check if state exist and if valid, if not pass and see all states
        if raw_state:
            if raw_state in STATES:
                domain.append(('state', '=', raw_state))

        raw_optometrist_id = self.kwargs.get('optometrist_id')
        # Check if optometrist id exist, if not pass and return all optometrist 
        if raw_optometrist_id:
            try:
                optometrist_id = int(raw_optometrist_id)
                if optometrist_id > 0:
                    domain.append(('optometrist_id', '=', optometrist_id))
            except:
                pass

        patient_id = self.kwargs.get('patient_id')
        # Check if patient id exist, if not pass and return all patient 
        if patient_id:
            try:
                patient_id = int(patient_id)
                if patient_id > 0:
                    domain.append(('patient_id', '=', patient_id))
            except:
                pass
            
        return domain
            
    def _obtain_limit(self):
        limit = 10
        # Check if limit exist and is not negative, if not pass and show 10 results
        try:
            limit = max(1, int(self.kwargs.get('limit', 0)))
        except:
            pass
        
        return limit
    
    def _obtain_fields(self):
        raw_fields = self.data.get('fields')
        # Check if fields is a list and exist
        fields = DIOPTRE_FIELDS
        if isinstance(raw_fields, list):
            # Only add valid fields
            fields = [field for field in raw_fields if field in DIOPTRE_FIELDS]

        # If fields are invalid then length is 0 and return all fields
        return fields if len(fields) != 0 else DIOPTRE_FIELDS
