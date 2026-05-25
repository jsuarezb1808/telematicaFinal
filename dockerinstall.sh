#!/bin/bash

# 1. Ensure the script is run with sudo privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo: sudo ./install-docker.sh"
  exit 1
fi

echo "Starting Docker installation..."

# 2. Detect the operating system
source /etc/os-release

if [[ "$ID" == "amzn" ]]; then
    echo "Detected Amazon Linux. Installing Docker..."
    
    # Update packages and install Docker
    yum update -y
    yum install -y docker
    
elif [[ "$ID" == "ubuntu" || "$ID" == "debian" ]]; then
    echo "Detected Ubuntu/Debian. Installing Docker via the official convenience script..."
    
    # Update packages and install prerequisites
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release
    
    # Download and run the official Docker installation script
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
else
    echo "Unsupported OS: $ID. Falling back to the official Docker convenience script..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

    sudo docker run hello-world
