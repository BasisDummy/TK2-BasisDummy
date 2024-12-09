from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .database import add_user, add_worker, user_exists, worker_exists, users_db, workers_db
from .forms import UserRegistrationForm, WorkerRegistrationForm
from .models import User, Worker, JobCategory, SubJobCategory, Transaction, Service, Discount, Order, PurchasedVoucher, Testimonial
from datetime import datetime, date
from django.contrib import messages
from django.http import JsonResponse

def choose_role(request):
    return render(request, 'choose_role.html')

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
import datetime

def register_user(request):
    """Menangani pendaftaran pengguna baru."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            dob = request.POST.get('dob')
            address = form.cleaned_data['address']

            dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()

            try:
                # Simpan ke database
                user_profile = User(
                    name=name,
                    password=password,
                    gender=gender,
                    phone=phone,
                    date=dob_date,
                    address=address
                )
                user_profile.save() 
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, 'register_user.html', {'form': form})
    else:
        form = UserRegistrationForm()

    return render(request, 'register_user.html', {'form': form})

def register_worker(request):
    """Menangani pendaftaran pekerja baru."""
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            address = form.cleaned_data['address']
            account_number = form.cleaned_data['account_number']
            npwp = form.cleaned_data['npwp']
            photo_url = form.cleaned_data['photo_url']
            bank_name = form.cleaned_data['bank_name']

            # Validasi nomor HP sudah ada
            if Worker.objects.filter(phone=phone).exists():
                form.add_error('phone', 'Nomor HP sudah digunakan.')
                return render(request, 'register_worker.html', {'form': form})

            # Validasi kombinasi nama bank dan nomor rekening tidak duplikat
            if Worker.objects.filter(bank_name=bank_name, account_number=account_number).exists():
                form.add_error('account_number', 'Nomor rekening sudah digunakan untuk bank yang sama.')
                return render(request, 'register_worker.html', {'form': form})

            # Validasi nomor NPWP tidak duplikat
            if Worker.objects.filter(npwp=npwp).exists():
                form.add_error('npwp', 'Nomor NPWP sudah digunakan.')
                return render(request, 'register_worker.html', {'form': form})
            
            try:
                Worker.objects.create(
                    name=name,
                    password=password,
                    gender=gender,
                    phone=phone,
                    dob=dob,
                    address=address,
                    account_number=account_number,
                    npwp=npwp,
                    photo_url=photo_url,
                    bank_name=bank_name
                )
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, 'register_worker.html', {'form': form})
    else:
        form = WorkerRegistrationForm()
    
    return render(request, 'register_worker.html', {'form': form})

def profile(request):
    if "user_phone" in request.session:
        user = User.objects.get(phone=request.session["user_phone"])
        return render(request, "profile.html", {
            "role": "user",
            "user": user
        })
    if "worker_phone" in request.session:
        worker = Worker.objects.get(phone=request.session["worker_phone"])

        order = Order.objects.filter(status="COMPLETED")
        order = order.filter(worker=worker)
        
        categories = worker.sub_categories.all()

        jumlah = 0
        for o in order:
            testi = Testimonial.objects.get(service=o.service)
            jumlah += testi.rating

    
        return render(request, "profile.html", {
            "role": "worker",
            "worker": worker,
            "order_done": len(order),
            "categories": categories,
            "rating": jumlah if jumlah == 0 else jumlah / len(order) 
        })
    return redirect('login')

def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = None
        error_message = "Invalid username or password"
      # Periksa di tabel User
        try:
            user = User.objects.get(phone=phone)
            # print(user)
            if password == user.password:
                # Simpan data User ke session
                request.session['user_id'] = user.id
                request.session['user_phone'] = user.phone
                request.session['role'] = 'User'  # Tandai role sebagai User
                return redirect('home_user')  # Ganti 'home' dengan URL tujuan
        except User.DoesNotExist:
            pass  # Lanjut ke tabel Worker

          # Periksa di tabel Worker
        try:
            worker = Worker.objects.get(phone=phone)
            if password == worker.password:
                # Simpan data Worker ke session
                request.session['worker_id'] = worker.id
                request.session['worker_phone'] = worker.phone
                request.session['role'] = 'Worker'  # Tandai role sebagai Worker
                print(worker.password == password)
                return redirect('home_worker')  # Ganti 'dashboard' dengan URL tujuan
        except Worker.DoesNotExist:
            pass

        # Jika tidak ditemukan di kedua tabel
        return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

def home(request):
    """Menampilkan halaman utama setelah login berhasil."""
    if 'user_phone' not in request.session:
        print(request.session)
        return
        return redirect('login') 
    
    phone = request.session['user_phone']
    if user_exists(phone):
        return render(request, 'home.html', {'user': users_db[phone]}) 
    return redirect('login')

def logout(request):
    """Menangani proses logout."""
    request.session.flush()  
    return redirect('login')

def landing(request):
    return render(request, 'landing.html')

def home_worker(request):
    # print(request.session['worker_phone'])
    """Menampilkan halaman untuk pekerja."""
    if 'worker_phone' not in request.session:
        return redirect('login') 

    phone = request.session['worker_phone']
    if Worker.objects.filter(phone=phone).exists():  
        worker = Worker.objects.get(phone=phone)
                # Retrieve categories, subcategories, and services
        categories = JobCategory.objects.all()

        return render(request, 'home_worker.html', {'user': worker , 'categories': categories})  
    return redirect('home_user')

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

def subkategori(request, subcategory_id):
    # Gunakan subcategory_id langsung dari parameter
    subkategori_id = subcategory_id

    
    # Pastikan ID subkategori ada di data
    try:
        subkategori = SubJobCategory.objects.get(id=subcategory_id)
        services = subkategori.services.all()

        # testimonials = subkategori.services.testimonial.all()
        testimonials = None
        workers = subkategori.workers.all()
        service_ids = [service.id for service in services]
        testimonials = Testimonial.objects.filter(service__in=services)
        is_join = False
        if "worker_phone" in request.session:
            is_join = Worker.objects.get(phone=request.session["worker_phone"]).sub_categories.filter(id=subkategori.id).exists()
        # print(is_join)
        return render(request, 'sub_category.html', {'subcategory': subkategori, 'services': services, 'testimonials': testimonials, 'workers': workers, "role": request.session['role'], "is_join": is_join})
    except SubJobCategory.DoesNotExist:
        return render(request, '404.html', {'message': 'ID Subkategori tidak ditemukan atau tidak valid.'}, status=404)

def home_user(request):
  
    """Menampilkan halaman untuk pengguna."""
    if 'user_phone' not in request.session:
        return redirect('login')  

    phone = request.session['user_phone']
    if User.objects.filter(phone=phone).exists():
        user = User.objects.get(phone=phone)
        categories = JobCategory.objects.all()

        return render(request, 'home_user.html', {'user': user , 'categories': categories}) 
    return redirect('home_worker')


def daftar_diskon(request):
    vouchers = Discount.objects.filter(voucher_price__gt=0)
    promos = Discount.objects.filter(voucher_price=0)
    print(promos)
    return render(request, 'user/daftar_diskon.html', {'vouchers': vouchers, 'promos': promos})

def my_pay(request):
    phone = None
    if 'user_phone' in request.session:
        pengguna = None
        phone = request.session['user_phone']
        if User.objects.filter(phone=phone).exists():
            pengguna = User.objects.get(phone=phone)
        transactions = pengguna.transactions.all()
        role = request.session['role']
        print(role)
        return render(request, 'user/mypay.html', {"pengguna": pengguna, "transactions": transactions, 'role': role})
    elif 'worker_phone' in request.session:
        phone = request.session['worker_phone']
        if Worker.objects.filter(phone=phone).exists():
            pengguna = Worker.objects.get(phone=phone)
        transactions = pengguna.transactions.all()
        role = request.session['role']
        print(role)
        return render(request, 'user/mypay.html', {"pengguna": pengguna, "transactions": transactions, 'role': role})
    else:
        redirect('login')

def transaksi_mypay_view(request):
    # Ambil user_type dari sesi
    user_type = request.session.get('role', 'User')  # Default ke 'Pengguna' jika tidak diatur

    user = None
    orders = None
    print(orders)
    if 'user_phone' in request.session:
        try:
            user_order = User.objects.get(phone=request.session['user_phone'])
        except User.DoesNotExist:
            return render(request, 'error.html', {'message': 'User not found'})

        # Ambil semua order yang statusnya "Menunggu Pembayaran"
        orders = Order.objects.filter(user=user_order, status="AWAITING_PAYMENT")

    auth_role = "user"
    if 'user_phone' in request.session:
        user = User.objects.get(phone=request.session['user_phone'])
    elif 'worker_phone' in request.session:
        auth_role = "worker"
        user = Worker.objects.get(phone=request.session['worker_phone'])

    if user == None:
        return redirect('login')
    if request.method == 'POST':
        # print(kategori)
        kategori = request.POST.get('kategori_transaksi')
        tanggal_transaksi = datetime.datetime.now().strftime('%Y-%m-%d')        
        saldo_user = user.saldo
        if kategori == 'TOP UP MY PAY':
            nominal = int(request.POST.get('nominal', 0))
            if nominal > 0:
                # request.session['saldo'] += nominal
                print(user)
                user.saldo += nominal
                user.save()

                if request.session['role'] == 'User':
                    # Buat instance transaksi
                    transaction = Transaction(
                        user=user,
                        category="TOPUP",
                        amount=nominal,
                        type="in"
                    )
                else:
                    # Buat instance transaksi
                    transaction = Transaction(
                        worker=user,
                        category="TOPUP",
                        amount=nominal,
                        type="in"
                    )

                # Simpan transaksi ke database
                transaction.save()
                messages.success(request, 'Top Up Berhasil!')

            else:
                messages.error(request, 'Nominal tidak valid.')

        elif kategori == 'MEMBAYAR TRANSAKSI':
            if user_type == 'User':
                pesanan_jasa = request.POST.get('pesanan_jasa')
                # Ekstrak jumlah dari pesanan_jasa (misalnya, "Jasa 1 - Rp 200.000")

                try:
                  
                    order = Order.objects.get(id=pesanan_jasa)
                    print(order.total_price)
                    if user.saldo >= order.total_price:
                        order.status = 'SEARCHING_WORKER'
                        user.saldo -= order.total_price
                         # Buat instance transaksi
                        transaction = Transaction(
                            user=user,
                            category="MEMBAYAR TRANSAKSI",
                            amount=order.total_price,
                            type="out"
                        )


                        # Simpan transaksi ke database
                        user.save()
                        order.save()
                        transaction.save()
                        print("success")
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
            is_worker = False
            is_tujuan = False
     
            if Worker.objects.filter(phone=no_hp_tujuan).exists():
                is_worker = True
                is_tujuan = True
            elif User.objects.filter(phone=no_hp_tujuan):        
                is_worker = False
                is_tujuan = True

      
            if is_tujuan:
                if nominal_transfer > 0 and user.saldo >= nominal_transfer:
                    if is_worker:
                        worker = Worker.objects.get(phone=no_hp_tujuan)
                        worker.saldo += nominal_transfer
                        worker.save()
                    else:
                        worker = User.objects.get(phone=no_hp_tujuan)
                        # print(worker)
                        worker.saldo += nominal_transfer
                        worker.save()
                        
                    user.saldo -= nominal_transfer
                    user.save()
                
                    if is_worker and auth_role == "worker":
                        # Buat instance transaksi
                        transaction = Transaction(
                            worker=worker,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="in"
                        )
                        transaction.save()

                        transaction = Transaction(
                            worker=user,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="out"
                        )
                        transaction.save()
                    elif is_worker and auth_role == "user":
                     
                        transaction = Transaction(
                            user=user,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="out"
                        )
                        transaction.save()
                        transaction = Transaction(
                            worker=worker,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="in"
                        )
                        transaction.save()
                    elif not is_worker and auth_role == "worker":
                        transaction = Transaction(
                            user=worker,
                            type="in",
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                        )

                        transaction.save()
                        transaction = Transaction(
                            type="out",
                            worker=user,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                        )
                        transaction.save()
                    elif not is_worker and auth_role == "user":
                        transaction = Transaction(
                            user=user,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="out"
                        )
                        transaction.save()
                        transaction = Transaction(
                            user=worker,
                            category="TRANSFER MYPAY",
                            amount=nominal_transfer,
                            type="in"
                        )
                        transaction.save()
                    # Simpan transaksi ke database
                    messages.success(request, 'Transfer Berhasil!')
                else:
                    messages.error(request, 'Jumlah transfer tidak valid atau saldo tidak mencukupi.')
            else:
                messages.error(request, 'Nomor pekerja tidak ada.')

        elif kategori == 'WITHDRAWAL':
           
            nama_bank = request.POST.get('nama_bank')
            no_rekening = request.POST.get('no_rekening')
            nominal_withdrawal = int(request.POST.get('nominal_withdrawal', 0))
            if nominal_withdrawal > 0 and user.saldo >= nominal_withdrawal:
                user.saldo -= nominal_withdrawal
                user.save()


                if request.session['role'] == 'User':
                    # Buat instance transaksi
                    transaction = Transaction(
                        user=user,
                        category="WITHDRAWAL",
                        amount=nominal_withdrawal,
                        type="out"
                    )
                else:
                    # Buat instance transaksi
                    transaction = Transaction(
                        worker=user,
                        category="WITHDRAWAL",
                        amount=nominal_withdrawal,
                        type="out"
                    )

                # Simpan transaksi ke database
                transaction.save()
                messages.success(request, 'Withdrawal Berhasil!')

            else:
                messages.error(request, 'Jumlah withdrawal tidak valid atau saldo tidak mencukupi.')

        else:
            messages.error(request, 'Kategori transaksi tidak valid.')

        return redirect('/myapp/home/transaksi-user-mypay')

    # Data dummy untuk form
    pengguna = user

 
    
    dummy_form = {
        'nama_user': pengguna.name,
        'tanggal_transaksi': datetime.datetime.now().strftime('%Y-%m-%d'),
        'saldo_user': f"Rp {pengguna.saldo:,}".replace(',', '.'),
    }

    # Tentukan kategori transaksi dan pilih template berdasarkan user_type
    if user_type == 'User':
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'MEMBAYAR TRANSAKSI', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'user/transaksi.html'
    else:  # Pekerja
        dummy_form['kategori_transaksi'] = ['TOP UP MY PAY', 'TRANSFER MYPAY', 'WITHDRAWAL']
        template_name = 'user/transaksi.html'
    print("succcess")
    return render(request, template_name, {'form': dummy_form, 'user_type': user_type, 'orders': orders})


def get_user_pending_orders(request):
    try:
        user = User.objects.get(phone=request.session['user_phone'])
        orders = Order.objects.filter(user=user, status="AWAITING_PAYMENT")
        
        # Buat response berupa JSON
        orders_data = [
            {
                'id': order.id,
                'service': order.service.name,
                'status': order.status,
                'total_price': order.total_price,
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for order in orders
        ]
        
        return JsonResponse({'orders': orders_data})
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def kelola_pesanan(request):
        
    try:
        user = User.objects.get(phone=request.session['user_phone'])
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found'})

    # Ambil semua order yang terkait dengan pengguna
    orders = Order.objects.filter(user=user)
    subkategori = SubJobCategory.objects.all()
    return render(request, 'user/kelola_pesanan.html', { 'orders': orders, "subkategori": subkategori})

def view_pemesanan(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'POST':
        service_id = request.POST.get("id")
        tanggal = request.POST.get("tanggal")
        amount = request.POST.get("amount")
        diskon = request.POST.get("diskon")

        try:
            user = User.objects.get(phone=request.session['user_phone'])
            service = Service.objects.get(id=service_id)

        except (User.DoesNotExist, Service.DoesNotExist) as e:
            return render(request, "error.html", {"message": str(e)})

        discount = None
        try:
            discount = Discount.objects.get(code=diskon)
        except (Discount.DoesNotExist) as e:
            pass
        
        if discount != None:
            print(discount.usage_quota)
            if discount.usage_quota == discount.max_usage:
                messages.error(request, 'Diskon melewati batas penggunaan')
                return redirect(request.META.get('HTTP_REFERER', 'default_url'))
                
            discount.usage_quota += 1
            discount.save()
            order = Order(
                user=user,
                service=service,
                status="AWAITING_PAYMENT",
                discount=discount,
            )
        else:
            order = Order(
                user=user,
                service=service,
                status="AWAITING_PAYMENT",
            )

        order.total_price = amount

        # Simpan data ke database
        order.save()
        return redirect('kelola_pesanan')
    return render(request, 'user/pemesanan.html', { 'service': service })

def beli_diskon(request, diskon_id):
    diskon = Discount.objects.get(id=diskon_id)
    user = User.objects.get(phone=request.session['user_phone'])

    if user.saldo < diskon.voucher_price:
        return JsonResponse(
            {
                "message": "Saldo anda tidak mencukupi"
            }
        )
    user.saldo -= diskon.voucher_price
    user.save()

            # Pastikan diskon belum expired
    if diskon.expired_date and diskon.expired_date < date.today():
        return JsonResponse({"message": "Diskon telah kedaluwarsa"}, status=status.HTTP_400_BAD_REQUEST)
    
    if PurchasedVoucher.objects.filter(user=user, discount=diskon).exists():
        return JsonResponse(
            {"message": "Voucher ini sudah pernah dibeli oleh Anda"},
        )

    purchased_voucher = PurchasedVoucher.objects.create(user=user, discount=diskon)
        
 
    print(diskon.voucher_price)
    return JsonResponse({
                "status": "success",
                "message": f"Selamat! Anda berhasil membeli voucher kode {diskon.code}.",
                "new_saldo": user.saldo,
                "code": diskon.code,
                "expiry_date": diskon.expired_date,
                "quota": diskon.usage_quota
            })

def kelola_pekerjaan_worker(request):
    if 'worker_phone' not in request.session:
        return redirect('login')
    
    categories = JobCategory.objects.all()
    orders = Order.objects.filter(status="SEARCHING_WORKER")
    return render(request, 'worker/kelola_pekerjaan.html', {'categories': categories, "orders": orders})

def get_subkategori(request, kategori_id):
    if 'worker_phone' not in request.session:
        return redirect('login')
    sub_job_kategoris = SubJobCategory.objects.filter(category_id=kategori_id).values('id', 'name')
    return JsonResponse(list(sub_job_kategoris), safe=False)

def kerjakan_service(request, order_id):
    if 'worker_phone' not in request.session:
        return redirect('login')
    
    worker = Worker.objects.get(phone=request.session['worker_phone'])
    order = Order.objects.get(id=order_id)
    order.worker = worker
    order.status = "WAITING_WORKER"
    order.save()

    return redirect('kelola_status_pekerjaan')

def batal_pesanan(request, order_id):
    order = Order.objects.get(id=order_id)    
    if order.status != "AWAITING_PAYMENT":
        user = User.objects.get(phone=request.session['user_phone'])
        user.saldo += order.total_price
        user.save()
        transaction = Transaction(
            user=user,
            category="REFUND CANCEL",
            amount= order.total_price,
            type="in"
        )
        transaction.save()
    order.status = "CANCELED"
    order.save()
    return redirect('kelola_pesanan')

def update_service(request, order_id):
    order = Order.objects.get(id=order_id)  
    print(order.status)  
    if order.status == "WAITING_WORKER":
        order.status = "ARRIVE_WORKER"
    elif order.status == "ARRIVE_WORKER":
        order.status = "IN_PROGRESS"
    elif order.status == "IN_PROGRESS":
        order.status = "COMPLETED"
        worker = Worker.objects.get(id=order.worker.id)
        worker.saldo += order.total_price
        worker.save()
        transaction = Transaction(
            worker=worker,
            category="PEMBAYARAN JASA",
            amount= order.total_price,
            type="in"
        )
        transaction.save()
        print("selesai", order.worker.id)
    order.save()
    return redirect('kelola_status_pekerjaan')

def join_service(request, sub_category_id):
    if "worker_phone" not in request.session:
        return redirect("login")
    worker = Worker.objects.get(phone=request.session["worker_phone"])
        # Ambil objek subkategori berdasarkan ID yang diterima
    subcategories = SubJobCategory.objects.filter(id__in=sub_category_id)
    
    # Gabungkan pekerja dengan subkategori yang dipilih
    worker.sub_categories.add(*subcategories)

    return redirect(request.META.get('HTTP_REFERER', 'default_url'))

def buat_testimoni(request, order_id):
    if "user_phone" not in request.session:
        return redirect('login')

    if request.method == "POST":
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        user = User.objects.get(phone=request.session['user_phone'])
        order = Service.objects.get(id=order_id)
        testi = Testimonial.objects.create(
            user=user,
            service=order,
            rating=rating,
            text=text
        )
        return redirect('kelola_pesanan')
    return render(request, 'user/buat_testimoni.html', { "order_id": order_id, "range": range(1, 6) })

def kelola_status_pekerjaan(request):
    if 'worker_phone' not in request.session:
        return redirect('login')
    categories = JobCategory.objects.all()
    worker = Worker.objects.get(phone=request.session['worker_phone'])
    orders = Order.objects.filter(worker=worker)
        
    return render(request, 'worker/kelola_status_pekerjaan.html', {"orders": orders})

def profile_worker(request):
    if 'worker_phone' not in request.session:
        return redirect('login')
    return render(request, 'worker/profile.html')

def update_profile(request):
    role = None
    if "user_phone" in request.session:
        role = "user"
        try:
            user = User.objects.get(phone=request.session['user_phone'])
        except User.DoesNotExist:
            return redirect("login")

        
        if request.method == "POST":
            
            # Mengambil data dari form input
            user.name = request.POST.get('name')
            user.gender = request.POST.get('gender')
            user.phone = request.POST.get('phone')
            user.address = request.POST.get('address')
            user.date = request.POST.get('date')

            user.save()  # Menyimpan data ke database

            messages.success(request, "Profile berhasil diperbarui!")
            return redirect("profile")

        return render(request, "update_profile.html", {"role": role, "user": user})
    elif "worker_phone" in request.session:
        role = "worker"
        try:
            worker = Worker.objects.get(phone=request.session['worker_phone'])
        except Worker.DoesNotExist:
            return redirect("login")

        if request.method == "POST":
            worker.name = request.POST.get('name')
            worker.gender = request.POST.get('gender')
            worker.phone = request.POST.get('phone')
            worker.address = request.POST.get('address')
            worker.bank_name = request.POST.get('bank_name')
            worker.account_number = request.POST.get('account_number')
            worker.npwp = request.POST.get('npwp')
            worker.photo_url = request.POST.get('url_photo')
            worker.dob = request.POST.get('dob')

            worker.save()  # Menyimpan data ke database

            messages.success(request, "Profile pekerja berhasil diperbarui!")
            return redirect("profile")

        return render(request, "update_profile.html", {"role": role, "worker": worker})
    else:
        return redirect("login")
    
def get_voucher_and_promo(request):
    if "user_phone" not in request.session:
        return redirect("login")
    
    promo = Discount.objects.filter(voucher_price=0)
    vouchers = Discount.objects.filter(
        voucher_price__gt=0,
        purchased_vouchers__user=User.objects.get(phone=request.session["user_phone"])
    ).distinct()
    print(vouchers)
    promo_data = [
        {
            'id': p.id,
            'code': p.code,
            'percentage': p.percentage,
            'avaible': p.max_usage - p.usage_quota,
            'min_transaction': p.min_transaction
        }
        for p in promo
    ]
    
    voucher_data = [
        {
            'id': p.id,
            'code': p.code,
            'percentage': p.percentage,
            'avaible': p.max_usage - p.usage_quota,
            'min_transaction': p.min_transaction
        }
        for p in vouchers
    ]

    data = promo_data + voucher_data
    
    return JsonResponse({'discount': data}, status=200)