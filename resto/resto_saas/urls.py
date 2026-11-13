from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/products/', include(('products.urls', 'products'),namespace='products')),
    path('api/orders/', include(('orders.urls', 'orders'),namespace='orders')),
    path('api/chatbot/', include(('chatbot.urls', 'chatbot'),namespace='chatbot')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
