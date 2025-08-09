# 🔄 EC2 Production Update Guide

## 📋 Overview

This guide shows you how to update your live ALX E-Commerce project on EC2 with zero or minimal downtime.

**Current Production:** https://ecom-backend.store  
**Server:** AWS EC2 Ubuntu (98.87.47.179)  

---

## 🚀 Quick Update Process

### Step 1: SSH to Your EC2 Instance
```bash
ssh -i ecom-backend.pem ubuntu@98.87.47.179
```

### Step 2: Navigate to Project Directory
```bash
cd ~/alx-project-nexus
```

### Step 3: Run the Update Script
```bash
# Use the automated update script
./scripts/update-production.sh
```

**That's it!** The script will:
1. ✅ Pull latest code from GitHub
2. ✅ Stop current containers
3. ✅ Rebuild with new code
4. ✅ Restart services
5. ✅ Verify health

---

## 🔧 Manual Update Process

If you prefer manual control:

### 1. Pull Latest Code
```bash
cd ~/alx-project-nexus
git pull origin main
```

### 2. Stop Current Services
```bash
# Stop all containers
docker compose -f docker-compose.prod.yml down
```

### 3. Rebuild Containers
```bash
# Rebuild with latest code (no cache for fresh build)
docker compose -f docker-compose.prod.yml build --no-cache
```

### 4. Start Updated Services
```bash
# Start all services in detached mode
docker compose -f docker-compose.prod.yml up -d
```

### 5. Verify Update
```bash
# Check container status
docker compose -f docker-compose.prod.yml ps

# Test health endpoint
curl https://ecom-backend.store/health/

# View logs if needed
docker compose -f docker-compose.prod.yml logs -f
```

---

## 🔄 Different Update Scenarios

### Scenario 1: Code Changes Only ⚡
**When:** You updated Python code, templates, or static files  
**Downtime:** ~30 seconds
```bash
./scripts/update-production.sh
```

### Scenario 2: Dependencies Changed 📦
**When:** You updated requirements.txt  
**Downtime:** ~2-3 minutes
```bash
cd ~/alx-project-nexus
git pull origin main
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml build --no-cache  # Important: no-cache
docker compose -f docker-compose.prod.yml up -d
```

### Scenario 3: Database Migrations 🗄️
**When:** You have new Django migrations  
**Downtime:** ~1-2 minutes
```bash
cd ~/alx-project-nexus
git pull origin main
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d db  # Start DB first
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
docker compose -f docker-compose.prod.yml up -d  # Start all services
```

### Scenario 4: Environment Variables 🔧
**When:** You updated .env.prod file  
**Downtime:** ~30 seconds
```bash
# Update .env.prod file first, then:
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

### Scenario 5: Nginx Configuration 🌐
**When:** You updated nginx configuration  
**Downtime:** ~10 seconds
```bash
cd ~/alx-project-nexus
git pull origin main
docker compose -f docker-compose.prod.yml restart nginx
```

---

## 📊 Zero-Downtime Updates

For critical updates with minimal downtime:

### Using Blue-Green Deployment
```bash
# 1. Start new containers with different names
docker compose -f docker-compose.prod.yml -p alx-green up -d

# 2. Wait for health check
sleep 30
curl -f https://ecom-backend.store/health/

# 3. Switch traffic (update nginx upstream)
# 4. Stop old containers
docker compose -f docker-compose.prod.yml -p alx-blue down
```

---

## 🔍 Monitoring During Updates

### Check Container Status
```bash
docker compose -f docker-compose.prod.yml ps
```

### View Real-time Logs  
```bash
docker compose -f docker-compose.prod.yml logs -f
```

### Monitor Specific Service
```bash
# Django app logs
docker compose -f docker-compose.prod.yml logs -f web

# Database logs  
docker compose -f docker-compose.prod.yml logs -f db

# Nginx logs
docker compose -f docker-compose.prod.yml logs -f nginx
```

### Health Check Commands
```bash
# Quick health check
curl https://ecom-backend.store/health/

# Detailed health check
curl https://ecom-backend.store/health/db/
curl https://ecom-backend.store/health/cache/

# Check SSL certificate
curl -I https://ecom-backend.store/
```

---

## 🚨 Rollback Process

If something goes wrong:

### Quick Rollback
```bash
# 1. Go to previous Git commit
cd ~/alx-project-nexus
git log --oneline -5  # See recent commits
git checkout <previous-commit-hash>

# 2. Rebuild and restart
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

### Emergency Rollback
```bash
# If containers won't start, use backup
docker compose -f docker-compose.prod.yml down
docker system prune -f  # Clean up
git checkout HEAD~1     # Go back one commit
./scripts/update-production.sh
```

---

## 📋 Pre-Update Checklist

Before updating production:

- [ ] ✅ **Test locally** - Ensure changes work in development
- [ ] ✅ **Run tests** - All unit tests pass
- [ ] ✅ **Check dependencies** - No breaking changes
- [ ] ✅ **Backup database** - Create backup if needed
- [ ] ✅ **Review changes** - Check git diff
- [ ] ✅ **Plan rollback** - Know how to revert if needed

### Create Database Backup (Optional)
```bash
# Backup current database
docker compose -f docker-compose.prod.yml exec db pg_dump -U postgres ecommerce_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

---

## 🔧 Common Update Issues & Solutions

### Issue 1: Containers Won't Start
```bash
# Solution: Check logs and rebuild
docker compose -f docker-compose.prod.yml logs
docker compose -f docker-compose.prod.yml down
docker system prune -f
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

### Issue 2: Database Connection Errors
```bash
# Solution: Start database first, then migrate
docker compose -f docker-compose.prod.yml up -d db
sleep 10
docker compose -f docker-compose.prod.yml run --rm web python manage.py migrate
docker compose -f docker-compose.prod.yml up -d
```

### Issue 3: Static Files Not Loading
```bash
# Solution: Collect static files
docker compose -f docker-compose.prod.yml run --rm web python manage.py collectstatic --noinput
docker compose -f docker-compose.prod.yml restart nginx
```

### Issue 4: SSL Certificate Problems
```bash
# Solution: Restart nginx and check certificate
docker compose -f docker-compose.prod.yml restart nginx
sudo certbot certificates
```

---

## 📈 Update Best Practices

### 1. **Regular Updates** 🔄
- Update weekly or bi-weekly
- Don't let updates accumulate

### 2. **Test First** 🧪  
- Always test locally before production
- Use staging environment if available

### 3. **Monitor After Update** 📊
- Watch logs for 5-10 minutes after update
- Check error rates and response times

### 4. **Document Changes** 📝
- Keep changelog of what was updated
- Note any manual steps required

### 5. **Backup Strategy** 💾
- Regular database backups
- Keep last working Docker images

---

## 🎯 Quick Commands Reference

```bash
# Update production (automated)
./scripts/update-production.sh

# Manual update steps
git pull origin main
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

# Health checks
curl https://ecom-backend.store/health/
docker compose -f docker-compose.prod.yml ps

# View logs
docker compose -f docker-compose.prod.yml logs -f

# Emergency restart
docker compose -f docker-compose.prod.yml restart
```

---

## 🌐 Post-Update Verification

After any update, verify:

1. **✅ Site loads:** https://ecom-backend.store
2. **✅ Health check:** https://ecom-backend.store/health/  
3. **✅ Admin panel:** https://ecom-backend.store/admin/
4. **✅ API docs:** https://ecom-backend.store/api/v1/docs/
5. **✅ SSL certificate:** Green lock in browser
6. **✅ Key functionality:** Test critical user flows

---

**🎉 Your production updates are now automated and reliable!**

The `update-production.sh` script makes updates simple and consistent. Your ALX E-Commerce platform will stay current with minimal downtime.
