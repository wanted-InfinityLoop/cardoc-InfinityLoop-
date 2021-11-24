from django.db import models

class User(models.Model):
    id       = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = "users"
