from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)
    url_photo = models.CharField(max_length=15)
    address = models.TextField()
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    date = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class JobCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nama kategori pekerjaan
    description = models.TextField(blank=True, null=True)  # Deskripsi opsional

    def __str__(self):
        return self.name

class SubJobCategory(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Service(models.Model):
    sub_category = models.ForeignKey(SubJobCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 


    def __str__(self):
        return f"{self.name} ({self.sub_category.name})"

class Testimonial(models.Model):
    user = models.ForeignKey(User, related_name='testimonials', on_delete=models.CASCADE)  # Link to the User model
    service = models.ForeignKey(Service, related_name='testimonials', on_delete=models.CASCADE)  # Link to SubJobCategory
    text = models.TextField()  # Field to store the testimonial text
    rating = models.PositiveIntegerField()  # Field to store the rating (1-5, for example)

    def __str__(self):
        return f'Testimonial by {self.user.name} for {self.service.name}'

class Worker(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    phone = models.CharField(max_length=15, unique=True)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    npwp = models.CharField(max_length=20)
    photo_url = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) 
    sub_categories = models.ManyToManyField(SubJobCategory, related_name='workers')  # Relasi ke SubJobCategory


    @classmethod
    def worker_exists(cls, phone, npwp):
        return cls.objects.filter(phone=phone).exists() or cls.objects.filter(npwp=npwp).exists()


class Transaction(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", verbose_name="User", null=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="transactions", verbose_name="Worker", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Transaction Time")
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=[
        ("in", "UANG MASUK"),
        ("out", "UANG KELUAR"),
    ], default='in', verbose_name="Type Transaction")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Transaction Amount")

class Discount(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Promo Code")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Discount Percentage")
    min_transaction = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Minimum Transaction")
    max_usage = models.PositiveIntegerField(verbose_name="Max Usage")
    usage_quota = models.PositiveIntegerField(default=0, verbose_name="Usage Quota")  # Track usage count
    voucher_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Voucher Price")
    expired_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return f"{self.code} - {self.percentage}% off"

class Order(models.Model):
    STATUS_CHOICES = [
        ('AWAITING_PAYMENT', 'Menunggu Pembayaran'),
        ('SEARCHING_WORKER', 'Mencari Pekerja Terdekat'),
        ('WORKER_FOUND', 'Mendapatkan Pekerja'),
        ('WAITING_WORKER', 'Menunggu Pekerja Tiba'),
        ('ARRIVE_WORKER', 'Pekerja Tiba'),
        ('IN_PROGRESS', 'Dikerjakan'),
        ('COMPLETED', 'Selesai'),
        ('CANCELED', 'Dibatalkan'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Pemesan",
        related_name="orders",
        null=True,  # Menandakan kolom ini bisa null
        blank=True,  # Menandakan kolom ini bisa kosong di form
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service", related_name="orders")
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Worker", related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AWAITING_PAYMENT', verbose_name="Order Status")
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Discount", related_name="orders")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Price")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def calculate_price(self):
        """
        Recalculate the total price after applying discount if applicable.
        """
        base_price = self.service.amount
        discount_amount = 0

        if self.discount and self.discount.min_transaction <= base_price and self.discount.usage_quota < self.discount.max_usage:
            discount_amount = (base_price * self.discount.percentage / 100)
            # Update usage quota
            self.discount.usage_quota += 1
            self.discount.save()

        return base_price - discount_amount

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.calculate_price()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.service.name} ({self.get_status_display()})"

class PurchasedVoucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pembeli", related_name="vouchers")
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name="Diskon", related_name="purchased_vouchers")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Pembelian")
    is_used = models.BooleanField(default=False, verbose_name="Telah Digunakan")
    
    def __str__(self):
        return f"{self.user.username} - {self.discount.code} - {'Digunakan' if self.is_used else 'Belum Digunakan'}"
        