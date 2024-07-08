#!/bin/bash
#
#
# Installs the vectormyboi script into an existing wire-pod installation. 
#
# 1. Verify that the wire-pod directory exists
# 2. Attempt to update wire-pod
# 3. Move the files to the correct directory

# COLOR CODES
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# FILE PATHS
WIREPOD_DIR="$HOME/wire-pod"
WIREPOD_PLUGIN_DIR="$WIREPOD_DIR/chipper/plugins"
TARGET_DIR="$WIREPOD_PLUGIN_DIR/vectormyboi"
WEBROOT="$WIREPOD_DIR/chipper/webroot"
PROJ_DIR="$HOME/vectormyboi"
VENV_DIR="$HOME/vector-venv"
SERVICE_FILE_PATH="/etc/systemd/system/vector-flask.service"

echo "----- vectormyboi Plug-In Installer -----"
echo -e "Created by: TechnoEquinox\tCreated on: 07-06-2024\tLast updated: 07-06-2024"

echo -e "\nVerifying cron installation..."
if command -v cron >/dev/null 2>&1 || command -v crond >/dev/null 2>&1; then
    echo -e "${GREEN}Cron is installed.${NC}"
else
    echo -e "${YELLOW}Cron is not installed. Installing it now...${NC}"
    sudo apt-get install cron
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully installed cron.${NC}"
    else
        echo -e "${RED}ERROR: Failed to install cron.${NC}"
        exit 1
    fi
fi

echo -e "Verifying vectormyboi files..."
if [ -d "$PROJ_DIR" ]; then
    echo -e "${GREEN}Successfully verified vectormyboi files.${NC}"
    # TODO: Check for vectormyboi update
else
    echo -e "${RED}ERROR: Verification of vectormyboi files failed.${NC}"
    exit 1
fi

echo "Verifying wire-pod installation..."
if [ -d "$WIREPOD_DIR" ]; then
  echo -e "${GREEN}Successfully verified wire-pod installation.${NC}"
  
  echo "Verifying wire-pod plug-in directory..."
  if [ -d "$WIREPOD_PLUGIN_DIR" ]; then
    echo -e "${GREEN}Successfully verified wire-pod plug-in directory.${NC}"

    echo "Verifying if plugin/vectormyboi exists..."
    if [ -d "$TARGET_DIR" ]; then
        echo -e "${GREEN}plugin/vectormyboi already exists.${NC}"
    else
        echo -e "${YELLOW}plugin/vectormyboi does not exist. Creating it now...${NC}"
        mkdir -p "$TARGET_DIR"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully created plugin/vectormyboi.${NC}"
        else
            echo -e "${RED}ERROR: Failed to create plugin/vectormyboi.${NC}"
            exit 1
        fi
    fi
    
    echo "Verifying the wire-pod webroot..."
    if [ -d "$WEBROOT" ]; then
        echo -e "${GREEN}Successfully verified wire-pod webroot.${NC}"
        # Continue
        echo "Checking for wire-pod updates..."
        echo -e "${YELLOW}Stopping wire-pod service.${NC}"
        sudo systemctl stop wire-pod
        cd $HOME/wire-pod
        sudo ./update.sh
        echo -e "${GREEN}Checking for wire-pod updates completed.${NC}"
        cd $HOME/vectormyboi  
    else
        echo -e "${RED}ERROR: Verification of wire-pod webroot failed.${NC}"
        exit 1
    fi
  else
    echo -e "${RED}ERROR: Verification of wire-pod plug-in directory failed.${NC}"
    exit 1
  fi
else
  echo -e "${RED}ERROR: Verification of wire-pod installation failed.${NC}"
  exit 1
fi

echo "Installing Vector to ${TARGET_DIR}"
cp -r Vector $TARGET_DIR
if [ -d "$TARGET_DIR/Vector" ] && [ "$(ls -A $TARGET_DIR/Vector)" ]; then
    echo -e "${GREEN}Successfully installed Vector to ${TARGET_DIR}.${NC}"
else
    echo -e "${RED}ERROR: Installation of Vector to ${TARGET_DIR} failed.${NC}"
    exit 1
fi

echo "Installing VectorConfig to ${TARGET_DIR}"
cp -r VectorConfig $TARGET_DIR
if [ -d "$TARGET_DIR/VectorConfig" ] && [ "$(ls -A $TARGET_DIR/VectorConfig)" ]; then
    echo -e "${GREEN}Successfully installed VectorConfig to ${TARGET_DIR}.${NC}"
else
    echo -e "${RED}ERROR: Installation of VectorConfig to ${TARGET_DIR} failed.${NC}"
    exit 1
fi

echo "Installing files to ${WEBROOT}"
sudo cp shop_items.json custom_page.html index.html $WEBROOT
if [ -f "$WEBROOT/index.html" ] && [ -f "$WEBROOT/shop_items.json" ] && [ -f "$WEBROOT/custom_page.html" ]; then
    echo -e "${GREEN}Successfully installed configs to ${WEBROOT}.${NC}"
else
    echo -e "${RED}ERROR: Installation of configs to ${WEBROOT} failed.${NC}"
    exit 1
fi

# Check if robot_config.json exists in the webroot
if [ -f "$WEBROOT/robot_config.json" ]; then
    echo -e "${GREEN}robot_config.json already exists in the webroot.${NC}"
else
    echo -e "${YELLOW}robot_config.json does not exist. Creating it now...${NC}"
    
    # Prompt the user for input
    read -p "Enter the robot's serial number: " robotSerial
    read -p "Enter the robot's IP address: " ip_address
    read -p "Enter the robot's name: " robot_name
    
    # Create the robot_config.json file
    cat <<EOL > "$WEBROOT/robot_config.json"
{
    "robotSerial": "$robotSerial",
    "ip_address": "$ip_address",
    "robot_name": "$robot_name",
    "robot_wallet": 0,
    "robot_energy_level": 20,
    "robot_level": 1,
    "robot_xp": 0,
    "last_jog": "2000-01-01T00:00:01",
    "robot_total_jog_dist": 0,
    "items": []
}
EOL

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully created robot_config.json.${NC}"
    else
        echo -e "${RED}ERROR: Failed to create robot_config.json.${NC}"
        exit 1
    fi
fi

echo "Configuring cron jobs..."

# Define the cron job
CRON_JOB="0 * * * * /usr/bin/python3 $TARGET_DIR/Vector/energy_manager.py >> $TARGET_DIR/VectorConfig/Logging/energy_manager_log.txt 2>&1"

# Check if the cron job already exists
(crontab -l | grep -Fxq "$CRON_JOB")

# If the cron job doesn't exist, add it
if [ $? -ne 0 ]; then
    (crontab -l; echo "$CRON_JOB") | crontab -
    echo -e "${GREEN}Successfully added cron job.${NC}"
else
    echo -e "${YELLOW}Cron job already exists. No changes made.${NC}"
fi

# venv and Python package installation
echo "Checking if Python venv already exists in $HOME ..."
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Python venv already exists. No changes made.${NC}"
else
    echo -e "${YELLOW}Python venv does not exist. Creating it now...${NC}"
    python3 -m venv "$VENV_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully created Python venv.${NC}"
        echo "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully activated virtual environment.${NC}"
            echo "Installing required Python packages..."
            pip install -r "$PROJ_DIR/requirements.txt"
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Successfully installed required Python packages.${NC}"
            else
                echo -e "${RED}ERROR: Failed to install required Python packages.${NC}"
                deactivate
                exit 1
            fi
            deactivate
        else
            echo -e "${RED}ERROR: Failed to activate virtual environment.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}ERROR: Failed to create Python venv.${NC}"
        exit 1
    fi
fi

# Add environment variable to venv activate script
echo "Adding PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION environment variable to venv..."
echo 'export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python' >> "$VENV_DIR/bin/activate"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully added environment variable.${NC}"
else
    echo -e "${RED}ERROR: Failed to add environment variable.${NC}"
    exit 1
fi

# Define the systemd service file content
SERVICE_FILE_CONTENT="[Unit]
Description=VectorMyBoi Python Server
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$TARGET_DIR/VectorConfig/
ExecStart=$HOME/vector-venv/bin/python3 $TARGET_DIR/VectorConfig/python_server.py
Environment=\"PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python\"
Restart=always

[Install]
WantedBy=multi-user.target
"

# Write the service file
echo "Creating systemd service file at $SERVICE_FILE_PATH..."
echo "$SERVICE_FILE_CONTENT" | sudo tee $SERVICE_FILE_PATH > /dev/null

# Reload systemd to recognize the new service, enable it, and start it
echo -e "${YELLOW}Reloading systemd, enabling and starting the vector-flask service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable vector-flask.service
sudo systemctl start vector-flask.service
echo -e "${GREEN}Python server service has been set up and started successfully.${NC}"

cd $WIREPOD_DIR
echo "Enabling the wire-pod daemon..."
sudo ./setup.sh daemon-enable
echo -e "${GREEN}Starting wire-pod service...${NC}"
sudo systemctl start wire-pod

echo -e "${GREEN}Success!${NC}"