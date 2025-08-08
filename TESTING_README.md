# 🧪 Testing Guide - ALX E-Commerce Backend

Complete testing documentation for the ALX E-Commerce Backend project, covering unit tests, integration tests, API testing, and security testing.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Test Suite Structure](#-test-suite-structure)
- [Running Tests](#-running-tests)
- [Test Categories](#-test-categories)
- [API Testing](#-api-testing)
- [Security Testing](#-security-testing)
- [Performance Testing](#-performance-testing)
- [Test Data](#-test-data)
- [Continuous Integration](#-continuous-integration)
- [Test Coverage](#-test-coverage)
- [Writing New Tests](#-writing-new-tests)

---

## 🎯 Overview

Our testing strategy ensures comprehensive coverage across all application layers:

### Test Statistics
- **Total Tests**: 63+ test methods
- **Test Files**: 9 test files
- **Coverage Target**: >90%
- **Test Categories**: Unit, Integration, API, Security

### Testing Framework
- **Django Test Framework**: Built-in testing capabilities
- **Django REST Framework Test**: API testing utilities
- **Factory Boy**: Test data generation (optional)
- **Coverage.py**: Code coverage analysis

---

## 🏗️ Test Suite Structure

```
alx-project-nexus/
├── 🧪 Integration Tests
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth_endpoints.py      # Authentication API tests
│   │   ├── test_products_api.py        # Product API tests
│   │   └── test_categories_api.py      # Category API tests
│
├── 📦 Unit Tests (App-specific)
│   ├── users/tests/
│   │   ├── __init__.py
│   │   ├── test_models.py              # User model tests
│   │   ├── test_views.py               # User view tests
│   │   └── test_serializers.py         # User serializer tests
│   │
│   ├── catalog/tests/
│   │   ├── __init__.py
│   │   ├── test_models.py              # Product/Category model tests
│   │   ├── test_views.py               # Catalog view tests
│   │   └── test_serializers.py         # Catalog serializer tests
│   │
│   ├── cart/tests/
│   │   ├── __init__.py
│   │   └── test_cart.py                # Cart functionality tests
│   │
│   ├── orders/tests/
│   │   ├── __init__.py
│   │   └── test_orders.py              # Order processing tests
│   │
│   └── reviews/tests/
│       ├── __init__.py
│       └── test_reviews.py             # Review system tests
│
├── 🛠️ Test Utilities
│   ├── test_utils.py                   # Common test utilities
│   └── fixtures/                       # Test data fixtures
```

---

## 🚀 Running Tests

### Docker Environment (Recommended)

```bash
# Run all tests
make test

# Run with verbose output
docker compose exec web python manage.py test --verbosity=2

# Run specific app tests
docker compose exec web python manage.py test users
docker compose exec web python manage.py test catalog
docker compose exec web python manage.py test tests.test_auth_endpoints

# Run single test class
docker compose exec web python manage.py test tests.test_auth_endpoints.AuthEndpointTests

# Run single test method
docker compose exec web python manage.py test tests.test_auth_endpoints.AuthEndpointTests.test_user_registration
```

### Local Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML coverage report

# Run specific tests
python manage.py test users.tests.test_models
python manage.py test catalog.tests
python manage.py test tests.test_products_api

# Run with specific settings
python manage.py test --settings=ecommerce_backend.test_settings
```

### Test Database

```bash
# Django automatically creates and destroys test databases
# Test database name: test_ecommerce (for PostgreSQL)
# No manual database setup required
```

---

## 📚 Test Categories

### 1. Unit Tests

#### User Model Tests (`users/tests/test_models.py`)
- User creation and validation
- Custom user manager functionality
- User profile relationships
- Password hashing and validation

```python
class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating a user with email is successful"""
        
    def test_create_user_without_email_raises_error(self):
        """Test creating user without email raises ValueError"""
        
    def test_create_superuser(self):
        """Test creating a superuser"""
```

#### Product Model Tests (`catalog/tests/test_models.py`)
- Product creation and validation
- Category relationships
- Price validation
- Stock management
- Slug generation

```python
class ProductModelTests(TestCase):
    def test_create_product(self):
        """Test creating a product with valid data"""
        
    def test_product_str_representation(self):
        """Test the string representation of product"""
        
    def test_product_slug_generation(self):
        """Test automatic slug generation"""
```

### 2. Integration Tests

#### Authentication API Tests (`tests/test_auth_endpoints.py`)
- User registration endpoint
- JWT token creation
- Token refresh functionality
- User profile endpoints
- Permission-based access

```python
class AuthEndpointTests(APITestCase):
    def test_user_registration_success(self):
        """Test successful user registration"""
        
    def test_user_registration_invalid_data(self):
        """Test registration with invalid data"""
        
    def test_jwt_token_creation(self):
        """Test JWT token creation on login"""
        
    def test_jwt_token_refresh(self):
        """Test JWT token refresh functionality"""
```

#### Product API Tests (`tests/test_products_api.py`)
- Product CRUD operations
- Filtering and search functionality
- Pagination testing
- Permission-based access control
- Bulk operations

```python
class ProductAPITests(APITestCase):
    def test_get_products_list(self):
        """Test retrieving products list"""
        
    def test_create_product_admin_user(self):
        """Test product creation by admin user"""
        
    def test_create_product_unauthorized(self):
        """Test product creation by unauthorized user"""
        
    def test_product_filtering_by_category(self):
        """Test product filtering functionality"""
```

### 3. Security Tests

#### Permission Tests
- Role-based access control
- Admin-only endpoints
- User-specific data access
- Anonymous user restrictions

```python
class SecurityTests(APITestCase):
    def test_admin_only_product_creation(self):
        """Test that only admin users can create products"""
        
    def test_user_can_only_access_own_orders(self):
        """Test users can only access their own orders"""
        
    def test_anonymous_user_restrictions(self):
        """Test anonymous user access restrictions"""
```

#### Authentication Security Tests
- Invalid token handling
- Expired token validation
- Token blacklisting
- Password strength validation

---

## 🔍 API Testing

### Test Client Setup

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

class BaseAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
    def authenticate_user(self, user=None):
        """Helper method to authenticate user"""
        if user is None:
            user = self.user
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
```

### API Test Examples

#### Testing Product Creation
```python
def test_create_product_success(self):
    """Test successful product creation by admin"""
    admin_user = get_user_model().objects.create_superuser(
        email='admin@example.com',
        username='admin',
        password='adminpass123'
    )
    self.authenticate_user(admin_user)
    
    data = {
        'title': 'Test Product',
        'description': 'Test Description',
        'price': '99.99',
        'category': self.category.id,
        'stock_quantity': 10
    }
    
    response = self.client.post('/api/v1/products/', data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['title'], 'Test Product')
```

#### Testing Authentication
```python
def test_jwt_authentication_required(self):
    """Test that authentication is required for protected endpoints"""
    response = self.client.get('/api/v1/orders/')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Authenticate and try again
    self.authenticate_user()
    response = self.client.get('/api/v1/orders/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
```

---

## 🛡️ Security Testing

### Authentication Tests
- JWT token validation
- Token expiration handling
- Refresh token security
- Password hashing verification

### Authorization Tests
- Role-based permissions
- Object-level permissions
- Admin access controls
- User data isolation

### Input Validation Tests
- SQL injection prevention
- XSS protection
- Input sanitization
- File upload security

### Example Security Test
```python
def test_sql_injection_prevention(self):
    """Test that SQL injection attacks are prevented"""
    malicious_input = "'; DROP TABLE catalog_product; --"
    
    response = self.client.get(
        f'/api/v1/products/?search={malicious_input}'
    )
    # Should return 200 without executing malicious SQL
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Verify products table still exists
    from catalog.models import Product
    self.assertTrue(Product.objects.exists())
```

---

## ⚡ Performance Testing

### Database Query Testing
```python
def test_product_list_query_efficiency(self):
    """Test that product list uses efficient queries"""
    with self.assertNumQueries(2):  # Should only make 2 queries
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

### Load Testing Preparation
```python
def test_bulk_product_creation(self):
    """Test creating multiple products for load testing"""
    products_data = [
        {
            'title': f'Product {i}',
            'description': f'Description {i}',
            'price': f'{i * 10}.99',
            'category': self.category.id,
            'stock_quantity': i * 5
        }
        for i in range(100)
    ]
    
    # Bulk create products for performance testing
    for data in products_data:
        response = self.client.post('/api/v1/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

---

## 📊 Test Data

### Fixtures
Create reusable test data in `fixtures/` directory:

```python
# fixtures/test_data.py
from django.contrib.auth import get_user_model
from catalog.models import Category, Product

class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire TestCase"""
        cls.user = get_user_model().objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        cls.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        
        cls.category = Category.objects.create(
            name='Electronics',
            description='Electronic products'
        )
        
        cls.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price='99.99',
            category=cls.category,
            stock_quantity=10
        )
```

### Factory Pattern (Optional)
```python
# Using factory_boy for complex test data
import factory
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
    
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'catalog.Product'
    
    title = factory.Faker('word')
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category = factory.SubFactory('catalog.CategoryFactory')
```

---

## 🔄 Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: ecommerce_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage
    
    - name: Run tests with coverage
      run: |
        coverage run --source='.' manage.py test
        coverage report
        coverage xml
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: tests
        name: tests
        entry: python manage.py test
        language: system
        pass_filenames: false
        always_run: true
```

---

## 📈 Test Coverage

### Coverage Goals
- **Overall Coverage**: >90%
- **Models**: >95%
- **Views**: >90%
- **Serializers**: >85%
- **Utilities**: >90%

### Coverage Commands
```bash
# Generate coverage report
coverage run --source='.' manage.py test
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser

# Coverage with branch analysis
coverage run --branch --source='.' manage.py test
coverage report --show-missing

# Export coverage data
coverage xml  # For CI/CD integration
coverage json # For programmatic access
```

### Coverage Configuration
```ini
# .coveragerc
[run]
source = .
omit = 
    */venv/*
    */migrations/*
    manage.py
    */settings/*
    */tests/*
    */test_*.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

---

## ✍️ Writing New Tests

### Test Guidelines
1. **Descriptive Names**: Use clear, descriptive test method names
2. **Single Responsibility**: Each test should test one specific behavior
3. **Arrange-Act-Assert**: Follow the AAA pattern
4. **Independent Tests**: Tests should not depend on each other
5. **Data Cleanup**: Use setUp/tearDown or transactions for clean state

### Test Template
```python
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class NewFeatureTests(APITestCase):
    def setUp(self):
        """Set up test data before each test method"""
        # Create test data here
        pass
    
    def test_feature_success_case(self):
        """Test description of what this test validates"""
        # Arrange
        # Set up test data and conditions
        
        # Act
        # Perform the action being tested
        response = self.client.get('/api/endpoint/')
        
        # Assert
        # Verify the results
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('expected_key', response.data)
    
    def test_feature_failure_case(self):
        """Test error handling for invalid input"""
        # Arrange
        invalid_data = {'invalid': 'data'}
        
        # Act
        response = self.client.post('/api/endpoint/', invalid_data)
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def tearDown(self):
        """Clean up after each test method"""
        # Clean up test data if needed
        pass
```

### Model Test Example
```python
class ProductModelTests(TestCase):
    def test_create_product_with_valid_data(self):
        """Test creating a product with all valid data"""
        category = Category.objects.create(name='Test Category')
        
        product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price=Decimal('99.99'),
            category=category,
            stock_quantity=10
        )
        
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.category, category)
        self.assertEqual(product.stock_quantity, 10)
        self.assertTrue(product.slug)  # Auto-generated slug
```

### API Test Example
```python
class ProductAPITests(APITestCase):
    def test_filter_products_by_category(self):
        """Test filtering products by category"""
        # Create test data
        electronics = Category.objects.create(name='Electronics')
        books = Category.objects.create(name='Books')
        
        Product.objects.create(title='iPhone', category=electronics, price='999.99')
        Product.objects.create(title='Python Book', category=books, price='49.99')
        
        # Test filtering
        response = self.client.get(f'/api/v1/products/?category={electronics.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'iPhone')
```

---

## 🚨 Test Debugging

### Debug Failed Tests
```bash
# Run specific failed test with verbose output
python manage.py test tests.test_products_api.ProductAPITests.test_create_product --verbosity=2

# Use pdb for debugging
import pdb; pdb.set_trace()  # Add to test code

# Print debug information
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Test Issues
1. **Database State**: Tests affecting each other due to shared data
2. **Authentication**: Forgetting to authenticate test client
3. **Time-dependent Tests**: Tests that depend on current time
4. **External Dependencies**: Tests that depend on external services

### Test Performance
```bash
# Run tests with timing information
python manage.py test --verbosity=2 --timing

# Profile test execution
python -m cProfile manage.py test
```

---

## 📝 Test Documentation

### Documenting Test Cases
- Use docstrings to describe test purpose
- Include expected behavior in test names
- Document test data requirements
- Explain complex test scenarios

### Test Reports
```bash
# Generate test report
python manage.py test --verbosity=2 > test_report.txt

# Generate JUnit XML report (for CI/CD)
pip install django-nose
# Configure in settings
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-xunit']
```

---

## 🎯 Testing Best Practices

### Do's
- ✅ Write tests before or during development (TDD)
- ✅ Use descriptive test names
- ✅ Test both success and failure scenarios
- ✅ Keep tests simple and focused
- ✅ Use test data factories for complex objects
- ✅ Mock external dependencies
- ✅ Run tests frequently during development

### Don'ts
- ❌ Write tests that depend on each other
- ❌ Test implementation details instead of behavior
- ❌ Use production data in tests
- ❌ Skip testing edge cases
- ❌ Write overly complex test setup
- ❌ Ignore failing tests
- ❌ Test third-party library functionality

---

## 🔧 Test Utilities

### Custom Test Assertions
```python
# test_utils.py
def assert_api_error(test_case, response, expected_status, expected_message=None):
    """Helper function to assert API error responses"""
    test_case.assertEqual(response.status_code, expected_status)
    if expected_message:
        test_case.assertIn(expected_message, str(response.data))

def create_test_user(email='test@example.com', is_staff=False, is_superuser=False):
    """Helper function to create test users"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        email=email,
        username=email.split('@')[0],
        password='testpass123',
        is_staff=is_staff,
        is_superuser=is_superuser
    )
```

### Test Mixins
```python
class AuthTestMixin:
    """Mixin to handle authentication in tests"""
    
    def authenticate_as_admin(self):
        """Authenticate test client as admin user"""
        admin_user = create_test_user('admin@example.com', is_staff=True, is_superuser=True)
        refresh = RefreshToken.for_user(admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return admin_user
    
    def authenticate_as_user(self):
        """Authenticate test client as regular user"""
        user = create_test_user('user@example.com')
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return user
```

---

## 🎯 Comprehensive Test List

Our 63+ test methods cover the following areas:

### Authentication & Authorization (12 tests)
- ✅ User registration validation
- ✅ JWT token creation and validation
- ✅ Token refresh functionality
- ✅ Permission-based access control
- ✅ Admin-only endpoint protection
- ✅ User profile management

### Product Management (15 tests)
- ✅ Product CRUD operations
- ✅ Category relationships
- ✅ Product filtering and search
- ✅ Price validation
- ✅ Stock management
- ✅ Slug generation
- ✅ Image handling

### Shopping Cart (8 tests)
- ✅ Add items to cart
- ✅ Update cart quantities
- ✅ Remove cart items
- ✅ Cart total calculations
- ✅ User-specific cart isolation

### Order Processing (10 tests)
- ✅ Order creation from cart
- ✅ Order status management
- ✅ Order history retrieval
- ✅ Order cancellation
- ✅ Payment processing simulation

### Review System (6 tests)
- ✅ Create product reviews
- ✅ Rating validation
- ✅ Review permissions
- ✅ Average rating calculations

### Security & Performance (12 tests)
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Rate limiting
- ✅ Database query optimization
- ✅ Input validation
- ✅ Access control verification

---

## 📊 Summary

This comprehensive testing guide provides:

- **Complete Test Coverage**: 63+ tests across all functionality
- **Multiple Test Types**: Unit, integration, API, and security tests
- **Practical Examples**: Real test code and patterns
- **Best Practices**: Guidelines for writing maintainable tests
- **CI/CD Integration**: Automated testing workflows
- **Performance Testing**: Query optimization and load testing
- **Security Testing**: Authentication and authorization validation

Our test suite ensures the ALX E-Commerce Backend is robust, secure, and ready for production deployment. Regular testing helps maintain code quality and catch regressions early in the development process.

---

*Happy Testing! 🚀*
