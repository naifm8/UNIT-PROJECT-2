from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class User(AbstractUser):
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('coach', 'Coach'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Player(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    profile_photo = models.ImageField(upload_to='players/', null=True, blank=True)
    parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'parent'}
    )

    def __str__(self):
        return self.full_name

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
