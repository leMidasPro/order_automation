from django.urls import path
from .views import *
urlpatterns = [
    path('create_order/', create_order, name="order"),
    path('invoice/<int:order_id>/', invoice_view, name="invoice"),
    path('invoice/pdf/<int:order_id>/', download_invoice, name="download_invoice"),
]