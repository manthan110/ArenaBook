from django.db import models
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class AppUser(models.Model):
    first_name = models.CharField(max_length=100) 
    last_name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=255) 
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True) 
    date_joined = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserProfile(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE) 
    address = models.TextField() 
    phone_no = models.CharField(max_length=15) 
    image = models.ImageField(upload_to='profiles/', null=True, blank=True) 
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True) 
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True) 
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True) 

class SportCategory(models.Model):
    category_name = models.CharField(max_length=100) 
    description = models.TextField() 
    image = models.ImageField(upload_to='categories/', null=True, blank=True) 

    def __str__(self):
        return self.category_name

class Turf(models.Model):
    turf_name = models.CharField(max_length=200) 
    description = models.TextField() 
    category = models.ForeignKey(SportCategory, on_delete=models.CASCADE) 
    address = models.TextField() 
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True) 
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True) 
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True) 
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2) 
    open_time = models.TimeField() 
    close_time = models.TimeField() 
    image = models.ImageField(upload_to='turfs/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.turf_name

class TurfImages(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='turfs/gallery/') 

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ] #

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE) 
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE) 
    booking_date = models.DateField() 
    start_time = models.TimeField() 
    end_time = models.TimeField() 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True) 

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('other', 'Other')
    ] #
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ] #

    user = models.ForeignKey(AppUser, on_delete=models.CASCADE) 
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    payment_date = models.DateTimeField(auto_now_add=True) #

class Review(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE) 
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE) 
    rating = models.IntegerField() 
    comment = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 

class ContactUs(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField() 
    phone = models.CharField(max_length=15) 
    message = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 