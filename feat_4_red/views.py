# feat_4_red/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

def mypay_view(request):
    # Inisialisasi data sesi jika belum ada
    if 'no_hp' not in request.session:
        request.session['no_hp'] = '081234567890'
    if 'saldo' not in request.session:
        request.session['saldo'] = 1500000  # Rp 1.500.000
    if 'transactions' not in request.session:
        request.session['transactions'] = [
            {'date': '2024-10-01', 'type': 'TOP UP MY PAY', 'amount': 500000},
            {'date': '2024-10-05', 'type': 'MEMBAYAR TRANSAKSI', 'amount': -200000},
            {'date': '2024-10-10', 'type': 'TRANSFER MYPAY', 'amount': -300000},
        ]

    # Simulasi tipe pengguna
    user_type = 'Pekerja'  # Ubah menjadi 'Pengguna' atau 'Pekerja' sesuai kebutuhan
    request.session['user_type'] = user_type  # Simpan di sesi

    # Siapkan data untuk template
    dummy_mypay = {
        'no_hp': request.session['no_hp'],
        'saldo': f"Rp {request.session['saldo']:,}".replace(',', '.'),
        'transactions': [
            {
                'date': t['date'],
                'type': t['type'],
                'amount': f"+ Rp {t['amount']:,}" if t['amount'] >= 0 else f"- Rp {-t['amount']:,}"
            }
            for t in request.session['transactions']
        ]
    }
    return render(request, 'feat_4_red/riwayat_transaksi.html', {'mypay': dummy_mypay, 'user_type': user_type})

def transaksi_mypay_view(request):
    # Ambil user_type dari sesi
    user_type = request.session.get('user_type', 'Pengguna')  # Default ke 'Pengguna' jika tidak diatur

    if request.method == 'POST':
        kategori = request.POST.get('kategori_transaksi')
        tanggal_transaksi = datetime.now().strftime('%Y-%m-%d')
        saldo_user = request.session.get('saldo', 0)

        if kategori == 'TOP UP MY PAY':
            nominal = int(request.POST.get('nominal', 0))
            if nominal > 0:
                request.session['saldo'] += nominal
                request.session['transactions'].append({
                    'date': tanggal_transaksi,
                    'type': 'TOP UP MY PAY',
                    'amount': nominal
                })
                messages.success(request, 'Top Up Berhasil!')
            else:
                messages.error(request, 'Nominal tidak valid.')

        elif kategori == 'MEMBAYAR TRANSAKSI':
            if user_type == 'Pengguna':
                pesanan_jasa = request.POST.get('pesanan_jasa')
                # Ekstrak jumlah dari pesanan_jasa (misalnya, "Jasa 1 - Rp 200.000")
                try:
                    amount_str = pesanan_jasa.split('- Rp ')[1].replace('.', '').replace(',', '')
                    amount = int(amount_str)
                    if saldo_user >= amount:
                        request.session['saldo'] -= amount
                        request.session['transactions'].append({
                            'date': tanggal_transaksi,
                            'type': 'MEMBAYAR TRANSAKSI',
                            'amount': -amount
                        })
                        messages.success(request, 'Pembayaran Berhasil!')
                    else:
                        messages.error(request, 'Saldo tidak mencukupi.')
                except (IndexError, ValueError):
                    messages.error(request, 'Pesanan jasa tidak valid.')
            else:
                messages.error(request, 'MEMBAYAR TRANSAKSI tidak tersedia untuk Pekerja.')

        elif kategori == 'TRANSFER MYPAY':
            no_hp_tujuan = request.POST.get('no_hp')
            nominal_transfer = int(request.POST.get('nominal_transfer', 0))
            if nominal_transfer > 0 and saldo_user >= nominal_transfer:
                request.session['saldo'] -= nominal_transfer
                request.session['transactions'].append({
                    'date': tanggal_transaksi,
                    'type': 'TRANSFER MYPAY',
                    'amount': -nominal_transfer
                })
                messages.success(request, 'Transfer Berhasil!')
            else:
                messages.error(request, 'Jumlah transfer tidak valid atau saldo tidak mencukupi.')

        elif kategori == 'WITHDRAWAL':
            nama_bank = request.POST.get('nama_bank')
            no_rekening = request.POST.get('no_rekening')
            nominal_withdrawal = int(request.POST.get('nominal_withdrawal', 0))
            if nominal_withdrawal > 0 and saldo_user >= nominal_withdrawal:
                request.session['saldo'] -= nominal_withdrawal
                request.session['transactions'].append({
                    'date': tanggal_transaksi,
                    'type': 'WITHDRAWAL',
                    'amount': -nominal_withdrawal
                })
                messages.success(request, 'Withdrawal Berhasil!')
            else:
                messages.error(request, 'Jumlah withdrawal tidak valid atau saldo tidak mencukupi.')

        else:
            messages.error(request, 'Kategori transaksi tidak valid.')

        return redirect('mypay_view')

    # Data dummy untuk form
    dummy_form = {
        'nama_user': 'Budi Santoso',
        'tanggal_transaksi': datetime.now().strftime('%Y-%m-%d'),
        'saldo_user': f"Rp {request.session.get('saldo', 0):,}".replace(',', '.'),
    }

    # Tentukan kategori transaksi dan pilih template berdasarkan user_type
    if user_type == 'Pengguna':
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'MEMBAYAR TRANSAKSI', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'feat_4_red/transaksi_mypay_pengguna.html'
    else:  # Pekerja
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'feat_4_red/transaksi_mypay_pekerja.html'

    return render(request, template_name, {'form': dummy_form, 'user_type': user_type})

def pekerjaan_jasa_view(request):
    # Inisialisasi data pesanan yang tersedia di sesi jika belum ada
    if 'available_jobs' not in request.session:
        request.session['available_jobs'] = [
            {
                'id': 1,
                'kategori': 'Home Cleaning',
                'subkategori': 'Setrika',
                'nama_pelanggan': 'Alice',
                'tanggal_pemesanan': '2024-11-01',
                'tanggal_pekerjaan': '2024-11-03',
                'total_biaya': 100000,
                'status': 'Mencari Pekerja Terdekat',
            },
            {
                'id': 2,
                'kategori': 'Massage',
                'subkategori': 'Full Body Massage',
                'nama_pelanggan': 'Bob',
                'tanggal_pemesanan': '2024-11-02',
                'tanggal_pekerjaan': '2024-11-04',
                'total_biaya': 150000,
                'status': 'Mencari Pekerja Terdekat',
            },
            # Tambahkan data dummy lainnya sesuai kebutuhan
        ]

    # Ambil data pesanan dari sesi
    available_jobs = request.session['available_jobs']

    # Opsi dropdown
    kategori_options = ['Home Cleaning', 'Massage', 'Babysitting']
    subkategori_options = ['Setrika', 'Daily Cleaning', 'Pembersihan Dapur', 'Full Body Massage', 'Foot Massage']

    # Ambil pilihan dari pengguna
    selected_kategori = request.GET.get('kategori', '')
    selected_subkategori = request.GET.get('subkategori', '')

    # Filter subkategori berdasarkan kategori yang dipilih
    if selected_kategori == 'Home Cleaning':
        subkategori_options = ['Setrika', 'Daily Cleaning', 'Pembersihan Dapur']
    elif selected_kategori == 'Massage':
        subkategori_options = ['Full Body Massage', 'Foot Massage']
    elif selected_kategori == 'Babysitting':
        subkategori_options = ['Infant Care', 'Toddler Care']

    # Filter pesanan berdasarkan kategori dan subkategori
    filtered_jobs = []
    for job in available_jobs:
        if selected_kategori and job['kategori'] != selected_kategori:
            continue
        if selected_subkategori and job['subkategori'] != selected_subkategori:
            continue
        if job['status'] == 'Mencari Pekerja Terdekat':
            filtered_jobs.append(job)

    context = {
        'kategori_options': kategori_options,
        'subkategori_options': subkategori_options,
        'selected_kategori': selected_kategori,
        'selected_subkategori': selected_subkategori,
        'jobs': filtered_jobs,
    }
    return render(request, 'feat_4_red/pekerjaan_jasa.html', context)

def accept_job_view(request):
    if request.method == 'POST':
        job_id = int(request.POST.get('job_id', -1))

        # Ambil data pesanan dari sesi
        available_jobs = request.session.get('available_jobs', [])

        # Cari pesanan berdasarkan job_id
        job = next((job for job in available_jobs if job['id'] == job_id), None)

        if job:
            if job['status'] != 'Mencari Pekerja Terdekat':
                messages.error(request, 'Pesanan tidak tersedia untuk diambil.')
            else:
                # Ubah status pesanan
                job['status'] = 'Menunggu Pekerja Berangkat'

                # Update available_jobs di sesi
                request.session['available_jobs'] = available_jobs

                # Tambahkan ke accepted_jobs di sesi
                if 'accepted_jobs' not in request.session:
                    request.session['accepted_jobs'] = []
                accepted_jobs = request.session['accepted_jobs']
                accepted_jobs.append(job)
                request.session['accepted_jobs'] = accepted_jobs

                messages.success(request, 'Pesanan telah diterima dan ditambahkan ke daftar pekerjaan Anda.')
        else:
            messages.error(request, 'Pesanan tidak ditemukan.')

        return redirect('pekerjaan_jasa')
    else:
        return redirect('pekerjaan_jasa')

def status_pekerjaan_jasa_view(request):
    accepted_jobs = request.session.get('accepted_jobs', [])

    # Ambil input filter
    nama_jasa = request.GET.get('nama_jasa', '')
    status_pesanan_filter = request.GET.get('status_pesanan', '')

    # Filter pekerjaan
    filtered_jobs = []
    for job in accepted_jobs:
        if nama_jasa and nama_jasa.lower() not in job['subkategori'].lower():
            continue
        if status_pesanan_filter and job['status'] != status_pesanan_filter:
            continue
        filtered_jobs.append(job)

    context = {
        'jobs': filtered_jobs,
        'nama_jasa': nama_jasa,
        'status_pesanan_filter': status_pesanan_filter,
        'status_options': [
            'Menunggu Pekerja Berangkat',
            'Pekerja Tiba Di Lokasi',
            'Pelayanan Jasa Sedang Dilakukan',
            'Pesanan Selesai',
        ],
    }
    return render(request, 'feat_4_red/status_pekerjaan_jasa.html', context)

def update_job_status_view(request):
    if request.method == 'POST':
        job_id = int(request.POST.get('job_id', -1))
        action = request.POST.get('action', '')
        accepted_jobs = request.session.get('accepted_jobs', [])

        # Cari indeks pekerjaan dalam accepted_jobs berdasarkan job_id
        job_index = next((index for (index, job) in enumerate(accepted_jobs) if job['id'] == job_id), None)

        if job_index is not None:
            job = accepted_jobs[job_index]

            if action == 'tiba' and job['status'] == 'Menunggu Pekerja Berangkat':
                job['status'] = 'Pekerja Tiba Di Lokasi'
                messages.success(request, 'Status diperbarui menjadi "Pekerja Tiba Di Lokasi".')
            elif action == 'mulai' and job['status'] == 'Pekerja Tiba Di Lokasi':
                job['status'] = 'Pelayanan Jasa Sedang Dilakukan'
                messages.success(request, 'Status diperbarui menjadi "Pelayanan Jasa Sedang Dilakukan".')
            elif action == 'selesai' and job['status'] == 'Pelayanan Jasa Sedang Dilakukan':
                job['status'] = 'Pesanan Selesai'
                messages.success(request, 'Status diperbarui menjadi "Pesanan Selesai".')
            else:
                messages.error(request, 'Aksi tidak valid untuk status saat ini.')

            # Perbarui pekerjaan di accepted_jobs
            accepted_jobs[job_index] = job
            request.session['accepted_jobs'] = accepted_jobs
        else:
            messages.error(request, 'Pekerjaan tidak ditemukan.')

        return redirect('status_pekerjaan_jasa')
    else:
        return redirect('status_pekerjaan_jasa')
