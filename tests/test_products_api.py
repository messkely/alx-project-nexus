from rest_framework.test import APITestCase
from catalog.models import Category, Product
from users.models import User
from rest_framework import status


class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="creator", email="creator@example.com", password="password123", is_staff=True)
        self.category = Category.objects.create(name="Accessories")
        self.client.force_authenticate(user=self.user)

        self.product = Product.objects.create(
            title="USB Cable",
            description="Fast charge",
            price=9.99,
            inventory=100,
            category=self.category
        )

    def test_create_product(self):
        data = {
            "title": "Bluetooth Speaker",
            "description": "Loud and clear",
            "price": "49.99",
            "inventory": 30,
            "category": self.category.id
        }
        response = self.client.post("/api/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product_patch(self):
        response = self.client.patch(f"/api/products/{self.product.id}/", {"price": "14.99"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(str(self.product.price), "14.99")

    def test_delete_product(self):
        response = self.client.delete(f"/api/products/{self.product.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)
