#!/usr/bin/env python
"""
Comprehensive Security Audit Script for E-Commerce Backend
This script checks for common security vulnerabilities and misconfigurations.
"""

import os
import sys
import re
import requests
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import User


class SecurityAudit:
    def __init__(self):
        self.findings = []
        self.base_url = "http://localhost:8001"
    
    def log_finding(self, severity, category, message, recommendation=None):
        """Log a security finding"""
        finding = {
            'severity': severity,  # CRITICAL, HIGH, MEDIUM, LOW, INFO
            'category': category,
            'message': message,
            'recommendation': recommendation
        }
        self.findings.append(finding)
        
        severity_colors = {
            'CRITICAL': '\033[91m',  # Red
            'HIGH': '\033[93m',      # Yellow
            'MEDIUM': '\033[94m',    # Blue
            'LOW': '\033[92m',       # Green
            'INFO': '\033[96m'       # Cyan
        }
        
        color = severity_colors.get(severity, '\033[0m')
        print(f"{color}[{severity}] {category}: {message}\033[0m")
        if recommendation:
            print(f"  └─ Recommendation: {recommendation}")
    
    def check_django_settings(self):
        """Check Django settings for security issues"""
        print("\n🔍 Checking Django Settings...")
        
        # Check DEBUG setting
        if settings.DEBUG:
            self.log_finding(
                'CRITICAL', 
                'Django Configuration',
                'DEBUG=True in production environment',
                'Set DEBUG=False in production'
            )
        
        # Check SECRET_KEY
        if hasattr(settings, 'SECRET_KEY'):
            if len(settings.SECRET_KEY) < 50:
                self.log_finding(
                    'HIGH',
                    'Django Configuration',
                    'SECRET_KEY is too short (less than 50 characters)',
                    'Generate a longer, more complex SECRET_KEY'
                )
            
            if 'django-insecure' in settings.SECRET_KEY:
                self.log_finding(
                    'HIGH',
                    'Django Configuration',
                    'Using default Django SECRET_KEY',
                    'Generate a unique SECRET_KEY for production'
                )
        
        # Check ALLOWED_HOSTS
        if '*' in settings.ALLOWED_HOSTS and not settings.DEBUG:
            self.log_finding(
                'HIGH',
                'Django Configuration',
                'ALLOWED_HOSTS contains wildcard (*) in production',
                'Specify exact hostnames in ALLOWED_HOSTS'
            )
        
        # Check security middleware
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ]
        
        for middleware in required_middleware:
            if middleware not in settings.MIDDLEWARE:
                self.log_finding(
                    'MEDIUM',
                    'Django Configuration',
                    f'Missing security middleware: {middleware}',
                    f'Add {middleware} to MIDDLEWARE setting'
                )
    
    def check_database_security(self):
        """Check database configuration security"""
        print("\n🔍 Checking Database Security...")
        
        db_config = settings.DATABASES.get('default', {})
        
        # Check for default passwords
        password = db_config.get('PASSWORD', '')
        weak_passwords = ['admin', 'password', '123456', 'root', '']
        
        if password in weak_passwords:
            self.log_finding(
                'CRITICAL',
                'Database Security',
                'Database using weak or default password',
                'Use a strong, unique password for database access'
            )
        
        # Check if database is on default port
        if db_config.get('PORT') == '5432' and db_config.get('HOST') != 'localhost':
            self.log_finding(
                'MEDIUM',
                'Database Security',
                'Database using default PostgreSQL port',
                'Consider using a non-standard port for additional security'
            )
    
    def check_user_permissions(self):
        """Check user and permission configurations"""
        print("\n🔍 Checking User Permissions...")
        
        User = get_user_model()
        
        # Check for users with weak passwords (if we can detect them)
        superusers = User.objects.filter(is_superuser=True)
        
        if superusers.count() == 0:
            self.log_finding(
                'HIGH',
                'User Management',
                'No superuser accounts found',
                'Create at least one superuser account for admin access'
            )
        elif superusers.count() > 5:
            self.log_finding(
                'MEDIUM',
                'User Management',
                f'Too many superuser accounts ({superusers.count()})',
                'Limit the number of superuser accounts to necessary personnel only'
            )
        
        # Check for users with similar usernames and emails
        for user in User.objects.all()[:10]:  # Check first 10 users
            if user.username and user.username.lower() in ['admin', 'administrator', 'root', 'test']:
                self.log_finding(
                    'MEDIUM',
                    'User Management',
                    f'User with predictable username: {user.username}',
                    'Avoid using predictable usernames for admin accounts'
                )
    
    def check_api_endpoints(self):
        """Check API endpoints for security issues"""
        print("\n🔍 Checking API Endpoints...")
        
        test_endpoints = [
            ('/api/v1/products/', 'GET'),
            ('/api/v1/categories/', 'GET'),
            ('/api/v1/orders/', 'GET'),
            ('/api/v1/cart/', 'GET'),
            ('/admin/', 'GET'),
        ]
        
        for endpoint, method in test_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.request(method, url, timeout=5)
                
                # Check for information disclosure
                if response.status_code == 200 and 'orders' in endpoint:
                    self.log_finding(
                        'HIGH',
                        'API Security',
                        f'{endpoint} accessible without authentication',
                        'Require authentication for sensitive endpoints'
                    )
                
                # Check for missing security headers
                security_headers = [
                    'X-Content-Type-Options',
                    'X-Frame-Options',
                    'X-XSS-Protection'
                ]
                
                for header in security_headers:
                    if header not in response.headers:
                        self.log_finding(
                            'LOW',
                            'Security Headers',
                            f'Missing security header: {header} on {endpoint}',
                            f'Add {header} to response headers'
                        )
                
            except requests.exceptions.RequestException as e:
                print(f"Could not test endpoint {endpoint}: {e}")
    
    def check_file_permissions(self):
        """Check file and directory permissions"""
        print("\n🔍 Checking File Permissions...")
        
        sensitive_files = [
            'ecommerce_backend/settings.py',
            'manage.py',
            '.env',
            'requirements.txt'
        ]
        
        for file_path in sensitive_files:
            full_path = project_root / file_path
            if full_path.exists():
                # Check if file is world-readable
                stat_info = full_path.stat()
                permissions = oct(stat_info.st_mode)[-3:]
                
                if permissions[2] in ['4', '5', '6', '7']:  # World-readable
                    self.log_finding(
                        'MEDIUM',
                        'File Permissions',
                        f'{file_path} is world-readable',
                        f'Remove world-read permissions: chmod o-r {file_path}'
                    )
    
    def check_dependency_security(self):
        """Check for known vulnerable dependencies"""
        print("\n🔍 Checking Dependencies...")
        
        requirements_file = project_root / 'requirements.txt'
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                dependencies = f.read()
            
            # Check for known vulnerable packages (simplified check)
            vulnerable_patterns = [
                r'django==.*[12]\.',  # Django 1.x or 2.x
                r'requests==.*1\.',   # Old requests versions
                r'pillow==.*[1-7]\.'  # Old Pillow versions
            ]
            
            for pattern in vulnerable_patterns:
                if re.search(pattern, dependencies):
                    self.log_finding(
                        'HIGH',
                        'Dependency Security',
                        f'Potentially vulnerable dependency found: {pattern}',
                        'Update to the latest stable version'
                    )
    
    def generate_report(self):
        """Generate a comprehensive security report"""
        print("\n" + "="*80)
        print("🛡️  SECURITY AUDIT REPORT")
        print("="*80)
        
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'INFO': 0
        }
        
        for finding in self.findings:
            severity_counts[finding['severity']] += 1
        
        print(f"\n📊 Summary:")
        print(f"   Critical: {severity_counts['CRITICAL']}")
        print(f"   High:     {severity_counts['HIGH']}")
        print(f"   Medium:   {severity_counts['MEDIUM']}")
        print(f"   Low:      {severity_counts['LOW']}")
        print(f"   Info:     {severity_counts['INFO']}")
        print(f"   Total:    {len(self.findings)}")
        
        if severity_counts['CRITICAL'] > 0:
            print("\n🚨 URGENT: Critical security issues found! Address immediately.")
        elif severity_counts['HIGH'] > 0:
            print("\n⚠️  WARNING: High-priority security issues found.")
        else:
            print("\n✅ No critical security issues found.")
        
        # Save detailed report to file
        report_file = project_root / 'security_audit_report.json'
        with open(report_file, 'w') as f:
            json.dump(self.findings, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
    
    def run_audit(self):
        """Run the complete security audit"""
        print("🔒 Starting Security Audit...")
        print("="*50)
        
        self.check_django_settings()
        self.check_database_security()
        self.check_user_permissions()
        self.check_api_endpoints()
        self.check_file_permissions()
        self.check_dependency_security()
        
        self.generate_report()


if __name__ == "__main__":
    audit = SecurityAudit()
    audit.run_audit()
