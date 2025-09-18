def validate_user_data(user):
    required_fields = ['id', 'name', 'email', 'phone']
    return all(field in user for field in required_fields)

def normalize_user_data(user):
    normalized = {
        'id': str(user['id']),
        'name': user['name'].strip().title(),
        'email': user['email'].lower().strip(),
        'phone': user['phone'].replace('-', '').replace(' ', '')
    }
    return normalized