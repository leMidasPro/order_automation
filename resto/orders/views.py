from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import Order
from products.models import Product
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_invoice_pdf, generate_invoice

def invoice_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        html = generate_invoice_pdf(order)
        return HttpResponse(html)
    except Order.DoesNotExist:
        return HttpResponse("Facture non trouvée")


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            product = Product.objects.get(menu_order=data['menu_order'])
            quantity = int(data['quantite'])

            total = product.price * quantity

            order = Order.objects.create(
                product=product,
                quantity=quantity,
                total_price=total,
                customer_phone=data['phone'],
                location=data['location'],
                user=request.user if request.user.is_authenticated else None
            )

            pdf_path = generate_invoice_pdf(order)
            invoice_text = generate_invoice(order)

            order.invoice_pdf = pdf_path
            order.save()

            return JsonResponse({

                f"📄 Votre facture est prête. {invoice_text}"

                'success': True,
                'order_id': order.id
            })

        except Exception as e:
            return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid method'})
