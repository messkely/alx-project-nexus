from django.test import TestCase
from users.models import User
from catalog.models import Category, Product
from orders.models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="johndoe", password="password123")
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            title="Smartphone",
            description="A new smartphone",
            price=699.99,
            stock_quantity=50,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=0.00  # Will be updated by items
        )

    def test_order_default_statuses(self):
        self.assertEqual(self.order.status, "pending")
        self.assertEqual(self.order.payment_status, "unpaid")

    def test_order_str_method(self):
        expected_str = f"Order #{self.order.pk} - {self.user}"
        self.assertEqual(str(self.order), expected_str)


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="janedoe", password="password123")
        self.category = Category.objects.create(name="Accessories")
        self.product = Product.objects.create(
            title="USB-C Cable",
            description="Fast charging cable",
            price=19.99,
            stock_quantity=200,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=0.00
        )

    def test_order_item_subtotal(self):
        quantity = 3
        unit_price = self.product.price
        subtotal = quantity * unit_price

        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )

        self.assertEqual(item.subtotal, subtotal)
        self.assertEqual(str(item), f"{quantity} x {self.product.title} in Order #{self.order.pk}")
