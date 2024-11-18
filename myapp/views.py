from django.shortcuts import render, redirect
from .database import add_user, add_worker, user_exists, worker_exists, users_db, workers_db
from .forms import UserRegistrationForm, WorkerRegistrationForm

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
                add_user(name, password, gender, phone, dob_date, address)
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
            
            try:
                add_worker(name, password, gender, phone, dob, address, bank_name, account_number, npwp, photo_url)
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
                return render(request, 'register_worker.html', {'form': form})
    else:
        form = WorkerRegistrationForm()
    
    return render(request, 'register_worker.html', {'form': form})

def login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if phone in users_db and users_db[phone]['password'] == password:
            request.session['user_phone'] = phone
            return redirect('home_user')  

        elif phone in workers_db and workers_db[phone]['password'] == password:
            request.session['user_phone'] = phone
            return redirect('home_worker')

        else:
            return render(request, 'login.html', {'error': '*No HP atau password salah.'})

    return render(request, 'login.html')

def home(request):
    """Menampilkan halaman utama setelah login berhasil."""
    if 'user_phone' not in request.session:
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
    """Menampilkan halaman untuk pekerja."""
    if 'user_phone' not in request.session:
        return redirect('login') 

    phone = request.session['user_phone']
    if worker_exists(phone):  
        return render(request, 'home_worker.html', {'user': workers_db[phone]})  
    return redirect('home_user')

def home_user(request):
    """Menampilkan halaman untuk pengguna."""
    if 'user_phone' not in request.session:
        return redirect('login')  

    phone = request.session['user_phone']
    if user_exists(phone):
        return render(request, 'home_user.html', {'user': users_db[phone]})
    return redirect('home_worker')