from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    city = models.CharField(max_length=255)
    is_merchant = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Restaurant(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, blank=False, null=False)
    food_type = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=1024, blank=False, null=False)
    open_time = models.TimeField(blank=False, null=True)
    close_time = models.TimeField(blank=False, null=True)
    lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    long = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return "<{}: {}>".format(self.pk, self.name)


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    # is_organic = models.BooleanField(default=False, blank=False, null=False)
    # is_vegan = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return "<{}: {}$>".format(self.restaurant, self.name)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    foods = models.ManyToManyField(Food)
    is_accepted = models.BooleanField(default=False, blank=False, null=False)
    is_cancelled = models.BooleanField(default=False, blank=False, null=False)
    is_delivered = models.BooleanField(default=False, blank=False, null=False)
    create_datetime = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    accept_datetime = models.DateTimeField(default=None, null=True, blank=True)
    cancell_datetime = models.DateTimeField(default=None, null=True, blank=True)
    delivered_datetime = models.DateTimeField(default=None, null=True, blank=True)
    note = models.CharField(max_length=1024, default="")
    time_to_deliver = models.IntegerField(
        validators=[MinValueValidator(1)], blank=False, null=False, default=30
    )
