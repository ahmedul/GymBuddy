import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as logs from 'aws-cdk-lib/aws-logs';
import { Construct } from 'constructs';

interface ApiStackProps extends cdk.StackProps {
  vpc: ec2.Vpc;
  securityGroup: ec2.SecurityGroup;
  dbSecret: secretsmanager.Secret;
  dbEndpoint: string;
}

export class ApiStack extends cdk.Stack {
  public readonly apiUrl: string;

  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    // ECR repository for API image
    const repository = new ecr.Repository(this, 'ApiRepository', {
      repositoryName: 'gymbuddy-api',
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      imageScanOnPush: true,
    });

    // ECS Cluster
    const cluster = new ecs.Cluster(this, 'ApiCluster', {
      vpc: props.vpc,
      clusterName: 'gymbuddy-cluster',
      containerInsights: true,
    });

    // Application secret for JWT
    const appSecret = new secretsmanager.Secret(this, 'AppSecret', {
      secretName: 'gymbuddy/app-secret',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({}),
        generateStringKey: 'secret_key',
        excludePunctuation: true,
        passwordLength: 64,
      },
    });

    // Fargate service with ALB
    const fargateService = new ecsPatterns.ApplicationLoadBalancedFargateService(
      this,
      'ApiService',
      {
        cluster,
        serviceName: 'gymbuddy-api',
        cpu: 256,
        memoryLimitMiB: 512,
        desiredCount: 1,
        taskImageOptions: {
          image: ecs.ContainerImage.fromEcrRepository(repository, 'latest'),
          containerPort: 8000,
          environment: {
            ENVIRONMENT: 'production',
            DEBUG: 'false',
            DATABASE_URL: `postgresql+asyncpg://gymbuddy_admin:PLACEHOLDER@${props.dbEndpoint}:5432/gymbuddy`,
          },
          secrets: {
            SECRET_KEY: ecs.Secret.fromSecretsManager(appSecret, 'secret_key'),
            DB_PASSWORD: ecs.Secret.fromSecretsManager(props.dbSecret, 'password'),
          },
          logDriver: ecs.LogDrivers.awsLogs({
            streamPrefix: 'gymbuddy-api',
            logRetention: logs.RetentionDays.ONE_MONTH,
          }),
        },
        publicLoadBalancer: true,
        securityGroups: [props.securityGroup],
        assignPublicIp: false,
        healthCheckGracePeriod: cdk.Duration.seconds(60),
      }
    );

    // Configure health check
    fargateService.targetGroup.configureHealthCheck({
      path: '/health',
      healthyHttpCodes: '200',
      interval: cdk.Duration.seconds(30),
      timeout: cdk.Duration.seconds(10),
      healthyThresholdCount: 2,
      unhealthyThresholdCount: 3,
    });

    // Auto-scaling
    const scaling = fargateService.service.autoScaleTaskCount({
      minCapacity: 1,
      maxCapacity: 4,
    });

    scaling.scaleOnCpuUtilization('CpuScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    scaling.scaleOnMemoryUtilization('MemoryScaling', {
      targetUtilizationPercent: 70,
      scaleInCooldown: cdk.Duration.seconds(60),
      scaleOutCooldown: cdk.Duration.seconds(60),
    });

    this.apiUrl = fargateService.loadBalancer.loadBalancerDnsName;

    // Outputs
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: `http://${this.apiUrl}`,
      description: 'API URL',
    });

    new cdk.CfnOutput(this, 'EcrRepositoryUri', {
      value: repository.repositoryUri,
      description: 'ECR repository URI for pushing images',
    });
  }
}
