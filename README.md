 Smart File Archiver – Intelligent S3 Cost Optimizer

This AWS Lambda-based automation project scans files in an S3 bucket, deletes unwanted ones, and tags valid files for cost-based archival to Glacier/Deep Glacier.

 Features
- Deletes empty and corrupted files
- Tags usable files for lifecycle transitions
- Lifecycle rules: Glacier (30d), Deep Glacier (120d)
- Sends email reports using AWS SES
- CloudWatch logs for monitoring

Tech Stack
- AWS S3, Lambda, CloudWatch, SES
- Python 3.13

Architecture Diagram
![Architecture](C:\Users\Nitro v\Desktop\AWS PROJEC)

Setup
1. Upload `lambda_function.py` to AWS Lambda
2. Grant Lambda S3 & SES permissions
3. Configure S3 bucket + lifecycle rules
4. (Optional) Schedule via EventBridge

Email Output
Email sent via SES with file cleanup stats.
