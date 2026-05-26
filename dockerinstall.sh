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
    yum update -y
    yum install -y docker
    
elif [[ "$ID" == "ubuntu" || "$ID" == "debian" ]]; then
    echo "Detected Ubuntu/Debian. Installing Docker via the official convenience script..."
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release
    
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
else
    echo "Unsupported OS: $ID. Falling back to the official Docker convenience script..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

# 3. Start and enable the Docker service so it runs on boot
echo "Starting Docker service..."
systemctl start docker
systemctl enable docker

# 4. Install Docker Compose
echo "Installing the latest version of Docker Compose..."
# Fetch the latest version tag from GitHub
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)

# Download the binary for the correct architecture (works for both x86_64 and AWS Graviton/ARM)
curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create a symlink so it also works as a Docker CLI plugin (docker compose)
mkdir -p /usr/local/lib/docker/cli-plugins
ln -sf /usr/local/bin/docker-compose /usr/local/lib/docker/cli-plugins/docker-compose

# 5. Add the current user to the Docker group
echo "Configuring user permissions..."
if [ -n "$SUDO_USER" ]; then
    usermod -aG docker "$SUDO_USER"
    echo "Added user '$SUDO_USER' to the docker group."
else
    if [[ "$ID" == "amzn" ]]; then
        usermod -aG docker ec2-user 2>/dev/null
        echo "Added user 'ec2-user' to the docker group."
    elif [[ "$ID" == "ubuntu" ]]; then
        usermod -aG docker ubuntu 2>/dev/null
        echo "Added user 'ubuntu' to the docker group."
    fi
fi

echo "========================================="
echo "Installation completed successfully!"
docker --version
docker compose version
echo "========================================="
echo "IMPORTANT: You must log out of your SSH session and log back in for the user group changes to take effect."