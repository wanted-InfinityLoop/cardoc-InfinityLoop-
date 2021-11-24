from django.db import models


class Car(models.Model):
    brand    = models.CharField(max_length=16)
    model    = models.CharField(max_length=16)
    submodel = models.CharField(max_length=16)
    year     = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "cars"


class Trim(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    car  = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        db_table = "trims"


class Tire(models.Model):
    name         = models.CharField(max_length=16)
    width        = models.PositiveSmallIntegerField()
    aspect_ratio = models.PositiveSmallIntegerField()
    wheel_size   = models.PositiveSmallIntegerField()
    trim = models.ForeignKey(Trim, on_delete=models.CASCADE)

    class Meta:
        db_table = "tires"

