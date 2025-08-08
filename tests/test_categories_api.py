from rest_framework.test import APITestCase
from catalog.models import Category
from users.models import User
from rest_framework import status


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="adminpass", email="admin@example.com", is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.admin)
        Category.objects.create(name="Laptops")
        Category.objects.create(name="Phones")

    def test_get_categories_list(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_create_category(self):
        response = self.client.post("/api/categories/", {"name": "Tablets"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)
