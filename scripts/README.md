# Scripts Directory

This directory contains all automation and seeding scripts for the ALX E-Commerce Backend project.

## 📋 Scripts Overview

### ☁️ EC2 Ubuntu Deployment Script
- **`deploy-ec2.sh`** - AWS EC2 Ubuntu deployment automation
  - Initialize production environment on EC2
  - Setup Nginx, Gunicorn, PostgreSQL, Redis
  - SSL certificate management with Let's Encrypt
  - Security hardening and monitoring setup  
  - Usage: `./scripts/deploy-ec2.sh [command]`

### 🌱 Database Seeding Scripts
- **`seed_database.py`** - Comprehensive database seeding
  - Creates sample users, products, categories, orders, reviews
  - Uses Django ORM for data creation
  - Realistic e-commerce data for testing
  - Usage: `python scripts/seed_database.py`

- **`django_seed_script.py`** - Django shell seeding script
  - Alternative seeding method using Django shell
  - Same data as seed_database.py but shell-based
  - Usage: `python manage.py shell < scripts/django_seed_script.py`

## 🔧 Usage Instructions

### EC2 Ubuntu Deployment
```bash
# Make deployment script executable
chmod +x scripts/deploy-ec2.sh

# Deploy to EC2 Ubuntu instance
sudo ./scripts/deploy-ec2.sh init

# Update existing deployment
./scripts/deploy-ec2.sh update

# Check deployment status
./scripts/deploy-ec2.sh status
./scripts/deploy.sh status

# Create backup
./scripts/deploy.sh backup

# View logs
./scripts/deploy.sh logs
```

### Database Seeding
```bash
# Method 1: Direct Python execution (recommended)
python scripts/seed_database.py

# Method 2: Django shell execution
python manage.py shell < scripts/django_seed_script.py
```

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
