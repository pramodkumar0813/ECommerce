from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # 👈 AbstractUser ను AbstractBaseUser & BaseUserManager గా మార్చాం
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_profile_complete', True) # Admin True
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)

# 2. User model calss (AbstractBaseUser)
class User(AbstractBaseUser, PermissionsMixin):
    #  In AbstractUser default fields again defien
    
    # Required for Mobile OTP Login
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True) 

    # Full Name Fields ( from AbstractUser we can define again)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    
    # Address Fields
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # Status/Permissions Fields (is_staff/is_superuser  not in AbstractBaseUser , it comes from PermissionsMixin)
    is_profile_complete = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)  # Required by your old migrations/DB
    last_login = models.DateTimeField(null=True, blank=True) # Required by AbstractBaseUser for functionality
    
    # custom filed settings
    USERNAME_FIELD = 'phone' 
    REQUIRED_FIELDS = []
    
    # here we can set manager 
    objects = UserManager()

    def __str__(self):
        return self.phone

# --- 3. Category Model ---
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# --- 4. Product Model (Category added) ---
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# --- 5. Cart, CartItem Models ---
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Cart of {self.user.phone}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"