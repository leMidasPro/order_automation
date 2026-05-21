from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json

def list_products(request):
    if request.method == 'GET':
        products = Product.objects.filter(is_active=True).order_by('menu_order')

        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'price': str(p.price),
                'menu_order': p.menu_order
            })

        return JsonResponse({'products': data})
    
    return JsonResponse({'error': 'Invalid method'})



@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            product = Product.objects.create(
                name=data['name'],
                price=data['price'],
                menu_order=data.get('menu_order', 0),
                created_by=request.user if request.user.is_authenticated else None
            )

            return JsonResponse({'success': True, 'id': product.id})

        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid method'})
