from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
import os


def generate_invoice_pdf(order):
    data = generate_invoice_data(order)

    html_string = render_to_string('orders/fac.html', data)

    file_name = f"facture_{order.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    HTML(string=html_string).write_pdf(file_path)

    return file_path

def generate_invoice_data(order):
    return {
        "order_id": order.id,
        "product": order.product.name,
        "quantity": order.quantity,
        "unit_price": order.product.price,
        "total": order.total_price,
        "phone": order.customer_phone,
        "location": order.location,
        "status": order.status,
    }


def generate_invoice(order):
    return f"""
🧾 *FACTURE*

━━━━━━━━━━━━━━━

📌 *Commande N°* : {order.id}

🍽 *Plat* : {order.product.name}
🔢 *Quantité* : {order.quantity}
💵 *Prix unitaire* : {order.product.price} FCFA

━━━━━━━━━━━━━━━

💰 *TOTAL* : {order.total_price} FCFA

━━━━━━━━━━━━━━━

📞 *Client* : {order.customer_phone}
📍 *Adresse* : {order.location}

━━━━━━━━━━━━━━━

🚚 *Statut* : En cours de traitement

🙏 Merci pour votre confiance !
"""