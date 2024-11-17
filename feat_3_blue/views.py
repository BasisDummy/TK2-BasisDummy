from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

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
    {
        "id": 1,
        "subcategory": "Subkategori Jasa 1-1",
        "session_name": "Sesi Layanan 1",
        "price": "Rp 150.000",
        "worker_name": "Pekerja 1",
        "status": "Selesai",
    },
    {
        "id": 2,
        "subcategory": "Subkategori Jasa 2-3",
        "session_name": "Sesi Layanan 2",
        "price": "Rp 150.000",
        "worker_name": "Pekerja 3",
        "status": "Menunggu Pembayaran",
    },
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
@login_required
def buat_testimoni(request, order_id):
    # Filter pesanan selesai dari data hard-coded
    order = next((o for o in pesanan_data if o["id"] == order_id and o["status"] == "Selesai"), None)

    if not order:
        return render(request, '404.html', {"message": "Pesanan tidak ditemukan atau belum selesai."}, status=404)

    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        text = request.POST.get('text')
        new_testimoni = {
            "id": len(testimoni_data) + 1,
            "user": request.user.username,
            "worker": order["worker_name"],
            "rating": rating,
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        testimoni_data.append(new_testimoni)
        return redirect('feat_3_blue:daftar_testimoni')

    return render(request, 'feat_3_blue/buat_testimoni.html', {'order': order})

# R Testimoni: Daftar Testimoni
def daftar_testimoni(request):
    return render(request, 'feat_3_blue/daftar_testimoni.html', {'testimoni': testimoni_data})

# C Pembelian Voucher: Beli Voucher
@login_required
def beli_voucher(request, voucher_id):
    # Hardcode saldo pengguna
    saldo_pengguna = 20000  # Rp 20.000, contoh saldo
    voucher = next((v for v in voucher_data if v["id"] == voucher_id), None)
    
    if voucher:
        harga_voucher = int(voucher["harga"].replace("Rp ", "").replace(".", ""))
        if saldo_pengguna >= harga_voucher:
            # Pembelian sukses
            new_saldo = saldo_pengguna - harga_voucher
            message = f"Selamat! Anda berhasil membeli voucher kode {voucher['code']}. Voucher ini berlaku hingga {datetime.now().date() + timedelta(days=voucher['hari_berlaku'])} dengan kuota penggunaan sebanyak {voucher['kuota']} kali."
            return JsonResponse({"status": "success", "message": message, "new_saldo": new_saldo})
        else:
            # Gagal membeli voucher karena saldo tidak cukup
            return JsonResponse({"status": "error", "message": "Maaf, saldo Anda tidak cukup untuk membeli voucher ini."})
    
    return JsonResponse({"status": "error", "message": "Voucher tidak ditemukan."})

# R Diskon: Daftar Diskon
def daftar_diskon(request):
    return render(request, 'feat_3_blue/daftar_diskon.html', {'voucher_data': voucher_data, 'promo_data': promo_data})