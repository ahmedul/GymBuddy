# 🚀 Deployment Guide

> Guide for deploying GymBuddy to production using AWS.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [AWS CDK Deployment](#aws-cdk-deployment)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring](#monitoring)

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Node.js 18+
- Docker

```bash
# Install AWS CDK
npm install -g aws-cdk

# Verify installation
cdk --version
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AWS CLOUD                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────┐                                               │
│   │   Route 53      │  DNS                                          │
│   └────────┬────────┘                                               │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                               │
│   │   CloudFront    │  CDN (optional)                               │
│   └────────┬────────┘                                               │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────┐                                               │
│   │      ALB        │  Application Load Balancer                    │
│   │  (SSL/HTTPS)    │                                               │
│   └────────┬────────┘                                               │
│            │                                                         │
│            ▼                                                         │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │                    VPC (Private Subnets)                     │   │
│   │  ┌─────────────────────────────────────────────────────┐    │   │
│   │  │              ECS Fargate Cluster                     │    │   │
│   │  │                                                      │    │   │
│   │  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │    │   │
│   │  │  │ Task 1  │  │ Task 2  │  │ Task 3  │   Auto-scale│    │   │
│   │  │  │ FastAPI │  │ FastAPI │  │ FastAPI │             │    │   │
│   │  │  └─────────┘  └─────────┘  └─────────┘             │    │   │
│   │  └──────────────────────┬───────────────────────────────┘    │   │
│   │                         │                                     │   │
│   │                         ▼                                     │   │
│   │  ┌─────────────────────────────────────────────────────┐    │   │
│   │  │              Amazon RDS PostgreSQL                   │    │   │
│   │  │              (Multi-AZ, Encrypted)                   │    │   │
│   │  └─────────────────────────────────────────────────────┘    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│   │    ECR      │  │  Secrets    │  │ CloudWatch  │                │
│   │  (Images)   │  │  Manager    │  │   (Logs)    │                │
│   └─────────────┘  └─────────────┘  └─────────────┘                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## AWS CDK Deployment

### 1. Configure CDK

```bash
cd infra

# Install dependencies
npm install

# Bootstrap CDK (first time only)
cdk bootstrap aws://ACCOUNT_ID/REGION
```

### 2. Update Configuration

Edit `lib/api-stack.ts` with your settings:

```typescript
// Environment variables
const environment = {
  DATABASE_URL: dbSecret.secretArn,
  JWT_SECRET_KEY: jwtSecret.secretArn,
  ENVIRONMENT: 'production',
};
```

### 3. Deploy Stacks

```bash
# Deploy network infrastructure
cdk deploy NetworkStack

# Deploy database
cdk deploy DatabaseStack

# Deploy API
cdk deploy ApiStack

# Or deploy all at once
cdk deploy --all
```

### 4. Verify Deployment

```bash
# Get API URL
aws cloudformation describe-stacks \
  --stack-name ApiStack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text

# Test health endpoint
curl https://api.gymbuddy.app/health
```

---

## Database Setup

### Run Migrations

```bash
# Connect to ECS task
aws ecs execute-command \
  --cluster gymbuddy-cluster \
  --task <task-id> \
  --container api \
  --interactive \
  --command "/bin/bash"

# Inside container
alembic upgrade head
```

### Database Backups

RDS automated backups are configured:
- Retention: 7 days
- Backup window: 03:00-04:00 UTC
- Multi-AZ enabled

---

## Environment Variables

### Required Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `DATABASE_URL` | PostgreSQL connection | Secrets Manager |
| `JWT_SECRET_KEY` | Token signing key | Secrets Manager |
| `JWT_ALGORITHM` | HS256 | Task definition |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 | Task definition |

### Setting Secrets

```bash
# Create database secret
aws secretsmanager create-secret \
  --name gymbuddy/database-url \
  --secret-string "postgresql+asyncpg://user:pass@host:5432/gymbuddy"

# Create JWT secret
aws secretsmanager create-secret \
  --name gymbuddy/jwt-secret \
  --secret-string "your-super-secret-key-here"
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run tests
        run: |
          docker compose up -d db
          docker compose run api pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push
        run: |
          docker build -t gymbuddy-api backend/
          docker tag gymbuddy-api:latest $ECR_REGISTRY/gymbuddy-api:${{ github.sha }}
          docker push $ECR_REGISTRY/gymbuddy-api:${{ github.sha }}

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster gymbuddy-cluster \
            --service gymbuddy-api \
            --force-new-deployment
```

---

## Monitoring

### CloudWatch Logs

```bash
# View API logs
aws logs tail /ecs/gymbuddy-api --follow

# Search for errors
aws logs filter-log-events \
  --log-group-name /ecs/gymbuddy-api \
  --filter-pattern "ERROR"
```

### CloudWatch Alarms

Configured alarms:
- CPU > 80% for 5 minutes
- Memory > 80% for 5 minutes
- 5xx errors > 10 per minute
- Response time > 500ms

### Health Checks

```bash
# API health
curl https://api.gymbuddy.app/health

# Database connectivity (via API)
curl https://api.gymbuddy.app/health/db
```

---

## Scaling

### Auto Scaling Configuration

```typescript
// ECS Service Auto Scaling
const scaling = service.autoScaleTaskCount({
  minCapacity: 2,
  maxCapacity: 10,
});

scaling.scaleOnCpuUtilization('CpuScaling', {
  targetUtilizationPercent: 70,
});

scaling.scaleOnMemoryUtilization('MemoryScaling', {
  targetUtilizationPercent: 70,
});
```

### Manual Scaling

```bash
# Scale to 5 tasks
aws ecs update-service \
  --cluster gymbuddy-cluster \
  --service gymbuddy-api \
  --desired-count 5
```

---

## Rollback

### Quick Rollback

```bash
# Get previous task definition
aws ecs list-task-definitions \
  --family gymbuddy-api \
  --sort DESC

# Rollback to previous version
aws ecs update-service \
  --cluster gymbuddy-cluster \
  --service gymbuddy-api \
  --task-definition gymbuddy-api:PREVIOUS_VERSION
```

---

## Cost Optimization

| Resource | Monthly Estimate |
|----------|------------------|
| ECS Fargate (2 tasks) | ~$50 |
| RDS PostgreSQL (db.t3.micro) | ~$15 |
| ALB | ~$20 |
| Data Transfer | ~$10 |
| **Total** | **~$95/month** |

### Cost Saving Tips

1. Use Fargate Spot for non-production
2. Right-size RDS instance
3. Enable auto-scaling
4. Use Reserved Instances for steady workloads

---

<p align="center">
  <a href="README.md">← Back to README</a>
</p>
