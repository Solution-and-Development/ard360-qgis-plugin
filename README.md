# ARD360 QGIS Plugin

A QGIS plugin for loading and viewing 360-degree imagery from PostgreSQL databases.

## Features

- **PostgreSQL Integration**: Connect to PostgreSQL databases (no PostGIS required)
- **Middleware Architecture**: Converts lat/lon coordinates to QGIS vector geometries
- **360� Viewer**: Interactive 360-degree panoramic image viewer using Pannellum
- **Point-and-Click**: Click on map points to instantly view associated 360 images
- **Layer Management**: Automatic vector layer creation with custom styling
- **Configuration UI**: Easy-to-use database configuration dialog

## Requirements

- QGIS 3.0 or higher
- PostgreSQL database with 360 imagery data
- Database table with at minimum:
  - Latitude column (numeric)
  - Longitude column (numeric)
  - Image URL column (text)

## Installation

### Option 1: Install from ZIP

1. Download or build the plugin ZIP file
2. Open QGIS
3. Go to **Plugins � Manage and Install Plugins**
4. Click **Install from ZIP**
5. Select the `ard-qgis-plugin.zip` file
6. Restart QGIS

### Option 2: Manual Installation

1. Copy the plugin folder to your QGIS plugins directory:
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`
   - Windows: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
2. Restart QGIS
