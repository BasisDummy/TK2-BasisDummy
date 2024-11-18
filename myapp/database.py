
users_db = {
    '08521': {
        'name': 'User1',
        'password': 'user1',
        'gender': 'Male',
        'dob': '2003-04-15',
        'address': 'Palembang',
        'phone': '08521',
        'role': 'user'
    },
    '08522': {
        'name': 'User2',
        'password': 'user2',
        'gender': 'Male',
        'dob': '2001-01-21',
        'address': 'Palembang',
        'phone': '08522',
        'role': 'user'
    },
}

workers_db = {
    '08121': {
        'name': 'worker1',
        'password': 'worker1',
        'gender': 'Male',
        'dob': '1985-03-03',
        'address': 'Palembang',
        'phone': '08121',
        'bank_name': 'ovo',
        'account_number': '08121',
        'npwp': '08121',
        'photo_url': 'http://example.com/photo.jpg',
        'role': 'worker'
    },
    '08122': {
        'name': 'worker2',
        'password': 'worker2',
        'gender': 'Female',
        'dob': '1988-04-04',
        'address': 'Bandung',
        'phone': '08122',
        'bank_name': 'Gopay',
        'account_number': '08122',
        'npwp': '08122',
        'photo_url': 'http://example.com/photo2.jpg',
        'role': 'worker'
    },
}

def user_exists(phone):
    return phone in users_db

def worker_exists(phone):
    return phone in workers_db

def npwp_exists(npwp):
    return any(worker['npwp'] == npwp for worker in workers_db.values())

def add_user(name, password, gender, phone, dob, address):
    if user_exists(phone):
        raise ValueError("No HP telah terdaftar.")
    
    users_db[phone] = {
        'name': name,
        'password': password,
        'gender': gender,
        'dob': dob,
        'address': address,
        'role': 'user'
    }

def add_worker(name, password, gender, phone, dob, address, bank_name, account_number, npwp, photo_url):
    errors = []

    if worker_exists (phone):
        errors.append("No HP telah terdaftar.")

    if npwp_exists(npwp):
        errors.append("NPWP telah terdaftar.")

    for worker in workers_db.values():
        if worker['bank_name'] == bank_name and worker['account_number'] == account_number:
            errors.append("Pasangan nama bank dan nomor rekening sudah terdaftar.")

    if errors:
        raise ValueError(" | ".join(errors))

    workers_db[phone] = {
        'name': name,
        'password': password,
        'gender': gender,
        'dob': dob,
        'address': address,
        'bank_name': bank_name,
        'account_number': account_number,
        'npwp': npwp,
        'photo_url': photo_url,
        'role': 'worker'
    }