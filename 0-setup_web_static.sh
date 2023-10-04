#!/usr/bin/env bash
# script that sets up your web servers for the deployment

# Install nginx if not already installed
sudo apt-get -y update
sudo apt-get -y install nginx

# Create the necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing Nginx configuration
echo "fake test file to check nginx" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to /data/web_static/releases/test
sudo ln -sf /data/web_static/releases/test/  /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
# sudo chown -R ubuntu:ubuntu /data/
sudo chown -hR ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
# Check if the location block for /hbnb_static/ already exists
if ! grep -q "location /hbnb_static/" /etc/nginx/sites-available/default; then
    # Update the Nginx configuration to serve the content
    sudo sed -i '61i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
fi
# Restart Nginx to apply the changes
sudo service nginx restart
