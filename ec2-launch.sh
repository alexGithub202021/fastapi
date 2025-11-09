#!/bin/bash
set -e  # Exit on any error

# -------- Required environment variables --------
: "${AWS_ACCESS_KEY_ID:?Need AWS_ACCESS_KEY_ID}"
: "${AWS_SECRET_ACCESS_KEY:?Need AWS_SECRET_ACCESS_KEY}"
: "${AWS_DEFAULT_REGION:?Need AWS_DEFAULT_REGION}"
: "${AMI_ID:?Need AMI_ID}"
: "${KEY_NAME:?Need KEY_NAME}"
: "${SECURITY_GROUP_ID:?Need SECURITY_GROUP_ID}"
: "${INSTANCE_TYPE:?Need INSTANCE_TYPE}"
: "${INSTANCE_NAME:?Need INSTANCE_NAME}"

# -------- Clean & Validate AMI ID --------
# Remove spaces
AMI_ID=$(echo "$AMI_ID" | tr -d '[:space:]')

# Ensure lowercase letters
AMI_ID=$(echo "$AMI_ID" | tr '[:upper:]' '[:lower:]')

# Validate format
if [[ ! $AMI_ID =~ ^ami-[0-9a-f]{8}([0-9a-f]{9})?$ ]]; then
    echo "❌ Invalid AMI format: $AMI_ID"
    exit 1
fi

# Check AMI exists
if ! aws ec2 describe-images --image-ids "$AMI_ID" >/dev/null 2>&1; then
    echo "❌ AMI does not exist in this region: $AMI_ID"
    exit 1
fi

# -------- Launch Instance --------
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SECURITY_GROUP_ID" \
  # ${SUBNET_ID:+--subnet-id "$SUBNET_ID"} \
  --associate-public-ip-address \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
  --query 'Instances[0].InstanceId' \
  --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "❌ Instance launch failed."
    exit 1
fi

echo "✅ Instance launched: $INSTANCE_ID"

# -------- Wait until running --------
echo "Waiting for instance to reach 'running' state..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# -------- Get Public IP --------
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "✅ Instance is running."
echo "🌐 Public IP: $PUBLIC_IP"
echo "🧩 Connect via: ssh -i ~/.ssh/${KEY_NAME}.pem ec2-user@${PUBLIC_IP}"
