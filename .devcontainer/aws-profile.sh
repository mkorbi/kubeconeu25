#!/bin/bash

# This script creates an AWS profile configuration file using GitHub environment variables

# Check if the required environment variables are set
if [ -z "$AWS_ACCESS_KEY_ID" ]; then
  echo "Error: AWS_ACCESS_KEY_ID environment variable is not set"
  exit 1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "Error: AWS_SECRET_ACCESS_KEY environment variable is not set"
  exit 1
fi

# Default profile name and region
PROFILE_NAME=${AWS_PROFILE_NAME:-"default"}
AWS_REGION=${AWS_REGION:-"eu-north-1"}

# Ensure AWS config directory exists
AWS_CONFIG_DIR="$HOME/.aws"
mkdir -p "$AWS_CONFIG_DIR"

# Create credentials file
CREDENTIALS_FILE="$AWS_CONFIG_DIR/credentials"
echo "Creating AWS credentials file at $CREDENTIALS_FILE"

# Check if the file exists and if the profile already exists
if [ -f "$CREDENTIALS_FILE" ] && grep -q "\[$PROFILE_NAME\]" "$CREDENTIALS_FILE"; then
  # Profile exists, update it
  echo "Profile $PROFILE_NAME already exists, updating..."
  
  # Create a temporary file
  TEMP_FILE=$(mktemp)
  
  # Filter out the existing profile section
  awk -v profile="[$PROFILE_NAME]" '
    BEGIN { skip=0; }
    $0 ~ "^"profile"$" { skip=1; next; }
    /^\[/ { if (skip) skip=0; }
    !skip { print; }
  ' "$CREDENTIALS_FILE" > "$TEMP_FILE"
  
  # Append the new profile configuration
  echo "[$PROFILE_NAME]" >> "$TEMP_FILE"
  echo "aws_access_key_id = $AWS_ACCESS_KEY_ID" >> "$TEMP_FILE"
  echo "aws_secret_access_key = $AWS_SECRET_ACCESS_KEY" >> "$TEMP_FILE"
  
  # Replace the original file
  mv "$TEMP_FILE" "$CREDENTIALS_FILE"
else
  # Profile doesn't exist, append it
  echo "[$PROFILE_NAME]" >> "$CREDENTIALS_FILE"
  echo "aws_access_key_id = $AWS_ACCESS_KEY_ID" >> "$CREDENTIALS_FILE"
  echo "aws_secret_access_key = $AWS_SECRET_ACCESS_KEY" >> "$CREDENTIALS_FILE"
fi

# Set proper permissions for credentials file
chmod 600 "$CREDENTIALS_FILE"

# Create config file if it doesn't exist
CONFIG_FILE="$AWS_CONFIG_DIR/config"
echo "Creating/updating AWS config file at $CONFIG_FILE"

if [ -f "$CONFIG_FILE" ] && grep -q "\[profile $PROFILE_NAME\]" "$CONFIG_FILE"; then
  # Profile exists, update it
  echo "Config profile $PROFILE_NAME already exists, updating..."
  
  # Create a temporary file
  TEMP_FILE=$(mktemp)
  
  # Filter out the existing profile section
  awk -v profile="[profile $PROFILE_NAME]" '
    BEGIN { skip=0; }
    $0 ~ "^"profile"$" { skip=1; next; }
    /^\[/ { if (skip) skip=0; }
    !skip { print; }
  ' "$CONFIG_FILE" > "$TEMP_FILE"
  
  # Append the new profile configuration
  echo "[profile $PROFILE_NAME]" >> "$TEMP_FILE"
  echo "region = $AWS_REGION" >> "$TEMP_FILE"
  
  # Replace the original file
  mv "$TEMP_FILE" "$CONFIG_FILE"
else
  # Profile doesn't exist, append it
  echo "[profile $PROFILE_NAME]" >> "$CONFIG_FILE"
  echo "region = $AWS_REGION" >> "$CONFIG_FILE"
fi

# Set proper permissions for config file
chmod 600 "$CONFIG_FILE"

echo "AWS profile $PROFILE_NAME has been configured successfully"
echo "Access Key ID: ${AWS_ACCESS_KEY_ID:0:5}... (hidden for security)"
echo "Secret Access Key: (hidden for security)"
echo "Region: $AWS_REGION"