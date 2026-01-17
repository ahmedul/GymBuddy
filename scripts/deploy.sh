#!/bin/bash
set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPO_NAME="gymbuddy-api"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME"

echo "🚀 GymBuddy Deployment Script"
echo "=============================="
echo "AWS Account: $AWS_ACCOUNT_ID"
echo "Region: $AWS_REGION"
echo "ECR URI: $ECR_URI"
echo ""

# Step 1: Deploy infrastructure
echo "📦 Step 1: Deploying AWS infrastructure..."
cd infra
npm install
npm run cdk deploy -- --all --require-approval never
cd ..

# Step 2: Build and push Docker image
echo "🐳 Step 2: Building and pushing Docker image..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

cd backend
docker build -t $ECR_REPO_NAME:latest .
docker tag $ECR_REPO_NAME:latest $ECR_URI:latest
docker push $ECR_URI:latest
cd ..

# Step 3: Update ECS service
echo "🔄 Step 3: Updating ECS service..."
aws ecs update-service \
  --cluster gymbuddy-cluster \
  --service gymbuddy-api \
  --force-new-deployment \
  --region $AWS_REGION

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📱 Next steps for mobile app:"
echo "1. Update mobile/src/config/index.ts with the API URL"
echo "2. Run: cd mobile && npm install && npx expo start"
