"""
Unit tests for authentication and token validation
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

User = get_user_model()


class InvalidTokenTestCase(APITestCase):
    """Test 45: Invalid Token Access scenarios"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Protected endpoint for testing
        self.protected_url = reverse('cart-list')
    
    def test_invalid_token_access(self):
        """Test access with completely invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token_here')
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('token', response.data['detail'].lower())
    
    def test_malformed_token_too_short(self):
        """Test access with malformed token (too short)"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer abc123')
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('token', response.data['detail'].lower())
    
    def test_empty_bearer_token(self):
        """Test access with empty Bearer token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer')
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_missing_bearer_prefix(self):
        """Test access with token missing 'Bearer' prefix"""
        token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=token)  # Missing 'Bearer '
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_expired_token(self):
        """Test access with expired token"""
        # Create an expired token (set exp to past time)
        import time
        from datetime import datetime, timedelta
        
        payload = {
            'user_id': self.user.id,
            'exp': datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
            'iat': datetime.utcnow() - timedelta(hours=2),
        }
        
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('expired', response.data['detail'].lower())
    
    def test_tampered_token(self):
        """Test access with tampered token"""
        # Get valid token and tamper with it
        valid_token = str(RefreshToken.for_user(self.user).access_token)
        tampered_token = valid_token[:-5] + 'XXXXX'  # Change last 5 characters
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tampered_token}')
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_valid_token_access(self):
        """Test that valid token works correctly"""
        valid_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {valid_token}')
        response = self.client.get(self.protected_url)
        
        # Should work (cart endpoint returns 200 for authenticated users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_no_authorization_header(self):
        """Test access without Authorization header"""
        response = self.client.get(self.protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials', response.data['detail'])


class AuthenticationEndpointsTestCase(APITestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
    
    def test_login_with_valid_credentials(self):
        """Test login with valid email and password"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_with_invalid_email(self):
        """Test login with invalid email"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('credentials', response.data['detail'].lower())
    
    def test_login_with_invalid_password(self):
        """Test login with invalid password"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_with_missing_fields(self):
        """Test login with missing required fields"""
        # Missing password
        response = self.client.post(self.login_url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing email
        response = self.client.post(self.login_url, {'password': 'testpass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_refresh(self):
        """Test token refresh functionality"""
        # First login to get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Use refresh token to get new access token
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
    
    def test_token_refresh_with_invalid_token(self):
        """Test token refresh with invalid refresh token"""
        refresh_data = {'refresh': 'invalid_refresh_token'}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
