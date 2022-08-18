from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name
