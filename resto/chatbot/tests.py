import shutil
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse

from products.models import Product


class WhatsAppInvoiceTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_dir)
        self.media_override.enable()
        Product.objects.create(
            name="Riz au poulet",
            price="3000.00",
            menu_order=1,
            is_active=True,
        )

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.media_dir)

    def test_confirmed_whatsapp_order_returns_invoice_links(self):
        url = reverse("chatbot:webhook")
        phone = "+22891111111"

        for message in ("bonjour", "menu", "1", "2", "Lomé"):
            response = self.client.post(url, {"message": message, "phone": phone})
            self.assertEqual(response.status_code, 200)

        response = self.client.post(url, {"message": "confirmer", "phone": phone})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("invoice_url", payload)
        self.assertIn("download_url", payload)
        self.assertIn("facture", payload["reply"].lower())

# Create your tests here.
