"""
Unit tests for catalog app - Admin permissions and security
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from catalog.models import Category, Product
from catalog.permissions import IsAdminOrReadOnly

User = get_user_model()


class AdminPermissionsTestCase(APITestCase):
    """Test admin permissions for catalog endpoints (Test 50)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            username='regular_user',
            password='testpass123',
            is_staff=False
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin_user', 
            password='testpass123',
            is_staff=True
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Create test product
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=99.99,
            category=self.category,
            slug='test-product',
            inventory=10
        )
        
        # Get JWT tokens
        self.regular_token = str(RefreshToken.for_user(self.regular_user).access_token)
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_admin_product_creation_permissions(self):
        """Test 50: Verify admin product creation permissions"""
        url = reverse('admin-product-list')
        data = {
            'title': 'New Test Product',
            'description': 'New test description',
            'price': '149.99',
            'category': self.category.id,
            'slug': 'new-test-product',
            'inventory': 5
        }
        
        # Test without authentication - should get 401
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with regular user - should get 403
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('permission', response.data['detail'].lower())
        
        # Test with admin user - should succeed
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Product')
    
    def test_admin_product_read_permissions(self):
        """Verify read permissions allow all users"""
        url = reverse('admin-product-list')
        
        # Test without authentication - should work (public read)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with regular user - should work
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test with admin user - should work
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_admin_product_update_permissions(self):
        """Test admin product update permissions"""
        url = reverse('admin-product-detail', kwargs={'pk': self.product.pk})
        data = {'title': 'Updated Product Title', 'price': '199.99'}
        
        # Test without authentication - should get 401
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with regular user - should get 403
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with admin user - should succeed
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Product Title')
    
    def test_admin_product_delete_permissions(self):
        """Test admin product delete permissions"""
        url = reverse('admin-product-detail', kwargs={'pk': self.product.pk})
        
        # Test without authentication - should get 401
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with regular user - should get 403
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with admin user - should succeed
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify product was deleted
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())


class AdminRootSecurityTestCase(APITestCase):
    """Test admin root endpoint security (Information Disclosure Prevention)"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            username='regular_user',
            password='testpass123',
            is_staff=False
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin_user',
            password='testpass123',
            is_staff=True
        )
        
        # Get JWT tokens
        self.regular_token = str(RefreshToken.for_user(self.regular_user).access_token)
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
    
    def test_admin_root_without_auth(self):
        """Test admin root access without authentication"""
        url = reverse('admin_root')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials', response.data['detail'])
    
    def test_admin_root_with_regular_user(self):
        """Test admin root access with regular user (should be blocked)"""
        url = reverse('admin_root')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.regular_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('permission', response.data['detail'].lower())
    
    def test_admin_root_with_admin_user(self):
        """Test admin root access with admin user (should work)"""
        url = reverse('admin_root')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('products', response.data)
        self.assertIn('categories', response.data)


class IsAdminOrReadOnlyPermissionTestCase(TestCase):
    """Test the IsAdminOrReadOnly permission class"""
    
    def setUp(self):
        """Set up test users"""
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            username='regular_user',
            password='testpass123',
            is_staff=False
        )
        
        self.admin_user = User.objects.create_user(
            email='admin@test.com', 
            username='admin_user',
            password='testpass123',
            is_staff=True
        )
        
        self.permission = IsAdminOrReadOnly()
    
    def test_safe_methods_allowed_for_all(self):
        """Test that safe methods (GET, HEAD, OPTIONS) are allowed for all users"""
        from django.test import RequestFactory
        from rest_framework.permissions import SAFE_METHODS
        
        factory = RequestFactory()
        
        for method in SAFE_METHODS:
            request = getattr(factory, method.lower())('/')
            request.user = self.regular_user
            
            self.assertTrue(
                self.permission.has_permission(request, None),
                f"Safe method {method} should be allowed for regular users"
            )
    
    def test_unsafe_methods_require_admin(self):
        """Test that unsafe methods require admin privileges"""
        from django.test import RequestFactory
        
        factory = RequestFactory()
        unsafe_methods = ['post', 'put', 'patch', 'delete']
        
        for method in unsafe_methods:
            # Test with regular user
            request = getattr(factory, method)('/')
            request.user = self.regular_user
            
            self.assertFalse(
                self.permission.has_permission(request, None),
                f"Unsafe method {method.upper()} should be blocked for regular users"
            )
            
            # Test with admin user
            request.user = self.admin_user
            
            self.assertTrue(
                self.permission.has_permission(request, None),
                f"Unsafe method {method.upper()} should be allowed for admin users"
            )
