from django.db import models
from products.models import Product

class ChatSession(models.Model):
    STEP_CHOICES = (
        ('accueil', 'Accueil'),
        ('menu', 'Menu'),
        ('choix', 'Choix'),
        ('quantite', 'Quantité'),
        ('localisation', 'Localisation'),
        ('confirmation', 'Confirmation'),
    )

    phone_number = models.CharField(max_length=20)

    step = models.CharField(max_length=20, choices=STEP_CHOICES, default='accueil')

    selected_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    quantity = models.PositiveIntegerField(null=True, blank=True)

    location = models.TextField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number