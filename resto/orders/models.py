from django.db import models
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('livre', 'Livré'),
        ('annule', 'Annulé'),
    )

    user = models.ForeignKey('accounts.User',on_delete=models.SET_NULL,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    customer_phone = models.CharField(max_length=20)
    location = models.TextField()
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_phone}"