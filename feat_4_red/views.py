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
    user_type = 'Pekerja'  # Ubah menjadi 'Pekerja' sesuai kebutuhan
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
