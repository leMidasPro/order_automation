from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
import json

from .models import ChatSession
from products.models import Product
from orders.models import Order
from orders.utils import generate_invoice_pdf, generate_invoice


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        message = data.get('message', '').lower()
        phone = data.get('phone')

        # 🔹 récupérer ou créer session
        session, created = ChatSession.objects.get_or_create(
            phone_number=phone
        )

        # 🔹 STEP 1 : GREETING
        if message in ["bonjour", "salut", "hello"]:
            session.step = "accueil"
            session.save()

            return JsonResponse({
                "reply": "Bienvenue 👋\nTapez *menu* pour voir nos plats"
            })

        # 🔹 STEP 2 : MENU
        if message == "menu":
            products = Product.objects.filter(is_active=True).order_by('menu_order')

            menu_text = "🍽 *Menu* :\n\n"
            for p in products:
                menu_text += f"{p.menu_order}️⃣ {p.name} - {p.price} FCFA\n"

            session.step = "menu"
            session.save()

            return JsonResponse({
                "reply": menu_text + "\nChoisissez le numéro du plat"
            })

        # 🔹 STEP 3 : CHOIX DU PLAT
        if session.step == "menu":
            try:
                product = Product.objects.get(menu_order=int(message))
                session.selected_product = product
                session.step = "choix"
                session.save()

                return JsonResponse({
                    "reply": f"Vous avez choisi {product.name}\nCombien de plats voulez-vous ?"
                })
            except:
                return JsonResponse({
                    "reply": "Choix invalide ❌, veuillez entrer un numéro valide"
                })

        # 🔹 STEP 4 : QUANTITÉ
        if session.step == "choix":
            try:
                quantity = int(message)
                session.quantity = quantity
                session.step = "quantite"
                session.save()

                return JsonResponse({
                    "reply": "Veuillez envoyer votre localisation 📍"
                })
            except:
                return JsonResponse({
                    "reply": "Veuillez entrer un nombre valide"
                })

        # 🔹 STEP 5 : LOCALISATION
        if session.step == "quantite":
            session.location = message
            session.step = "localisation"
            session.save()

            product = session.selected_product
            total = product.price * session.quantity

            return JsonResponse({
                "reply": f"""
                Confirmez votre commande :

                Plat : {product.name}
                Quantité : {session.quantity}
                Total : {total} FCFA

                Tapez *confirmer* pour valider
                """
            })

        # 🔹 STEP 6 : CONFIRMATION
        if session.step == "localisation" and message == "confirmer":
            product = session.selected_product
            total = product.price * session.quantity

            order = Order.objects.create(
                product=product,
                quantity=session.quantity,
                total_price=total,
                customer_phone=phone,
                location=session.location
            )

            generate_invoice_pdf(order)
            invoice_text = generate_invoice(order)

            invoice_url = request.build_absolute_uri(
                reverse('orders:invoice', args=[order.id])
            )
            download_url = request.build_absolute_uri(
                reverse('orders:download_invoice', args=[order.id])
            )

            order_quantity = order.quantity
            order_total = order.total_price

            # reset session
            session.step = "accueil"
            session.selected_product = None
            session.quantity = None
            session.location = None
            session.save()

            return JsonResponse({
                "reply": f"""
                ✅ Commande confirmée
                {invoice_text}

                📄 Votre facture est prête.

                Voir : {invoice_url}
                Télécharger : {download_url}

                Plat : {product.name}
                Quantité : {order_quantity}
                Total : {order_total} FCFA

                Merci pour votre confiance 🙏
                """,
                "order_id": order.id,
                "invoice_url": invoice_url,
                "download_url": download_url,
            })

        # 🔹 FALLBACK
        return JsonResponse({
            "reply": "Je n’ai pas compris 🤖\nTapez *menu* pour commencer"
        })

    return JsonResponse({'error': 'Invalid method'})
