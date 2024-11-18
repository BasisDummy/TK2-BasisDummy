from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

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

# Data dummy untuk diskon
diskon_data = [
    {"id": 1, "code": "DISKON10", "description": "Diskon 10% untuk semua layanan", "discount_percentage": 10},
    {"id": 2, "code": "DISKON20", "description": "Diskon 20% untuk pelanggan baru", "discount_percentage": 20},
]

# Data dummy untuk testimoni
testimoni_data = [
    {"id": 1, "user": "Pengguna A", "worker": "Pekerja 1", "rating": 5, "text": "Sangat puas!", "date": "2024-11-07"},
    {"id": 2, "user": "Pengguna B", "worker": "Pekerja 3", "rating": 4, "text": "Layanan bagus", "date": "2024-11-06"},
]

# Data dummy untuk pesanan jasa
pesanan_data = [
    {'id': 1, 'subcategory': '1-2', 'worker_name': 'Pekerja 1', 'status': 'Selesai'},
    {'id': 2, 'subcategory': '2-3', 'worker_name': 'Pekerja 3', 'status': 'Mencari Pekerja Terdekat'},
    {'id': 3, 'subcategory': '3-1', 'worker_name': 'Pekerja 5', 'status': 'Selesai'},
]

# Data Dummy untuk Voucher dan Promo
voucher_data = [
    {"id": 1, "code": "VOUCHER10", "potongan": "10%", "min_transaksi": "Rp 100.000", "hari_berlaku": 30, "kuota": 5, "harga": "Rp 10.000"},
    {"id": 2, "code": "VOUCHER20", "potongan": "20%", "min_transaksi": "Rp 200.000", "hari_berlaku": 15, "kuota": 3, "harga": "Rp 20.000"},
]

promo_data = [
    {"id": 1, "code": "PROMO15", "expiry_date": "2024-12-31"},
    {"id": 2, "code": "PROMO25", "expiry_date": "2024-11-30"},
]

# CR Testimoni: Buat Testimoni Baru
def buat_testimoni(request, order_id):
    # Cari pesanan berdasarkan ID dan status
    order = next((o for o in pesanan_data if o["id"] == order_id and o["status"] == "Selesai"), None)

    if not order:
        return render(request, '404.html', {"message": "Pesanan tidak ditemukan atau belum selesai."}, status=404)

    if request.method == 'POST':
        # Ambil data dari form
        rating = int(request.POST.get('rating'))
        text = request.POST.get('text')
        new_testimoni = {
            "id": len(testimoni_data) + 1,
            "user": request.user.username if request.user.is_authenticated else "Anonim",
            "worker": order["worker_name"],
            "rating": rating,
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }

        # Tambahkan testimoni ke subkategori terkait
        subcategory_id = order['subcategory']  # Ambil subkategori dari pesanan
        if subcategory_id in subcategory_data:
            subcategory_data[subcategory_id]['testimonials'].append(new_testimoni)

        # Redirect ke halaman subkategori
        return redirect('feat_2_green:subkategori', subcategory_id=subcategory_id)

    return render(request, 'buat_testimoni.html', {'order': order, 'range': range(1, 6)})

# C Pembelian Voucher: Beli Voucher
def beli_voucher(request, voucher_id):
    from datetime import datetime, timedelta

    # Hardcode saldo pengguna
    saldo_pengguna = 5000  # Rp 5.000, contoh saldo
    voucher = next((v for v in voucher_data if v["id"] == voucher_id), None)
    
    if voucher:
        try:
            harga_voucher = int(voucher["harga"].replace("Rp ", "").replace(".", ""))
        except ValueError:
            return JsonResponse({"status": "error", "message": "Harga voucher tidak valid."})

        if saldo_pengguna >= harga_voucher:
            # Pembelian sukses
            new_saldo = saldo_pengguna - harga_voucher
            expiry_date = (datetime.now() + timedelta(days=voucher['hari_berlaku'])).strftime('%Y-%m-%d')
            return JsonResponse({
                "status": "success",
                "message": f"Selamat! Anda berhasil membeli voucher kode {voucher['code']}.",
                "new_saldo": new_saldo,
                "code": voucher['code'],
                "expiry_date": expiry_date,
                "quota": voucher['kuota']
            })
        else:
            return JsonResponse({"status": "error", "message": "Saldo Anda tidak cukup untuk membeli voucher ini."})

    return JsonResponse({"status": "error", "message": "Voucher tidak ditemukan."})

# R Diskon: Daftar Diskon
def daftar_diskon(request):
    return render(request, 'daftar_diskon.html', {'voucher_data': voucher_data, 'promo_data': promo_data})

def daftar_testimoni(request):
    testimoni_data = [
        {"id": 1, "user": "User1", "worker": "Pekerja1", "rating": 5, "text": "Bagus!", "date": "2024-11-17"},
        {"id": 2, "user": "User2", "worker": "Pekerja2", "rating": 4, "text": "Cukup baik.", "date": "2024-11-16"},
    ]
    return render(request, 'daftar_testimoni.html', {'testimoni_data': testimoni_data})