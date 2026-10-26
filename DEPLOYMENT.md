# 🚀 Deployment Guide - AWS EC2 with Docker

This guide will help you deploy your Resume Tailor application to AWS EC2 using Docker.

## 📋 Prerequisites

- AWS Account (Free tier eligible)
- Basic knowledge of AWS EC2
- SSH key pair for EC2 access

## 🎯 Why AWS EC2?

- ✅ **Free Tier**: 750 hours/month for 12 months
- ✅ **Full Control**: Complete server access
- ✅ **LaTeX Support**: Can install TeX Live
- ✅ **Scalable**: Easy to upgrade resources
- ✅ **Docker Ready**: Perfect for containerized apps

## 🏗️ Step-by-Step Deployment

### Step 1: Launch EC2 Instance

1. **Go to AWS Console** → EC2 → Launch Instance
2. **Choose Configuration**:
   - **Name**: `resume-tailor-app`
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: `t2.micro` (Free tier)
   - **Key Pair**: Create or select existing SSH key
   - **Security Group**: Create new with these rules:
     ```
     SSH (22): 0.0.0.0/0
     HTTP (80): 0.0.0.0/0
     Custom TCP (5000): 0.0.0.0/0
     ```

### Step 2: Connect to Instance

```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-public-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y
```

### Step 3: Clone Your Repository

```bash
# Install Git
sudo apt-get install git -y

# Clone your repository
git clone https://github.com/FuriousApe/resume-tailor.git
cd resume-tailor
```

### Step 4: Run Deployment Script

```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Step 5: Configure Environment Variables

Edit the `.env` file with your API keys:

```bash
nano .env
```

```env
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key
OPENROUTER_API_KEY=your_openrouter_key_here
CEREBRAS_API_KEY=your_cerebras_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### Step 6: Restart Application

```bash
# Restart with new environment
docker-compose down
docker-compose up -d
```

## 🔧 Alternative Deployment Methods

### Method 1: Manual Docker Setup

```bash
# Install Docker manually
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Build and run
docker-compose build
docker-compose up -d
```

### Method 2: Direct Installation (No Docker)

```bash
# Install system dependencies
sudo apt-get install python3 python3-pip texlive-full -y

# Install Python dependencies
pip3 install -r requirements.txt

# Run application
python3 app.py
```

## 🌐 Access Your Application

- **Local**: http://localhost:5000
- **Public**: http://your-ec2-public-ip:5000

## 🔒 Security Considerations

### 1. Update Security Group
```bash
# Only allow your IP for SSH
# Allow HTTP/HTTPS for web access
# Consider using Application Load Balancer for HTTPS
```

### 2. Set Up Domain (Optional)
- Register domain (e.g., resume-tailor.com)
- Point to EC2 public IP
- Set up SSL certificate

### 3. Environment Variables
```bash
# Never commit API keys to Git
# Use AWS Systems Manager Parameter Store for production
aws ssm put-parameter --name "/resume-tailor/openrouter-key" --value "your-key" --type "SecureString"
```

## 📊 Monitoring and Maintenance

### View Logs
```bash
# Docker logs
docker-compose logs -f

# System logs
sudo journalctl -u docker
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Backup Strategy
```bash
# Backup application data
tar -czf backup-$(date +%Y%m%d).tar.gz /opt/resume-tailor

# Backup to S3
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
```

## 💰 Cost Optimization

### Free Tier Usage
- **EC2**: 750 hours/month (t2.micro)
- **EBS**: 30 GB storage
- **Data Transfer**: 15 GB outbound

### Cost Monitoring
```bash
# Set up billing alerts in AWS Console
# Monitor usage with AWS Cost Explorer
# Use AWS Budgets for spending limits
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 5000 not accessible**:
   ```bash
   # Check security group rules
   # Verify application is running
   docker-compose ps
   ```

2. **LaTeX compilation fails**:
   ```bash
   # Check TeX Live installation
   which pdflatex
   # Rebuild Docker image
   docker-compose build --no-cache
   ```

3. **Memory issues**:
   ```bash
   # Monitor memory usage
   free -h
   # Consider upgrading to t3.small
   ```

### Useful Commands

```bash
# Check application status
docker-compose ps

# View logs
docker-compose logs -f resume-tailor

# Restart application
docker-compose restart

# Check system resources
htop
df -h
free -h
```

## 🔄 CI/CD Pipeline (Optional)

### GitHub Actions Setup

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to EC2

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_KEY }}
          script: |
            cd resume-tailor
            git pull origin main
            docker-compose down
            docker-compose up -d --build
```

## 🎉 Success!

Your Resume Tailor application is now deployed and accessible worldwide! 

**Next Steps**:
1. Set up monitoring and alerts
2. Configure domain and SSL
3. Set up automated backups
4. Monitor costs and usage

## 📞 Support

- **GitHub Issues**: Report bugs and feature requests
- **AWS Support**: For infrastructure issues
- **Documentation**: Check README.md for usage 