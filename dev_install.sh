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

echo "----- vectormyboi Development Installer -----"

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

echo -e "${GREEN}Development installation completed successfully!${NC}"
