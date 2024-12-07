# Music Festival Performance Tracking System

## Project Overview

This serverless application provides a robust solution for event planning companies to efficiently manage and query music festival performance data. By leveraging AWS services, the system automatically processes CSV files containing performance details and populates a DynamoDB database for easy retrieval and analysis.

## System Architecture

### Services Used
- **AWS S3**: File storage for CSV uploads
- **AWS Lambda**: Serverless compute to process CSV files
- **AWS DynamoDB**: NoSQL database for performance data
- **AWS SNS**: Notification service for processing status

## DynamoDB Schema Design

### Table: Performances
- **Partition Key (Hash Key)**: `stage` (String)
- **Sort Key (Range Key)**: `date#start` (String)

### Rationale for Schema Design
1. **Efficient Querying**: 
   - Partition key (stage) allows fast retrieval of performances by stage
   - Composite sort key (date#start) enables time-based queries
   - Supports quick lookups like:
     * All performances on a specific stage
     * Performances within a given date and time range

### Supported Queries
- Retrieve all performances by a specific performer
- List performances within a given time range
- Fetch performance details for a specific stage and time

## Cost and Scalability Analysis

### Infrastructure Cost Estimation

#### Daily Record Processing
| Record Volume | Estimated Monthly Cost |
|--------------|------------------------|
| 1,000 records | $1.50 - $3.00 |
| 10,000 records | $5.00 - $10.00 |
| 100,000 records | $20.00 - $40.00 |

### Scalability Strategies
- **DynamoDB**: Pay-per-request billing model
- **Lambda**: Automatically scales with incoming requests
- **S3**: Virtually unlimited storage
- Minimal operational overhead

## Security Considerations

### IAM Roles and Permissions
- Implemented least privilege access
- Separate roles for Lambda execution
- Restricted permissions for S3, DynamoDB, and SNS interactions

## Setup and Deployment

### Prerequisites
- AWS Account
- AWS CLI configured
- Python 3.10
- Boto3 library

### Deployment Steps
1. Create S3 bucket
2. Set up DynamoDB table
3. Configure Lambda function
4. Create SNS topic
5. Set up S3 event notifications

## Sample CSV Format
```csv
Performer,Stage,Start,End,Date
Megan Thee Stallion,Main Stage,8:00,10:00,2025-07-12
Olivia Rodrigo,Side Stage,7:00,9:00,2025-07-12
```

## Potential Improvements
- Add data validation
- Implement more complex querying mechanisms
- Create a front-end dashboard for data visualization

## Troubleshooting
- Check CloudWatch logs for Lambda errors
- Verify IAM role permissions
- Ensure correct environment variables
