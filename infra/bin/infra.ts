#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { NetworkStack } from '../lib/network-stack';
import { DatabaseStack } from '../lib/database-stack';
import { ApiStack } from '../lib/api-stack';

const app = new cdk.App();

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION || 'us-east-1',
};

// Network infrastructure (VPC, subnets, security groups)
const networkStack = new NetworkStack(app, 'GymBuddyNetwork', { env });

// Database (RDS PostgreSQL)
const databaseStack = new DatabaseStack(app, 'GymBuddyDatabase', {
  env,
  vpc: networkStack.vpc,
  securityGroup: networkStack.dbSecurityGroup,
});

// API (ECS Fargate + ALB)
const apiStack = new ApiStack(app, 'GymBuddyApi', {
  env,
  vpc: networkStack.vpc,
  securityGroup: networkStack.apiSecurityGroup,
  dbSecret: databaseStack.dbSecret,
  dbEndpoint: databaseStack.dbEndpoint,
});

// Add dependencies
databaseStack.addDependency(networkStack);
apiStack.addDependency(databaseStack);

app.synth();
