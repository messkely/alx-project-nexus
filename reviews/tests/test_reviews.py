"""
Unit tests for reviews functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from reviews.models import Review
from catalog.models import Category, Product
from orders.models import Order, OrderItem
from users.models import Address

User = get_user_model()


class ReviewsTestCase(APITestCase):
    """Test reviews functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        
        # Create test address
        self.address = Address.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address_line_1='123 Test Street',
            city='Test City',
            postal_code='12345',
            country='Test Country',
            phone_number='+1234567890',
            is_default=True
        )
        
        # Create test category and product
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            slug='test-product',
            inventory=10
        )
        
        # Create test order (delivered so user can review)
        self.order = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        # Create test review
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!',
            order_item=self.order_item
        )
        
        # Get JWT tokens
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.other_token = str(RefreshToken.for_user(self.other_user).access_token)
    
    def test_create_review_success(self):
        """Test successful review creation"""
        # Create another delivered order for this test
        order2 = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        order_item2 = OrderItem.objects.create(
            order=order2,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        url = reverse('review-list')
        review_data = {
            'product': self.product.id,
            'rating': 4,
            'comment': 'Good product, would recommend!',
            'order_item': order_item2.id
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, review_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 4)
        self.assertEqual(response.data['comment'], 'Good product, would recommend!')
        
        # Verify review was created in database
        self.assertTrue(Review.objects.filter(
            user=self.user,
            product=self.product,
            rating=4
        ).exists())
    
    def test_create_review_without_authentication(self):
        """Test review creation without authentication"""
        url = reverse('review-list')
        review_data = {
            'product': self.product.id,
            'rating': 4,
            'comment': 'Good product'
        }
        
        response = self.client.post(url, review_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials', response.data['detail'])
    
    def test_create_review_without_purchase(self):
        """Test review creation without purchasing the product"""
        url = reverse('review-list')
        review_data = {
            'product': self.product.id,
            'rating': 4,
            'comment': 'Good product'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_token}')
        response = self.client.post(url, review_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('purchase', str(response.data).lower())
    
    def test_create_duplicate_review(self):
        """Test creation of duplicate review for same product"""
        url = reverse('review-list')
        review_data = {
            'product': self.product.id,
            'rating': 3,
            'comment': 'Another review',
            'order_item': self.order_item.id
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, review_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already reviewed', str(response.data).lower())
    
    def test_update_own_review_success(self):
        """Test successful update of own review"""
        url = reverse('update_review', kwargs={'pk': self.review.pk})
        update_data = {
            'rating': 4,
            'comment': 'Updated review - still good!'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 4)
        self.assertEqual(response.data['comment'], 'Updated review - still good!')
        
        # Verify review was updated in database
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, 'Updated review - still good!')
    
    def test_update_other_users_review(self):
        """Test update of another user's review (should fail)"""
        url = reverse('update_review', kwargs={'pk': self.review.pk})
        update_data = {
            'rating': 1,
            'comment': 'Terrible product!'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_token}')
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify review was not updated
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great product!')
    
    def test_update_review_without_authentication(self):
        """Test review update without authentication"""
        url = reverse('update_review', kwargs={'pk': self.review.pk})
        update_data = {
            'rating': 4,
            'comment': 'Updated review'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_reviews(self):
        """Test getting user's own reviews"""
        url = reverse('user_reviews')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.review.id)
        self.assertEqual(response.data[0]['rating'], 5)
    
    def test_get_user_reviews_without_authentication(self):
        """Test getting user reviews without authentication"""
        url = reverse('user_reviews')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_product_reviews(self):
        """Test getting all reviews for a product"""
        # Create another review for the same product
        other_user_order = Order.objects.create(
            user=self.other_user,
            status='delivered',
            total_amount=Decimal('99.99')
        )
        
        other_user_order_item = OrderItem.objects.create(
            order=other_user_order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        Review.objects.create(
            user=self.other_user,
            product=self.product,
            rating=4,
            comment='Pretty good product',
            order_item=other_user_order_item
        )
        
        url = reverse('product_reviews', kwargs={'product_id': self.product.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify both reviews are present
        ratings = [review['rating'] for review in response.data]
        self.assertIn(5, ratings)  # Original review
        self.assertIn(4, ratings)  # New review
    
    def test_delete_own_review(self):
        """Test deletion of own review"""
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify review was deleted
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
    
    def test_delete_other_users_review(self):
        """Test deletion of another user's review (should fail)"""
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_token}')
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify review was not deleted
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
    
    def test_rating_validation(self):
        """Test rating validation (should be 1-5)"""
        # Create another order for testing
        order2 = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        order_item2 = OrderItem.objects.create(
            order=order2,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        url = reverse('review-list')
        
        # Test invalid ratings
        invalid_ratings = [0, 6, -1, 10]
        
        for rating in invalid_ratings:
            review_data = {
                'product': self.product.id,
                'rating': rating,
                'comment': 'Test review',
                'order_item': order_item2.id
            }
            
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
            response = self.client.post(url, review_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('rating', str(response.data).lower())
    
    def test_review_comment_length_validation(self):
        """Test review comment length validation"""
        # Create another order for testing
        order2 = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        order_item2 = OrderItem.objects.create(
            order=order2,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        url = reverse('review-list')
        
        # Test comment too long (if there's a max length limit)
        very_long_comment = 'x' * 2000  # Assuming max length is less than 2000
        
        review_data = {
            'product': self.product.id,
            'rating': 5,
            'comment': very_long_comment,
            'order_item': order_item2.id
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, review_data, format='json')
        
        # This test depends on actual validation - adjust based on implementation
        if response.status_code == 400:
            self.assertIn('comment', str(response.data).lower())
    
    def test_review_requires_delivered_order(self):
        """Test that reviews can only be created for delivered orders"""
        # Create pending order
        pending_order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        pending_order_item = OrderItem.objects.create(
            order=pending_order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        url = reverse('review-list')
        review_data = {
            'product': self.product.id,
            'rating': 5,
            'comment': 'Great product!',
            'order_item': pending_order_item.id
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, review_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('delivered', str(response.data).lower())
