from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

def homepage(request):
    return render(request, 'homepage.html')

# Hardcoded data untuk 9 subkategori dengan format baru
subcategory_data = {
    "1-1": {
        "name": "Subkategori Jasa 1-1",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 100.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 150.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 1"},
            {"name": "Nama Pekerja 2"},
        ],
        "testimonials": [
            {"user": "Pengguna A", "date": "2024-11-07", "text": "Sangat puas!", "worker": "Nama Pekerja 1", "rating": 5},
        ],
    },
    "1-2": {
        "name": "Subkategori Jasa 1-2",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 120.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 180.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 3"},
            {"name": "Nama Pekerja 4"},
        ],
        "testimonials": [
            {"user": "Pengguna B", "date": "2024-11-06", "text": "Layanan bagus", "worker": "Nama Pekerja 3", "rating": 4},
        ],
    },
    "1-3": {
        "name": "Subkategori Jasa 1-3",
        "category": "Kategori Jasa 1",
        "description": "Deskripsi layanan untuk Subkategori Jasa 1-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 110.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 170.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 5"},
            {"name": "Nama Pekerja 6"},
        ],
        "testimonials": [
            {"user": "Pengguna C", "date": "2024-11-05", "text": "Sangat memuaskan!", "worker": "Nama Pekerja 5", "rating": 5},
        ],
    },
    "2-1": {
        "name": "Subkategori Jasa 2-1",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 130.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 190.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 7"},
            {"name": "Nama Pekerja 8"},
        ],
        "testimonials": [
            {"user": "Pengguna D", "date": "2024-11-04", "text": "Pengalaman yang menyenangkan.", "worker": "Nama Pekerja 7", "rating": 4},
        ],
    },
    "2-2": {
        "name": "Subkategori Jasa 2-2",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 140.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 200.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 9"},
            {"name": "Nama Pekerja 10"},
        ],
        "testimonials": [
            {"user": "Pengguna E", "date": "2024-11-03", "text": "Kualitas layanan baik.", "worker": "Nama Pekerja 9", "rating": 3},
        ],
    },
    "2-3": {
        "name": "Subkategori Jasa 2-3",
        "category": "Kategori Jasa 2",
        "description": "Deskripsi layanan untuk Subkategori Jasa 2-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 150.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 210.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 11"},
            {"name": "Nama Pekerja 12"},
        ],
        "testimonials": [
            {"user": "Pengguna F", "date": "2024-11-02", "text": "Layanan yang ramah.", "worker": "Nama Pekerja 11", "rating": 5},
        ],
    },
    "3-1": {
        "name": "Subkategori Jasa 3-1",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-1.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 160.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 220.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 13"},
            {"name": "Nama Pekerja 14"},
        ],
        "testimonials": [
            {"user": "Pengguna G", "date": "2024-11-01", "text": "Harga sesuai kualitas.", "worker": "Nama Pekerja 13", "rating": 4},
        ],
    },
    "3-2": {
        "name": "Subkategori Jasa 3-2",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-2.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 170.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 230.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 15"},
            {"name": "Nama Pekerja 16"},
        ],
        "testimonials": [
            {"user": "Pengguna H", "date": "2024-10-31", "text": "Pekerjaan rapi dan cepat.", "worker": "Nama Pekerja 15", "rating": 5},
        ],
    },
    "3-3": {
        "name": "Subkategori Jasa 3-3",
        "category": "Kategori Jasa 3",
        "description": "Deskripsi layanan untuk Subkategori Jasa 3-3.",
        "sessions": [
            {"name": "Sesi Layanan 1", "price": "Rp 180.000"},
            {"name": "Sesi Layanan 2", "price": "Rp 240.000"},
        ],
        "workers": [
            {"name": "Nama Pekerja 17"},
            {"name": "Nama Pekerja 18"},
        ],
        "testimonials": [
            {"user": "Pengguna I", "date": "2024-10-30", "text": "Akan menggunakan jasa lagi.", "worker": "Nama Pekerja 17", "rating": 4},
        ],
    },
}

def subkategori(request):
    subkategori_id = request.GET.get('id')

    # Pastikan ID subkategori ada di data
    if subkategori_id in subcategory_data:
        subcategory = subcategory_data[subkategori_id]
        # Tambahkan ID ke dalam dictionary subkategori
        subcategory['id'] = subkategori_id
        return render(request, 'subkategori.html', {'subcategory': subcategory})
    else:
        return render(request, '404.html', {'message': 'ID Subkategori tidak ditemukan atau tidak valid.'}, status=404)

orders = {}

def buat_pemesanan(request, subkategori_id):
    # Cek apakah ID subkategori valid
    if subkategori_id not in subcategory_data:
        return render(request, '404.html', {'message': 'Subkategori tidak ditemukan'}, status=404)

    subkategori = subcategory_data[subkategori_id]

    if request.method == 'POST':
        session_name = request.POST.get('session_name')

        # Cari harga sesi berdasarkan nama sesi yang dipilih
        session_data = next((s for s in subkategori["sessions"] if s["name"] == session_name), None)

        if not session_data:
            return render(request, 'buat_pemesanan.html', {'subcategory': subkategori, 'error': 'Sesi tidak valid.'})

        # Ambil harga dari data dan hilangkan "Rp" serta titik
        price = int(session_data["price"].replace("Rp ", "").replace(".", ""))

        # Cek apakah ada kode diskon
        discount_code = request.POST.get('discount_code', '').upper()
        discount_percentage = 0
        discount_codes = {
            "DISKON10": 0.1,  # 10% diskon
            "DISKON20": 0.2,  # 20% diskon
        }
        if discount_code in discount_codes:
            discount_percentage = discount_codes[discount_code]

        # Hitung total harga setelah diskon
        total_payment = price * (1 - discount_percentage)

        # Ambil username pengguna yang login
        username = request.user.username

        # Simpan data pemesanan ke dalam dictionary `orders`
        user_orders = orders.get(username, [])
        user_orders.append({
            'subcategory': subkategori['name'],
            'session_name': session_name,
            'price': f"Rp {total_payment:,.0f}".replace(",", "."),
            'date_ordered': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'pending',
        })
        orders[username] = user_orders

        # Redirect ke halaman daftar pesanan
        return redirect('daftar_pesanan')

    return render(request, 'buat_pemesanan.html', {'subcategory': subkategori})

def daftar_pesanan(request):
    username = request.user.username
    user_orders = orders.get(username, [])
    return render(request, 'daftar_pesanan.html', {'orders': user_orders})
