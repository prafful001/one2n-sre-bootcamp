#!/bin/bash

install_docker() {
  echo "Installing Docker..."
  apt-get update -y
  apt-get install -y apt-transport-https ca-certificates curl software-properties-common
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
  apt-get update -y
  apt-get install -y docker-ce
  systemctl start docker
  systemctl enable docker
}

install_docker_compose() {
  echo "Installing Docker Compose..."
  curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
}

install_make() {
  echo "Installing Make..."
  apt-get install -y make
}

install_docker
install_docker_compose
install_make

echo "Setup complete!"