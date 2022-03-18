from core.utils.strings import html_escape

def validate_undangan(data:dict):
    results = {
        'undangan_type': None,
        'person_type': None,
        'person_name': None,
        'person_partner': None,
        'person_location': None,
        'phone_number': None,
        'is_active': False
    }
    errors = {}

    undangan_type = str(data.get('undangan_type')).strip() if data.get('undangan_type') is not None else None
    person_type = str(data.get('person_type')).strip() if data.get('person_type') is not None else None
    person_name = str(data.get('person_name')).strip() if data.get('person_name') is not None else None
    person_partner = str(data.get('person_partner')).strip() if data.get('person_partner') is not None else None
    person_location = str(data.get('person_location')).strip() if data.get('person_location') is not None else None
    phone_number =  str(data.get('phone_number')).strip() if data.get('phone_number') is not None else None
    results['is_active'] = bool(data.get('is_active')) if data.get('is_active') is not None else False

    if undangan_type is None:
        errors['undangan_type'] = 'is_required'
    elif undangan_type is not None and undangan_type != 'O' and undangan_type != 'G':
        errors['undangan_type'] = 'invalid_value'
    else:
        results['undangan_type'] = undangan_type

    if person_type is not None:
        if len(person_type) < 1 or len(person_type) > 50:
            errors['person_type'] = 'invalid_value'
        else:
            results['person_type'] = html_escape(person_type)

    if person_name is None:
        errors['person_name'] = 'is_required'
    elif len(person_name) < 1 or len(person_name) > 100:
        errors['person_name'] = 'invalid_value'
    else:
        results['person_name'] = html_escape(person_name)

    if person_partner is not None:
        if len(person_partner) < 1 or len(person_partner) > 50:
            errors['person_partner'] = 'invalid_value'
        else:
            results['person_partner'] = html_escape(person_partner)

    if person_location is not None:
        if len(person_location) < 1 or len(person_location) > 100:
            errors['person_location'] = 'invalid_value'
        else:
            results['person_location'] = html_escape(person_location)

    if phone_number is not None:
        phone_number = phone_number.replace(' ', '')
        if len(phone_number) > 0 and phone_number[0] == '+':
            phone_number = phone_number[0 : 0 : ] + phone_number[0 + 1 : :]

        if phone_number.isnumeric() is False:
            errors['phone_number'] = 'invalid_value'
        elif len(phone_number) < 10 or len(phone_number) > 15:
            errors['phone_number'] = 'invalid_length'
        else:
            results['phoone_number'] = phone_number

    if len(errors.keys()) > 0:
        return {
            'valid': False,
            'errors': errors
        }

    return {
        'valid': True,
        'data': results
    }
    