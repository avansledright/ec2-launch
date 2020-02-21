import boto3
import time
from botocore.exceptions import ClientError

CustomerName = input('Customer Domain Name: ')

ec2 = boto3.resource('ec2')
ip = boto3.client('ec2')
cf = boto3.client('cloudfront')
s3 = boto3.client('s3')

def createInstance():
    #create the instance
    instances = ec2.create_instances(
        ImageId='ami-##############',
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName='###########',
        SecurityGroupIds= ['sg-##########'],
    )
    # Get the Instance ID
    for instance in instances:
        print(instance.id, instance.instance_type)
        print('Instance is not running... Please wait')
        instance.wait_until_running(InstanceIds=[instance.id])
        try:
            allocation = ip.allocate_address(Domain='vpc')
            response = ip.associate_address(AllocationId=allocation['AllocationId'], InstanceId=instance.id)
            print(response)
        except ClientError as e:
            print(e)
createInstance()

## Create S3 Bucket
def createS3Bucket():
    s3.create_bucket(Bucket=CustomerName, CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})
createS3Bucket()

## Create CloudFront Distribution
def createCloudFront():
    cf.create_distribution(DistributionConfig=dict(CallerReference='firstOne',
                DefaultRootObject='index.html',
                Comment=CustomerName + 'Distribution',
                Enabled=True,
                Origins = dict(
                    Quantity = 1, 
                    Items = [dict(
                        Id = '1',
                        DomainName=CustomerName+'.s3.amazonaws.com',
                        S3OriginConfig = dict(OriginAccessIdentity = ''))
                    ]),
                DefaultCacheBehavior = dict(
                    TargetOriginId = '1',
                    ViewerProtocolPolicy= 'redirect-to-https',
                    TrustedSigners = dict(Quantity=0, Enabled=False),
                    ForwardedValues=dict(
                        Cookies = {'Forward':'all'},
                        Headers = dict(Quantity=0),
                        QueryString=False,
                        QueryStringCacheKeys= dict(Quantity=0),
                        ),
                    MinTTL=1000)
                )
    )
createCloudFront()