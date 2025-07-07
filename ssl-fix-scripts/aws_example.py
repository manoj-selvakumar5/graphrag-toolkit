"""
Example of using ssl_helper for AWS operations
This demonstrates the proper way to create AWS clients with SSL certificate verification
"""
from ssl_helper import create_aws_client, setup_ssl_for_aws
import json

# Setup SSL certificates first
setup_ssl_for_aws()

# Example 1: Create IAM client with proper SSL verification
def create_iam_role_example():
    """Example of creating an IAM role with proper SSL configuration"""
    APPLICATION_ID = "graphrag-toolkit-example"
    role_name = f"GraphRAGRole-{APPLICATION_ID}"
    
    # Use the ssl_helper to create the client
    iam = create_aws_client('iam')
    
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                        "bedrock.amazonaws.com",
                        "opensearch.amazonaws.com"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description=f"Role for GraphRAG toolkit {APPLICATION_ID}"
        )
        print(f"✅ IAM role created: {role_name}")
        return role_response
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"ℹ️ IAM role already exists: {role_name}")
        return iam.get_role(RoleName=role_name)
    except Exception as e:
        print(f"❌ Failed to create IAM role: {e}")
        return None

# Example 2: List S3 buckets
def list_s3_buckets_example():
    """Example of listing S3 buckets with proper SSL configuration"""
    s3 = create_aws_client('s3')
    
    try:
        response = s3.list_buckets()
        print("✅ S3 buckets:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
        return response
    except Exception as e:
        print(f"❌ Failed to list S3 buckets: {e}")
        return None

if __name__ == "__main__":
    print("Testing AWS operations with SSL helper...")
    print("\n1. Testing IAM role creation:")
    create_iam_role_example()
    
    print("\n2. Testing S3 bucket listing:")
    list_s3_buckets_example()
