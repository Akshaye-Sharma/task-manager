#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <EC2-IP>"
  exit 1
fi

EC2_IP="$1"
KEY_PATH="$HOME/.ssh/MyTMKeyPair.pem"

echo "Deploying to IP: $EC2_IP"

ssh -i "$KEY_PATH" ubuntu@"$EC2_IP" "rm -rf ~/TaskManager"

echo "Copying files with rsync..."
rsync -avz -e "ssh -i $KEY_PATH" --filter='merge .scpignore' ./ ubuntu@"$EC2_IP":~/TaskManager/
scp -i "$KEY_PATH" ./.env ubuntu@"$EC2_IP":~/TaskManager/

echo "✅ Deployment complete!"

