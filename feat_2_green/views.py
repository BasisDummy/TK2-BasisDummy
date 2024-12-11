from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
import psycopg2
from feat_2_green.connect import get_db_connection
from django.views.decorators.http import require_http_methods
import uuid
from django.views.decorators.csrf import csrf_exempt



# Homepage udah bener semua
# Subkategori  nama pekerja bisa di klik, yang buat pekerja belum di handle
# Pemesanan totally belum
# View Pemesanan 50% belum
def homepage(request):
    connection = get_db_connection()
    cursor = connection.cursor()
        # Ambil semua kategori dan subkategori yang terhubung
    cursor.execute("""
        SELECT 
            kj.Id AS KategoriId, 
            kj.Nama, 
            sj.Id AS SubkategoriId, 
            sj.NamaSubkategori
        FROM 
            KATEGORI_JASA kj
        LEFT JOIN 
            SUBKATEGORI_JASA sj ON kj.Id = sj.KategoriJasald
        ORDER BY 
            kj.Id, sj.Id
    """)
    results = cursor.fetchall()

    # Format hasil query menjadi dictionary yang dikelompokkan berdasarkan kategori
    categories = {}
    for row in results:
        kategori_id, kategori_name, subkategori_id, subkategori_name = row

        if kategori_id not in categories:
            categories[kategori_id] = {
                'id': kategori_id,
                'name': kategori_name,
                'subcategories': []
            }

        if subkategori_id:
            categories[kategori_id]['subcategories'].append({
                'id': subkategori_id,
                'name': subkategori_name
            })

    # Konversi dictionary ke list untuk keperluan rendering template
    categories_list = list(categories.values())

    return render(request, 'homepage.html', {'categories': categories_list})


def subkategori(request, subcategory_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # Ambil data subkategori
        cursor.execute("""
            SELECT DISTINCT
                sj.Id AS SubkategoriId, 
                sj.NamaSubkategori, 
                sj.Deskripsi, 
                kj.Nama AS KategoriNama
            FROM SUBKATEGORI_JASA sj
            JOIN KATEGORI_JASA kj ON sj.KategoriJasald = kj.Id
            WHERE sj.Id = %s
        """, [subcategory_id])
        subcategory = cursor.fetchone()

        if not subcategory:
            return render(request, '404.html', {'message': 'Subkategori tidak ditemukan.'}, status=404)

        # Ambil sesi layanan beserta nama pekerja
        cursor.execute("""
            SELECT DISTINCT 
                sl.Sesi, 
                sl.Harga, 
                pengguna.Nama AS NamaPekerja
            FROM SESI_LAYANAN sl
            LEFT JOIN TR_PEMESANAN_JASA tpj ON sl.SubkategoriId = tpj.IdKategoriJasa AND sl.Sesi = tpj.Sesi
            LEFT JOIN PEKERJA pj ON tpj.IdPekerja = pj.Id
            LEFT JOIN PENGGUNA pengguna ON pj.Id = pengguna.Id
            WHERE sl.SubkategoriId = %s
        """, [subcategory_id])
        sessions = cursor.fetchall()

        # Ambil testimoni terkait subkategori
        cursor.execute("""
            SELECT 
                t.Tgl, 
                t.Teks, 
                t.Rating, 
                pelanggan.Nama AS NamaPelanggan,
                pengguna.Nama AS NamaPekerja
            FROM TESTIMONI t
            JOIN TR_PEMESANAN_JASA tpj ON t.IdTrPemesanan = tpj.Id
            JOIN PELANGGAN pl ON tpj.IdPelanggan = pl.Id
            JOIN PENGGUNA pelanggan ON pl.Id = pelanggan.Id
            LEFT JOIN PEKERJA pekerja ON tpj.IdPekerja = pekerja.Id
            LEFT JOIN PENGGUNA pengguna ON pekerja.Id = pengguna.Id
            WHERE tpj.IdKategoriJasa = %s
        """, [subcategory_id])
        testimonials = cursor.fetchall()

    # Format data untuk rendering
    subcategory_data = {
        'id': subcategory[0],
        'name': subcategory[1],
        'description': subcategory[2],
        'category': subcategory[3],
        'sessions': [
            {
                'name': f"Sesi Layanan {row[0]}",
                'price': f"Rp {row[1]:,.0f}".replace(',', '.'),
                'worker_name': row[2] or ''
            }
            for row in sessions
        ],
        'testimonials': [
            {
                'date': testimonial[0],
                'text': testimonial[1],
                'rating': testimonial[2],
                'customer_name': testimonial[3],
                'worker_name': testimonial[4] or ''
            }
            for testimonial in testimonials
        ]
    }

    return render(request, 'subkategori.html', {'subcategory': subcategory_data})

@csrf_exempt
def buat_pemesanan(request, subkategori_id):
    if request.method == 'POST':
        # Ambil data dari form
        session_name = request.POST.get('session_name')
        discount_code = request.POST.get('discount_code', '').upper()
        payment_method = request.POST.get('payment_method')

        # Validasi data form
        if not session_name or not payment_method:
            return render(request, 'buat_pemesanan.html', {
                'error': 'Silakan lengkapi semua field yang diperlukan.',
                'subcategory_id': subkategori_id
            })

        # Hubungkan ke database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Ambil harga sesi
            cursor.execute(""" 
                SELECT Harga FROM SESI_LAYANAN 
                WHERE SubkategoriId = %s AND Sesi = %s
            """, [subkategori_id, session_name])
            session_data = cursor.fetchone()

            if not session_data:
                return render(request, 'buat_pemesanan.html', {
                    'error': 'Sesi tidak valid.',
                    'subcategory_id': subkategori_id
                })

            price = session_data[0]

            # Ambil potongan harga dari diskon
            discount_percentage = 0
            if discount_code:
                cursor.execute("""
                    SELECT Potongan FROM DISKON WHERE Kode = %s
                """, [discount_code])
                discount_data = cursor.fetchone()
                if discount_data:
                    discount_percentage = discount_data[0]
                    
                

            # Hitung total pembayaran
            total_payment = price * (1 - discount_percentage / 100)

            # Simpan data pesanan baru
            try:
                order_id = str(uuid.uuid4())  # Generate UUID di Python
                cursor.execute("""
                    INSERT INTO TR_PEMESANAN_JASA 
                    (Id, TglPemesanan, TglPekerjaan, WaktuPekerjaan, TotalBiaya,
                     IdPelanggan, IdPekerja, IdKategoriJasa, Sesi, IdDiskon, IdMetodeBayar)
                    VALUES (%s, CURRENT_DATE, CURRENT_DATE, CURRENT_TIMESTAMP, %s,
                            %s, NULL, %s, %s, %s, %s)
                """, [
                    order_id, total_payment, request.user.id, 
                    subkategori_id, session_name, 
                    discount_code or None, payment_method
                ])
                connection.commit()
                cursor.close()
                connection.close()
                return redirect('daftar_pesanan')

            except Exception as e:
                connection.rollback()
                return render(request, 'buat_pemesanan.html', {
                    'error': f'Terjadi kesalahan saat membuat pesanan: {e}',
                    'subcategory_id': subkategori_id
                })


    # Ambil data sesi dan metode pembayaran untuk rendering form
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Sesi, Harga FROM SESI_LAYANAN WHERE SubkategoriId = %s
        """, [subkategori_id])
        sessions = cursor.fetchall()

        cursor.execute("""
            SELECT Nama, Id FROM METODE_BAYAR
        """)
        payment_methods = cursor.fetchall()

        cursor.execute("""
            SELECT Kode, Potongan FROM DISKON
        """)
        discounts = cursor.fetchall()

    return render(request, 'buat_pemesanan.html', {
        'subcategory_id': subkategori_id,
        'sessions': [{'Sesi': s[0], 'Harga': f"Rp {s[1]:,.0f}".replace(',', '.')} for s in sessions],
        'payment_methods': [{'Nama': m[0], 'Id': m[1]} for m in payment_methods],
        'discounts': [{'Kode': d[0], 'Potongan': d[1]} for d in discounts],
    })

def daftar_pesanan(request):
    subcategory_filter = request.GET.get('subcategory', '')
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '').lower()

    query = """
        SELECT 
            tpj.Id AS IdPesanan, 
            sj.NamaSubkategori AS Subkategori,
            tpj.Sesi AS Sesi,
            tpj.TotalBiaya AS Harga,
            p.Nama AS NamaPekerja,
            sp.Status AS Status
        FROM TR_PEMESANAN_JASA tpj
        INNER JOIN SUBKATEGORI_JASA sj ON tpj.IdKategoriJasa = sj.Id
        LEFT JOIN PEKERJA pj ON tpj.IdPekerja = pj.Id
        LEFT JOIN PENGGUNA p ON p.Id = pj.Id
        LEFT JOIN TR_PEMESANAN_STATUS tps ON tpj.Id = tps.IdTrPemesanan
        LEFT JOIN STATUS_PESANAN sp ON tps.IdStatus = sp.Id
        WHERE 1=1
    """
    params = []

    # Tambahkan filter subkategori
    if subcategory_filter:
        query += " AND sj.NamaSubkategori = %s"
        params.append(subcategory_filter)

    # Tambahkan filter status
    if status_filter:
        query += " AND sp.Status = %s"
        params.append(status_filter)

    # Tambahkan filter pencarian
    if search_query:
        query += " AND (LOWER(pj.Nama) LIKE %s OR LOWER(sj.NamaSubkategori) LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    query += " ORDER BY tpj.TglPemesanan DESC"

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        orders = cursor.fetchall()

    # Format hasil query
    formatted_orders = [
        {
            'id': row[0],
            'subcategory': row[1],
            'session_name': f"Sesi Layanan {row[2]}",
            'price': f"Rp {row[3]:,.0f}".replace(',', '.'),
            'worker_name': row[4] or '-',
            'status': row[5] or 'Belum Diketahui',
        }
        for row in orders
    ]

    return render(request, 'daftar_pesanan.html', {'orders': formatted_orders})