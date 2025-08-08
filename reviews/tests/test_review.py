from django.test import TestCase
from django.db import IntegrityError
from users.models import User
from catalog.models import Category, Product
from reviews.models import Review


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="user@example.com", password="pass1234")
        self.category = Category.objects.create(name="Laptops")
        self.product = Product.objects.create(
            title="MacBook Pro",
            description="Apple laptop",
            price=1999.99,
            inventory=10,
            category=self.category
        )

    def test_review_creation(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="Fantastic product!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Fantastic product!")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)

    def test_review_str_method(self):
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment="Nice but pricey."
        )
        expected = f"{self.user.email} review for {self.product.title}"
        self.assertEqual(str(review), expected)

    def test_unique_user_product_review(self):
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            comment="Okay."
        )

        with self.assertRaises(IntegrityError):
            Review.objects.create(
                user=self.user,
                product=self.product,
                rating=4,
                comment="Changed my mind."
            )
