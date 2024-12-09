from django.core.management.base import BaseCommand
from myapp.models import JobCategory, SubJobCategory, Service, User, Worker, Discount  # Ganti `myapp` dengan nama aplikasi Anda
from datetime import  datetime
from datetime import date, timedelta
import random
from decimal import Decimal

from datetime import datetime



def run():
    # Data untuk di-seed
    categories_data = [
    {
        'name': 'Home Cleaning',
        'subcategories': [
            {
                'name': 'Daily Cleaning',
                'services': [
                    {'name': 'Daily Cleaning', 'description': 'Pembersihan harian rumah', 'amount': 100000},
                    {'name': 'Daily Cleaning', 'description': 'Pembersihan harian rumah', 'amount': 180000},
                    {'name': 'Daily Cleaning', 'description': 'Pembersihan harian rumah', 'amount': 200000},
                ]
            },
            {
                'name': 'Setrika',
                'services': [
                    {'name': 'Setrika', 'description': 'Layanan setrika pakaian', 'amount': 80000},
                    {'name': 'Setrika', 'description': 'Layanan setrika pakaian', 'amount': 150000},
                    {'name': 'Setrika', 'description': 'Layanan setrika pakaian', 'amount': 160000},
                ]
            },
            {
                'name': 'Pembersihan Dapur',
                'services': [
                    {'name': 'Pembersihan Dapur', 'description': 'Membersihkan dapur dan kulkas', 'amount': 120000},
                    {'name': 'Pembersihan Dapur', 'description': 'Membersihkan dapur dan kulkas', 'amount': 200000},
                    {'name': 'Pembersihan Dapur', 'description': 'Membersihkan dapur dan kulkas', 'amount': 220000},
                ]
            },
            {
                'name': 'Kombo Cleaning + Setrika',
                'services': [
                    {'name': 'Kombo Cleaning + Setrika', 'description': 'Paket kombo pembersihan harian dan setrika', 'amount': 180000},
                    {'name': 'Kombo Cleaning + Setrika', 'description': 'Paket kombo pembersihan harian dan setrika', 'amount': 300000},
                    {'name': 'Kombo Cleaning + Setrika', 'description': 'Paket kombo pembersihan harian dan setrika', 'amount': 320000},
                ]
            },
            {
                'name': 'Kombo Cleaning + Dapur',
                'services': [
                    {'name': 'Kombo Cleaning + Dapur', 'description': 'Paket kombo pembersihan harian dan dapur', 'amount': 200000},
                    {'name': 'Kombo Cleaning + Dapur', 'description': 'Paket kombo pembersihan harian dan dapur', 'amount': 350000},
                    {'name': 'Kombo Cleaning + Dapur', 'description': 'Paket kombo pembersihan harian dan dapur', 'amount': 380000},
                ]
            },
            {
                'name': 'Full Deep Cleaning',
                'services': [
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 250000},
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 400000},
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 420000},
                ]
            },
        ]
    },
    {
        'name': 'Deep Cleaning',
        'subcategories': [
            {
                'name': 'Full Deep Cleaning',
                'services': [
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 250000},
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 400000},
                    {'name': 'Full Deep Cleaning', 'description': 'Pembersihan mendalam seluruh rumah', 'amount': 420000},
                ]
            },
        ]
    },
    {
        'name': 'Service AC',
        'subcategories': [
            {
                'name': 'Cuci AC',
                'services': [
                    {'name': 'Cuci AC', 'description': 'Servis dan cuci AC', 'amount': 150000},
                    {'name': 'Cuci AC', 'description': 'Servis dan cuci AC', 'amount': 250000},
                    {'name': 'Cuci AC', 'description': 'Servis dan cuci AC', 'amount': 270000},
                ]
            },
        ]
    },
    {
        'name': 'Massage',
        'subcategories': [
            {
                'name': 'Pijat Refleksi',
                'services': [
                    {'name': 'Pijat Refleksi', 'description': 'Layanan pijat refleksi', 'amount': 120000},
                    {'name': 'Pijat Refleksi', 'description': 'Layanan pijat refleksi', 'amount': 220000},
                    {'name': 'Pijat Refleksi', 'description': 'Layanan pijat refleksi', 'amount': 240000},
                ]
            },
        ]
    },
    {
        'name': 'Hair Care',
        'subcategories': [
            {
                'name': 'Hair Treatment',
                'services': [
                    {'name': 'Hair Treatment', 'description': 'Perawatan rambut', 'amount': 100000},
                    {'name': 'Hair Treatment', 'description': 'Perawatan rambut', 'amount': 180000},
                    {'name': 'Hair Treatment', 'description': 'Perawatan rambut', 'amount': 190000},
                ]
            },
            {
                'name': 'Hair Spa',
                'services': [
                    {'name': 'Hair Spa', 'description': 'Spa untuk rambut', 'amount': 120000},
                    {'name': 'Hair Spa', 'description': 'Spa untuk rambut', 'amount': 200000},
                    {'name': 'Hair Spa', 'description': 'Spa untuk rambut', 'amount': 210000},
                ]
            },
        ]
    },
]

    # Daftar pengguna
    users = [
        {
            'name': 'Heri Setyawan',
            'password': '083853797950',
            'gender': 'L',
            'date': '1990-11-05',
            'phone': '083853797950',
            'saldo': 750000,
            'address': 'Jl. Mangga No. 2'
        },
        {
            'name': 'Savitri',
            'password': 'passwDD',
            'gender': 'P',
            'date': '1990-12-02',
            'phone': '081111111112',
            'saldo': 750000,
            'address': 'Jl. Mangga No. 2'
        },
        {
            'name': 'Kinar',
            'password': 'paSSword',
            'gender': 'P',
            'date': '1997-04-04',
            'phone': '081111111114',
            'saldo': 250000,
            'address': 'Jl. Apel No. 4'
        },
        {
            'name': 'Nawa',
            'password': 'passwWORd',
            'gender': 'P',
            'date': '2001-06-06',
            'phone': '081111111117',
            'saldo': 400000,
            'address': 'Jl. Melon No. 6'
        },
        {
            'name': 'Adel',
            'password': 'passTword',
            'gender': 'P',
            'date': '2006-08-08',
            'phone': '081111111119',
            'saldo': 800000,
            'address': 'Jl. Stroberi No. 8'
        },
        {
            'name': 'Cia',
            'password': 'passwordPP',
            'gender': 'P',
            'date': '2008-10-10',
            'phone': '081111111110',
            'saldo': 50000,
            'address': 'Jl. Lemon No. 10'
        }
    ]

    # Daftar pekerja
    workers = [
        {
            'name': 'Fachri',
            'password': 'PAssWOrd',
            'gender': 'L',
            'phone': '081111111116',
            'dob': datetime(2003, 5, 5),  # Tanggal lahir
            'saldo': 1000000,
            'address': 'Jl. Pisang No. 5',
            'account_number': '1111111111',
            'bank_name': 'gopay',
            'npwp': 'NPWP1',
            'photo_url': 'https://example.com/foto1.jpg'
        },
        {
            'name': 'Ramadhan',
            'password': 'PAssword',
            'gender': 'L',
            'phone': '081111111111',
            'dob': datetime(1980, 11, 1),
            'saldo': 500000,
            'address': 'Jl. Rambutan No. 1',
            'account_number': '1111111112',
            'bank_name': 'ovo',
            'npwp': 'NPWP2',
            'photo_url': 'https://example.com/foto2.jpg'
        },
        {
            'name': 'Fawwi',
            'password': 'passworKK',
            'gender': 'L',
            'phone': '081111111118',
            'dob': datetime(2004, 7, 7),
            'saldo': 350000,
            'address': 'Jl. Nanas No. 7',
            'account_number': '1111111113',
            'bank_name': 'bca',
            'npwp': 'NPWP3',
            'photo_url': 'https://example.com/foto3.jpg'
        },
        {
            'name': 'Zac',
            'password': 'password3',
            'gender': 'L',
            'phone': '081111111113',
            'dob': datetime(1995, 3, 3),
            'saldo': 300000,
            'address': 'Jl. Jeruk No. 3',
            'account_number': '1111111114',
            'bank_name': 'bni',
            'npwp': 'NPWP4',
            'photo_url': 'https://example.com/foto4.jpg'
        },
        {
            'name': 'Gege',
            'password': 'passwordSD',
            'gender': 'L',
            'phone': '081111111115',
            'dob': datetime(2007, 9, 9),
            'saldo': 150000,
            'address': 'Jl. Anggur No. 9',
            'account_number': '1111111115',
            'bank_name': 'mandiri',
            'npwp': 'NPWP5',
            'photo_url': 'https://example.com/foto5.jpg'
        },
        {
            'name': 'Developer',
            'password': '08888888888',
            'gender': 'L',
            'phone': '08888888888',
            'dob': datetime(2007, 9, 9),
            'saldo': 150000,
            'address': 'Jl. Anggur No. 9',
            'account_number': '111111199',
            'bank_name': 'bni',
            'npwp': 'NPWP52',
            'photo_url': 'https://example.com/foto5.jpg'
        }
    ]

    promo_codes = ['PROMO2024', 'SALE50', 'NEWYEAR10', 'DISCOUNT30', 'BLACKFRIDAY15', 'PROMO10', 'PROMO20']

    for promo_code in promo_codes:  # Menghasilkan 10 data diskon sebagai contoh

        if 'PROMO' in promo_code:
            code = promo_code
            percentage = 10  # Diskon antara 5% hingga 50%
            min_transaction = 150000  # Minimal transaksi antara 50 hingga 500
            max_usage = 2  # Maksimum penggunaan antara 1 hingga 100
            usage_quota = random.randint(0, max_usage)  # Kuota penggunaan diskon
            voucher_price = 0  # Harga voucher antara 50,000 hingga 100,000
            expired_date = date.today() + timedelta(days=random.randint(0, 30))
            # Buat dan simpan objek Discount
            discount = Discount.objects.create(
                code=code,
                percentage=Decimal(percentage),
                min_transaction=min_transaction,
                max_usage=max_usage,
                usage_quota=usage_quota,
                voucher_price=voucher_price,
                expired_date=expired_date
            )

        else:
            code = promo_code
            percentage = random.randint(5, 50)  # Diskon antara 5% hingga 50%
            min_transaction = 150000  # Minimal transaksi antara 50 hingga 500
            max_usage = random.randint(1, 100)  # Maksimum penggunaan antara 1 hingga 100
            usage_quota = random.randint(0, max_usage)  # Kuota penggunaan diskon
            voucher_price = Decimal(random.randint(50000, 100000))  # Harga voucher antara 50,000 hingga 100,000
            expired_date = date.today() + timedelta(days=random.randint(0, 30))

            # Buat dan simpan objek Discount
            discount = Discount.objects.create(
                code=code,
                percentage=Decimal(percentage),
                min_transaction=min_transaction,
                max_usage=max_usage,
                usage_quota=usage_quota,
                voucher_price=voucher_price,
                expired_date=expired_date
            )


    for user in users:
        User.objects.create(
            name=user['name'],
            password=user['password'],
            # gender=user['gender'],
            phone=user['phone'],
            saldo=user['saldo'],
            address=user['address'],
        )

    for worker in workers:
        Worker.objects.create(
            name=worker['name'],
            password=worker['password'],
            gender=worker['gender'],
            phone=worker['phone'],
            saldo=worker['saldo'],
            address=worker['address'],
            dob=worker['dob'],
            account_number=worker['account_number'],
            bank_name=worker['bank_name'],
            photo_url=worker['photo_url'],
            npwp=worker['npwp']
        )


    # Menyimpan data ke dalam database
    for category_data in categories_data:
        category = JobCategory.objects.create(name=category_data['name'])
        for subcategory_data in category_data['subcategories']:
            subcategory = SubJobCategory.objects.create(
                category=category,
                name=subcategory_data['name']
            )
            for service_data in subcategory_data['services']:
                Service.objects.create(
                    sub_category=subcategory,
                    name=service_data['name'],
                    description=service_data['description'],
                    amount=service_data['amount']
                )

    print("data success di seeder")
