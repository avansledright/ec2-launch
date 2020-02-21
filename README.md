# ec2-launch
Usage:
Creates an EC2 instance, S3 bucket, Cloudfront distribution and assigns an EIP to the EC2 instance
Simply run python3 main.py. You will be prompted to enter in a customer domain name which will define the S3 Bucket and create a Cloudfront distribution based upon the domain specified.

Modifications Needed:
You will need to add in an AMI, Security Group, Key Pair based on your environment. 

Future plans:
Prompt user for AMI, Security Group and Key Pair. 
Add in CNAME based on Cloudfront distribution something like cdn.CUSTOMERDOMAIN.com
Create options for instance size. Currently it is preset to a T3.Micro
