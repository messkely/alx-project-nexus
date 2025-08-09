#!/bin/bash
# Fix AWS Security Group for HTTPS access
# This script adds port 443 (HTTPS) to the EC2 instance security group

set -e

EC2_IP="98.87.47.179"

echo "🔍 Finding EC2 instance and security group for IP: $EC2_IP"

# Get instance ID from public IP
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=ip-address,Values=$EC2_IP" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "❌ Could not find EC2 instance with IP $EC2_IP"
    echo "💡 Make sure you have AWS CLI configured with proper credentials"
    exit 1
fi

echo "✅ Found instance: $INSTANCE_ID"

# Get security group ID
SECURITY_GROUP_ID=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[*].Instances[*].SecurityGroups[*].GroupId' \
    --output text)

echo "✅ Found security group: $SECURITY_GROUP_ID"

# Check if HTTPS rule already exists
EXISTING_RULE=$(aws ec2 describe-security-groups \
    --group-ids $SECURITY_GROUP_ID \
    --query "SecurityGroups[*].IpPermissions[?FromPort==\`443\` && ToPort==\`443\`]" \
    --output text)

if [ ! -z "$EXISTING_RULE" ]; then
    echo "✅ HTTPS rule (port 443) already exists in security group"
    echo "🤔 The issue might be elsewhere. Check your domain DNS settings."
    exit 0
fi

echo "🔧 Adding HTTPS rule (port 443) to security group..."

# Add HTTPS rule
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0 \
    --tag-specifications "ResourceType=security-group-rule,Tags=[{Key=Name,Value=ALX-ECommerce-HTTPS},{Key=Purpose,Value=Allow HTTPS traffic for ALX E-Commerce Backend}]"

echo "✅ Successfully added HTTPS rule to security group $SECURITY_GROUP_ID"
echo "🚀 Your site should now be accessible at: https://ecom-backend.store"
echo ""
echo "🧪 Testing connection in 5 seconds..."
sleep 5

curl -I https://ecom-backend.store/health/ && echo "🎉 SUCCESS! HTTPS is working!" || echo "⚠️ Still having issues. Please check AWS Console."
