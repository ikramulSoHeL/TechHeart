from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):

        if not email:
            raise ValueError('Must have an email address')

        if not name:
            raise ValueError('Must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Email & Password are required by default.

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
       return self.user.name


class Category(models.Model):
    category_name=models.CharField(max_length=255)
    category_id = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    desc =models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()

        return shipping

    @property
    def get_cart_total(self):
        orderitems =self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total








class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Delivery(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=15)
    trxId = models.CharField(max_length=15)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Blog(models.Model):
    title = models.CharField(max_length=500, null=True)
    desc = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    publish_date = models.DateTimeField()
    slug = models.SlugField(max_length=500)

    def __str__(self):
        return self.title





















































