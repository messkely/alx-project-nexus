c# 🛠️ Scripts Directory

This directory contains utility scripts for deployment, database management, and development setup.

## � Current Scripts

### 🚀 Production Deployment
- **`setup-domain-ssl.sh`** - Complete SSL setup with Let's Encrypt for production domain
- **`deploy-ec2-production.sh`** - Production deployment script for EC2
- **`start-ec2-production.sh`** - Start production services on EC2
- **`verify-dns.sh`** - Verify DNS configuration for domain setup

### 🧪 Testing & Monitoring  
- **`test-django-health.sh`** - Test Django health endpoints
- **`test-ec2-connection.sh`** - Test EC2 connectivity and services
- **`debug-ec2.sh`** - Debug EC2 deployment issues

### 🗄️ Database Management
- **`seed_database.py`** - Populate database with sample data
- **`django_seed_script.py`** - Django-based seeding script
- **`seed_data.sql`** - SQL seed data for direct database import

### 🔧 Development Utilities
- **`setup_dev.py`** - Set up development environment
- **`start_production.sh`** - Production startup script

## 📋 Usage Examples

### Production SSL Setup
```bash
sudo ./scripts/setup-domain-ssl.sh
```

### Deploy to EC2 Production
```bash
./scripts/deploy-ec2-production.sh
```

### Seed Database
```bash
python scripts/seed_database.py
```

### Health Check
```bash
./scripts/test-django-health.sh
```

---

**Note:** All scripts are designed to work from the project root directory.

## 📊 Script Features

### Deploy Script Features
- ✅ **Automated Setup**: One-command production deployment
- ✅ **SSL Management**: Automatic Let's Encrypt certificate setup
- ✅ **Health Monitoring**: Service status checks and health monitoring
- ✅ **Backup System**: Automated database backup and restoration
- ✅ **Log Management**: Centralized logging and log viewing
- ✅ **Update Management**: Safe deployment updates

### Seeding Script Features
- ✅ **Complete Data**: Users, categories, products, orders, reviews
- ✅ **Realistic Data**: Real-world e-commerce sample data
- ✅ **Django Integration**: Uses Django ORM and models
- ✅ **Safe Execution**: Checks for existing data before creating
- ✅ **Admin User**: Creates admin user for testing
- ✅ **Test Relationships**: Proper FK relationships and data integrity

## 🛡️ Security Considerations

### Deploy Script Security
- Uses secure environment variable handling
- SSL certificate validation
- Non-root container execution
- Secure database connections

### Seeding Script Security
- Secure password hashing for test users
- Data validation before insertion
- Safe Django ORM operations
- No hardcoded sensitive data

## 📖 Dependencies

All scripts require:
- Django environment properly configured
- Database connection established
- Required Python packages installed
- Appropriate file permissions set

---

**All scripts are production-ready and thoroughly tested.**
