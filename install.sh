#!/bin/bash
#
# Quick Installation Script for NOAA Space Weather
# This script copies the custom component to your Home Assistant config directory
#

set -e

echo "========================================="
echo "NOAA Space Weather Installation"
echo "========================================="
echo ""

# Check if running in the repository directory
if [ ! -f "custom_components/space_weather/manifest.json" ]; then
    echo "Error: Please run this script from the repository root directory"
    exit 1
fi

# Ask for Home Assistant config directory
read -p "Enter your Home Assistant config directory path (default: ~/.homeassistant): " HA_CONFIG_DIR
HA_CONFIG_DIR=${HA_CONFIG_DIR:-~/.homeassistant}

# Expand tilde to home directory
HA_CONFIG_DIR="${HA_CONFIG_DIR/#\~/$HOME}"

# Check if config directory exists
if [ ! -d "$HA_CONFIG_DIR" ]; then
    echo "Error: Directory '$HA_CONFIG_DIR' does not exist"
    exit 1
fi

# Create custom_components directory if it doesn't exist
CUSTOM_COMPONENTS_DIR="$HA_CONFIG_DIR/custom_components"
if [ ! -d "$CUSTOM_COMPONENTS_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_COMPONENTS_DIR"
fi

# Copy the component files
echo "Copying space_weather component..."
cp -r custom_components/space_weather "$CUSTOM_COMPONENTS_DIR/"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Add this to your configuration.yaml:"
echo ""
echo "   sensor:"
echo "     - platform: space_weather"
echo ""
echo "   Optional - add GloTEC with lat/lon ranges:"
echo "     - platform: space_weather"
echo "       lat_range_min: 25.0"
echo "       lat_range_max: 50.0"
echo "       lon_range_min: -125.0"
echo "       lon_range_max: -65.0"
echo ""
echo "2. Restart Home Assistant"
echo ""
echo "For dashboard cards, copy files from dashboard/www/ to $HA_CONFIG_DIR/www/"
echo ""
