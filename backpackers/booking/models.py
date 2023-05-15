from django.db import models
from account.models import User
from resorts.models import Resorts, Adventures, Destinations

# Create your models here.


class ResortBooking(models.Model):
    STATUS = (
        ("New", "New"),
        ("Checked In", "Checked In"),
        ("Checked Out", "Checked Out"),
        ("Cancelled", "Cancelled"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_resort = models.ForeignKey(Resorts, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=20)
    check_in = models.DateField()
    check_out = models.DateField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    booking_total = models.FloatField()
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS, default="New")
    occupancy = models.IntegerField()

    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class AdventureBooking(models.Model):
    STATUS = (
        ("New", "New"),
        ("Checked In", "Checked In"),
        ("Checked Out", "Checked Out"),
        ("Pending", "Pending"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_activity = models.ForeignKey(Adventures, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    age = models.IntegerField()
    activity_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    weight = models.IntegerField()
    guardian_name = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=50)
    booking_total = models.FloatField()
    medical_condition = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=30)

    status = models.CharField(max_length=20, choices=STATUS, default="New")
    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class ResortReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resorts, on_delete=models.CASCADE)
    review_heading = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()
    review_image = models.ImageField(upload_to="photos/resortReviews", blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + self.resort.resort_name


class AdventureReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventures, on_delete=models.CASCADE)
    review_heading = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()
    review_image = models.ImageField(upload_to="photos/adventureReviews")
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + self.adventure.activity_name


class DestinationReviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE)
    review_heading = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()
    review_image = models.ImageField(upload_to="photos/adventureReviews")
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + self.destination.spot_name


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    discount_amount = models.IntegerField()
    expiration_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coupon_name


class CouponAssign(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + self.coupon.coupon_name


class ResortPayments(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    order = models.IntegerField()
    payment_id = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " " + str(self.order)
