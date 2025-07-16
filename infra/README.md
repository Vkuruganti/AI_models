# Infrastructure Deployment

## Prerequisites
- Terraform installed
- AWS CLI configured

## Steps
1. Update subnet and security group IDs in `main.tf`.
2. Place your Lambda deployment package (`lambda_app.zip`) in the root directory.
3. Run:
   ```
   terraform init
   terraform apply
   ```
4. Note the outputs for API Gateway and MSK endpoints. 