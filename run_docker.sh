#!/bin/bash
# Usage: ./run_docker.sh <image_name>

if [ -z "$1" ]; then
    echo "Error: Please provide an image name."
    echo "Usage: ./run_docker.sh <image_name>"
    exit 1
fi

docker run -d --name pinbot_container "$1"
echo "Container started in background. You can check logs with: docker logs -f pinbot_container"
