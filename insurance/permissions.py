def get_allowed_fields_by_role(role):
    """
    Returns allowed fields for a given user role.
    """
    role_fields = {
        'admin': '__all__',
        'agent': [
            'nationality', 'travel_from', 'package_id', 'start_date', 'end_date',
            'surname', 'given_name', 'phone_number', 'email', 'dob', 'address',
            'emergency_contact', 'passport_no', 'passport_image_path', 'profile_image_path',
            'notes'
        ],
        'viewer': ['nationality', 'travel_from', 'package_id', 'start_date', 'end_date', 'surname', 'given_name', 'phone_number', 'email', 'dob', 'address', 'emergency_contact', 'passport_no', 'passport_image_path', 'profile_image_path', 'notes'],
    }
    return role_fields.get(role, [])