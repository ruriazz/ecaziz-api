from core.utils.strings import html_escape
from applications.undangan.models import Undangan

def validate_data_ucapan(data):
    errors = {}
    results = {
        'undangan': int(data.get('undangan')) if data.get('undangan', '') != '' else None,
        'sender': str(data.get('sender')).strip() if data.get('sender', '') != '' else None,
        'text': str(data.get('text')).strip() if data.get('text', '') != '' else None,
        'is_active': int(data.get('is_active')) if str(data.get('is_active', '')).isnumeric() else 1
    }

    if results.get('undangan') is None:
        errors['undangan'] = 'is_required'
    else:
        undangan = Undangan.objects.filter(id=results.get('undangan')).exists()
        if not undangan:
            errors['undangan'] = 'data_not_found'
        else:
            results['undangan'] = Undangan.objects.get(id=results.get('undangan'))
            if not results.get('undangan').is_active:
                errors['undangan'] = 'data_not_found'

    if results.get('sender') is None:
        errors['sender'] = 'is_required'
    else:
        if len(results.get('sender')) < 1 or len(results.get('sender')) > 100:
            errors['sender'] = 'invalid_length'
        else:
            results['sender'] = html_escape(results.get('sender'))

    if results.get('text') is None:
        errors['text'] = 'is_required'
    else:
        if len(results.get('text')) < 1 or len(results.get('text')) > 500:
            errors['text'] = 'invalid_length'
        else:
            results['text'] = html_escape(results.get('text'))

    if results.get('is_active') != 0 and results.get('is_active') != 1:
        errors['is_active'] = 'invalid_value'

    if len(errors.keys()) > 0:
        return {
            'valid': False,
            'errors': errors
        }
    
    return {
        'valid': True,
        'data': results
    }