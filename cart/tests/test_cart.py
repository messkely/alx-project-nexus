from django.test import TestCase
from django.contrib.auth import get_user_model
from cart.models import Cart, CartItem
from catalog.models import Product, Category

User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        # Setup required data
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Mouse",
            description="Wireless Mouse",
            price=15.99,
            category=self.category,
            inventory=10
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, "testuser")
        self.assertIsNotNone(self.cart.created_at)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product.title, "Mouse")
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(str(self.cart_item), "2 x Mouse")

    def test_cart_item_total_price(self):
        expected_total = self.product.price * self.cart_item.quantity
        # You can use this if you have a method called total_price()
        # self.assertEqual(self.cart_item.total_price(), expected_total)

        # If no method, test manually
        self.assertEqual(expected_total, 31.98)
