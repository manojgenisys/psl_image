import boto3

# Create a session using the default AWS credentials and configuration
session = boto3.Session()

# Retrieve the current region
current_region = session.region_name

# Print the current region
print("Current region:", current_region)