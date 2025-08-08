from django.test import TestCase
from catalog.models import Category, Product
from django.utils.text import slugify


class CategoryModelTest(TestCase):

    def test_category_slug_auto_generation(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.slug, slugify("Electronics"))

    def test_category_str_method(self):
        category = Category.objects.create(name="Books")
        self.assertEqual(str(category), "Books")


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Gadgets")

    def test_product_creation_and_slug(self):
        product = Product.objects.create(
            title="Wireless Mouse",
            description="A smooth wireless mouse",
            price=49.99,
            inventory=20,
            category=self.category
        )
        self.assertEqual(product.slug, slugify("Wireless Mouse"))
        self.assertEqual(product.price, 49.99)
        self.assertEqual(product.inventory, 20)
        self.assertEqual(product.category, self.category)

    def test_product_str_method(self):
        product = Product.objects.create(
            title="Mechanical Keyboard",
            description="A clicky mechanical keyboard",
            price=89.99,
            inventory=15,
            category=self.category
        )
        self.assertEqual(str(product), "Mechanical Keyboard")
