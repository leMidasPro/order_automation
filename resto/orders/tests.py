import shutil
import tempfile

from django.test import TestCase, override_settings
from django.urls import reverse

from products.models import Product


class InvoiceEndpointsTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.mkdtemp()
        self.media_override = override_settings(MEDIA_ROOT=self.media_dir)
        self.media_override.enable()
        self.product = Product.objects.create(
            name="Poulet braisé",
            price="2500.00",
            menu_order=1,
        )

    def tearDown(self):
        self.media_override.disable()
        shutil.rmtree(self.media_dir)

    def test_created_order_has_a_viewable_and_downloadable_pdf_invoice(self):
        response = self.client.post(
            reverse("orders:order"),
            data={
                "menu_order": self.product.menu_order,
                "quantite": 2,
                "phone": "+22890000000",
                "location": "Lomé",
            },
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertTrue(payload["success"])
        self.assertIn("download_url", payload)

        view_response = self.client.get(
            reverse("orders:invoice", args=[payload["order_id"]])
        )
        self.assertEqual(view_response.status_code, 200)
        self.assertEqual(view_response["Content-Type"], "application/pdf")
        self.assertTrue(b"".join(view_response.streaming_content).startswith(b"%PDF"))

        download_response = self.client.get(
            reverse("orders:download_invoice", args=[payload["order_id"]])
        )
        self.assertEqual(download_response.status_code, 200)
        self.assertIn("attachment", download_response["Content-Disposition"])
        self.assertIn("facture_", download_response["Content-Disposition"])

# Create your tests here.
