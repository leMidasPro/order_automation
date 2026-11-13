from weasyprint import HTML
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.template.loader import render_to_string


def generate_invoice_pdf(order):
    """Generate and persist the PDF through the configured Django storage.

    Returning the FileField (rather than an absolute local path) keeps the
    invoice compatible with both local storage and a future cloud storage.
    """
    if order.invoice_pdf:
        try:
            if order.invoice_pdf.storage.exists(order.invoice_pdf.name):
                return order.invoice_pdf
        except (OSError, ValueError, SuspiciousFileOperation):
            # Old invoices may contain the absolute path produced by the
            # previous implementation. Regenerate them with a valid name.
            pass

    html_string = render_to_string('orders/fac.html', generate_invoice_data(order))
    pdf_content = HTML(string=html_string).write_pdf()

    file_name = f"facture_{order.id}.pdf"
    order.invoice_pdf.save(file_name, ContentFile(pdf_content), save=True)
    return order.invoice_pdf

def generate_invoice_data(order):
    return {
        "order_id": order.id,
        "product": order.product.name,
        "quantity": order.quantity,
        "unit_price": order.product.price,
        "total": order.total_price,
        "phone": order.customer_phone,
        "location": order.location,
        "status": order.get_status_display(),
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
