from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('administrateur', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('employe', 'Employé'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employe')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    def __str__(self):
        return self.user.username

