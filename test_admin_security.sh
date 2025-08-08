#!/bin/bash

echo "=== Testing Admin Endpoint Security ==="
echo

echo "1. Testing admin endpoints WITHOUT authentication:"
echo

echo "GET /api/v1/admin/products"
curl -s http://localhost:8000/api/v1/admin/products | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/v1/admin/products
echo

echo "GET /api/v1/admin/categories"  
curl -s http://localhost:8000/api/v1/admin/categories | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/v1/admin/categories
echo

echo "GET /api/v1/admin/products/1"
curl -s http://localhost:8000/api/v1/admin/products/1 | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/v1/admin/products/1
echo

echo "GET /api/v1/admin/categories/1"
curl -s http://localhost:8000/api/v1/admin/categories/1 | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/v1/admin/categories/1
echo

echo "=== Expected Result: All should return 'Authentication credentials were not provided.' ==="
echo

echo "2. Testing public endpoints (should work without auth):"
echo

echo "GET /api/v1/products/"
curl -s http://localhost:8000/api/v1/products/ | head -n 3
echo

echo "GET /api/v1/categories/"  
curl -s http://localhost:8000/api/v1/categories/ | head -n 3
echo

echo "=== Security Test Complete ==="
