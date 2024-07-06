#!/bin/bash

# COLOR CODES
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# FILE PATHS
WIREPOD_PLUGIN_DIR="$HOME/wire-pod/chipper/plugins"
TARGET_DIR="$WIREPOD_PLUGIN_DIR/vectormyboi"
PROJ_DIR="$HOME/vectormyboi"
WEBROOT="$HOME/wire-pod/chipper/webroot"

echo "----- vectormyboi Development Installer -----"

echo -e "${YELLOW}Stopping wire-pod.service...${NC}"
sudo systemctl stop wire-pod
echo -e "${YELLOW}Stopping vector-flask.service...${NC}"
sudo systemctl stop vector-flask

echo -e "Removing existing vectormyboi directory..."
if [ -d "$TARGET_DIR" ]; then
    rm -rf "$TARGET_DIR"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully removed existing vectormyboi directory.${NC}"
    else
        echo -e "${RED}ERROR: Failed to remove existing vectormyboi directory.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}vectormyboi directory does not exist. No need to remove.${NC}"
fi

echo -e "Creating new vectormyboi directory..."
mkdir -p "$TARGET_DIR"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully created new vectormyboi directory.${NC}"
else
    echo -e "${RED}ERROR: Failed to create new vectormyboi directory.${NC}"
    exit 1
fi

echo -e "Moving contents from $PROJ_DIR to $TARGET_DIR..."
cp -r "$PROJ_DIR/Vector" "$TARGET_DIR"
cp -r "$PROJ_DIR/VectorConfig" "$TARGET_DIR"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully moved contents to vectormyboi directory.${NC}"
else
    echo -e "${RED}ERROR: Failed to move contents to vectormyboi directory.${NC}"
    exit 1
fi

echo "Applying changes to custom_page.html and index.html..."
sudo cp "$PROJ_DIR/custom_page.html" "$PROJ_DIR/index.html" "$WEBROOT"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully moved custom_page.html and index.html into $WEBROOT.${NC}"
else
    echo -e "${RED}ERROR: Failed to move custom_page.html and index.html into $WEBROOT.${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting wire-pod.service...${NC}"
sudo systemctl start wire-pod
echo -e "${YELLOW}Starting vector-flask.service...${NC}"
sudo systemctl start vector-flask

echo -e "${GREEN}Development installation completed successfully!${NC}"
