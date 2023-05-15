from django.db import models
from account.models import User
from location_field.models.plain import PlainLocationField

# Create your models here.

class Location(models.Model):
    city_name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name
    
class Resorts(models.Model):
    owner           = models.ForeignKey(User, on_delete=models.CASCADE)
    resort_name     = models.CharField(max_length=200)
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)
    map_location    = PlainLocationField(based_fields=['city'], zoom=7, blank=True, null=True)
    place           = models.CharField(max_length=100)
    address         = models.CharField(max_length=250)
    zipcode         = models.CharField(max_length=25)
    phone_number    = models.CharField(max_length=12)
    room_type       = models.CharField(max_length=100)
    price           = models.IntegerField()
    description     = models.TextField()
    rooms_available = models.IntegerField()
    pool_available  = models.BooleanField()
    wifi_available  = models.BooleanField()

    image_one       = models.ImageField(upload_to='photos/resorts')
    image_two       = models.ImageField(upload_to='photos/resorts')
    image_three     = models.ImageField(upload_to='photos/resorts',blank=True, null=True)
    image_four      = models.ImageField(upload_to='photos/resorts',blank=True, null=True)

    is_approved     = models.BooleanField(default=False)
    is_rejected   = models.BooleanField(default=False)

    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.resort_name
    
    
class Adventures(models.Model):
    owner         = models.ForeignKey(User, on_delete=models.CASCADE)
    resort        = models.ForeignKey(Resorts, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length= 200)
    place         = models.CharField(max_length=200)
    price         = models.IntegerField()
    about         = models.TextField()
    time_take     = models.CharField(max_length= 200)
    day_slot      = models.IntegerField()
    safety        = models.CharField(max_length= 200)
    is_approved   = models.BooleanField(default=False)
    is_rejected   = models.BooleanField(default=False)

    activity_one       = models.ImageField(upload_to='photos/adventures')
    activity_two       = models.ImageField(upload_to='photos/adventures')
    activity_three     = models.ImageField(upload_to='photos/adventures',blank=True, null=True)

    def __str__(self):
        return self.activity_name
    
class Destinations(models.Model):
    resort       = models.ForeignKey(Resorts, on_delete=models.CASCADE)
    owner        = models.ForeignKey(User, on_delete=models.CASCADE)
    place        = models.CharField(max_length=200)
    location     = models.FloatField(blank=True, null=True)
    spot_name    = models.CharField(max_length=200)
    map_location = PlainLocationField(based_fields=['city'], zoom=7, blank=True, null=True)
    about        = models.TextField()
    start_time   = models.TimeField()
    close_time   = models.TimeField()
    is_approved  = models.BooleanField(default=False)

    image_one    = models.ImageField(upload_to='photos/destinations')
    image_two    = models.ImageField(upload_to='photos/destinations')
    image_three  = models.ImageField(upload_to='photos/destinations', blank=True, null=True)

    def __str__(self):
        return self.spot_name