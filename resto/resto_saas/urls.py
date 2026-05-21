from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/products/', include(('products.urls', 'products'),namespace='products')),
    path('api/orders/', include(('orders.urls', 'orders'),namespace='orders')),
    path('api/chatbot/', include(('chatbot.urls', 'chatbot'),namespace='chatbot')),
]
