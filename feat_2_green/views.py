from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Hardcoded data 
subcategory_data = {
    "1-1": {
        "name": "Subkategori Jasa 1-1",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 1"},
            {"name": "Pekerja 2"},
        ],
        "testimonials": [
            {"user": "Pengguna A", "date": "2024-11-07", "text": "Sangat puas!", "worker": "Pekerja 1", "rating": 5},
        ],
    },
    "1-2": {
        "name": "Subkategori Jasa 1-2",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 3"},
            {"name": "Pekerja 4"},
        ],
        "testimonials": [
            {"user": "Pengguna B", "date": "2024-11-06", "text": "Layanan bagus", "worker": "Pekerja 3", "rating": 4},
        ],
    },
    "1-3": {
        "name": "Subkategori Jasa 1-3",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 5"},
            {"name": "Pekerja 6"},
        ],
        "testimonials": [
            {"user": "Pengguna C", "date": "2024-11-05", "text": "Sangat memuaskan!", "worker": "Pekerja 5", "rating": 5},
        ],
    },
    "2-1": {
        "name": "Subkategori Jasa 2-1",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 7"},
            {"name": "Pekerja 8"},
        ],
        "testimonials": [
            {"user": "Pengguna D", "date": "2024-11-04", "text": "Pengalaman yang menyenangkan.", "worker": "Pekerja 7", "rating": 4},
        ],
    },
    "2-2": {
        "name": "Subkategori Jasa 2-2",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 9"},
            {"name": "Pekerja 10"},
        ],
        "testimonials": [
            {"user": "Pengguna E", "date": "2024-11-03", "text": "Kualitas layanan baik.", "worker": "Pekerja 9", "rating": 3},
        ],
    },
    "2-3": {
        "name": "Subkategori Jasa 2-3",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 11"},
            {"name": "Pekerja 12"},
        ],
        "testimonials": [
            {"user": "Pengguna F", "date": "2024-11-02", "text": "Layanan yang ramah.", "worker": "Pekerja 11", "rating": 5},
        ],
    },
    "3-1": {
        "name": "Subkategori Jasa 3-1",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 13"},
            {"name": "Pekerja 14"},
        ],
        "testimonials": [
            {"user": "Pengguna G", "date": "2024-11-01", "text": "Harga sesuai kualitas.", "worker": "Pekerja 13", "rating": 4},
        ],
    },
    "3-2": {
        "name": "Subkategori Jasa 3-2",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Pekerja 15"},
            {"name": "Pekerja 16"},
        ],
        "testimonials": [
            {"user": "Pengguna H", "date": "2024-10-31", "text": "Pekerjaan rapi dan cepat.", "worker": "Pekerja 15", "rating": 5},
        ],
    },
    "3-3": {
        "name": "Subkategori Jasa 3-3",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 250.000"},
        ],
        "workers": [
            {"name": "Pekerja 17"},
            {"name": "Pekerja 18"},
        ],
        "testimonials": [
            {"user": "Pengguna I", "date": "2024-10-30", "text": "Akan menggunakan jasa lagi.", "worker": "Pekerja 17", "rating": 4},
        ],
    },
}

def homepage(request):
    return render(request, 'homepage.html')

def subkategori(request, subcategory_id):
    # Gunakan subcategory_id langsung dari parameter
    subkategori_id = subcategory_id

    # Pastikan ID subkategori ada di data
    if subkategori_id in subcategory_data:
        subcategory = subcategory_data[subkategori_id]
        # Tambahkan ID ke dalam dictionary subkategori
        subcategory['id'] = subkategori_id
        return render(request, 'subkategori_pekerja.html', {'subcategory': subcategory})
    else:
        return render(request, '404.html', {'message': 'ID Subkategori tidak ditemukan atau tidak valid.'}, status=404)

# This will be used to temporarily store orders (session-based)
orders = {}

def buat_pemesanan(request, subkategori_id):
    # Check if the ID is valid
    if subkategori_id not in subcategory_data:
        return render(request, '404.html', {'message': 'Subkategori tidak ditemukan'}, status=404)

    subkategori = subcategory_data[subkategori_id]

    if request.method == 'POST':
        session_name = request.POST.get('session_name')
        session_data = next((s for s in subkategori["sessions"] if s["name"] == session_name), None)

        if not session_data:
            return render(request, 'buat_pemesanan.html', {'subcategory': subkategori, 'error': 'Sesi tidak valid.'})

        # Mengambil harga dan menghitung total pembayaran
        price = int(session_data["price"].replace("Rp ", "").replace(".", ""))

        # Cek apakah ada kode diskon
        discount_code = request.POST.get('discount_code', '').upper()
        discount_percentage = 0
        discount_codes = {
            "DISKON10": 0.1,
            "DISKON20": 0.2,
        }

        if discount_code in discount_codes:
            discount_percentage = discount_codes[discount_code]

        total_payment = price * (1 - discount_percentage)

        # Mengambil daftar pesanan dari session, atau buat list baru jika belum ada
        user_orders = request.session.get('orders', [])
        user_orders.append({
            'subcategory': subkategori['name'],
            'session_name': session_name,
            'price': f"Rp {total_payment:,.0f}".replace(",", "."),
            'date_ordered': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'pending',
        })

        # Menyimpan daftar pesanan kembali ke session
        request.session['orders'] = user_orders

        # Redirect ke halaman daftar pesanan
        return redirect('daftar_pesanan')

    return render(request, 'buat_pemesanan.html', {'subcategory': subkategori})

def daftar_pesanan(request):
    # Dummy data
    orders = [
        {
            'id': 1,
            'subcategory': 'Subkategori Jasa 1-2',
            'session_name': 'Sesi Layanan 1',
            'price': 'Rp 150.000',
            'worker_name': 'Pekerja 1',
            'status': 'Menunggu Pembayaran',
        },
        {
            'id': 2,
            'subcategory': 'Subkategori Jasa 2-3',
            'session_name': 'Sesi Layanan 1',
            'price': 'Rp 150.000',
            'worker_name': 'Pekerja 3',
            'status': 'Mencari Pekerja Terdekat',
        },
        {
            'id': 3,
            'subcategory': 'Subkategori Jasa 3-1',
            'session_name': 'Sesi Layanan 2',
            'price': 'Rp 150.000',
            'worker_name': 'Pekerja 5',
            'status': 'Selesai',
        },
    ]

    # Mengambil filter dari request GET
    subcategory_filter = request.GET.get('subcategory', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '').lower()

    # Memfilter data
    if subcategory_filter:
        orders = [order for order in orders if order['subcategory'] == subcategory_filter]

    if status_filter:
        orders = [order for order in orders if order['status'] == status_filter]

    if search_query:
        orders = [
            order for order in orders
            if search_query in order['worker_name'].lower() or search_query in order['session_name'].lower()
        ]

    return render(request, 'daftar_pesanan.html', {'orders': orders})
