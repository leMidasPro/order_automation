from django.http import JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
import json
from .models import Order
from products.models import Product
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_invoice_pdf, generate_invoice

def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice = generate_invoice_pdf(order)
    invoice.open("rb")
    return FileResponse(
        invoice,
        content_type="application/pdf",
        filename=f"facture_{order.id}.pdf",
    )


@csrf_exempt
def create_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        product = Product.objects.get(menu_order=data['menu_order'])
        quantity = int(data['quantite'])
        if quantity <= 0:
            raise ValueError("La quantité doit être supérieure à zéro.")

        order = Order.objects.create(
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
            customer_phone=data['phone'],
            location=data['location'],
            user=request.user if request.user.is_authenticated else None,
        )
        generate_invoice_pdf(order)

        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'invoice_url': request.build_absolute_uri(
                reverse('orders:invoice', args=[order.id])
            ),
            'download_url': request.build_absolute_uri(
                reverse('orders:download_invoice', args=[order.id])
            ),
            'invoice_text': generate_invoice(order),
        }, status=201)
    except (KeyError, ValueError, json.JSONDecodeError) as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produit introuvable.'}, status=404)


def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice = generate_invoice_pdf(order)
    invoice.open("rb")
    return FileResponse(
        invoice,
        as_attachment=True,
        content_type="application/pdf",
        filename=f"facture_{order.id}.pdf",
    )
