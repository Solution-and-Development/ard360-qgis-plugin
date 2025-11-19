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

## Development Setup

### Prerequisites

- Python 3.11+
- UV package manager

### Setup Development Environment

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install development dependencies
uv pip install -e ".[dev]"
```

### Building the Plugin

```bash
# Using the build script
./build.sh

# Or using Make
make build
```

### Installing for Development

```bash
make install
```

## Usage

### 1. Configure Database Connection

1. Click the ARD360 toolbar icon or go to **ARD360 � Configure Database**
2. Enter your PostgreSQL connection details:
   - Host (e.g., `localhost`)
   - Port (default: `5432`)
   - Database name
   - Username
   - Password
3. Click **Test Connection** to verify
4. Click **Refresh Tables** to load available tables
5. Select your table containing 360 data
6. Specify column names for:
   - Latitude
   - Longitude
   - Image URL
7. Click **Save**

### 2. Load 360 Points

1. Go to **ARD360 � Load 360 Points**
2. The plugin will:
   - Connect to your database
   - Fetch all records with valid coordinates
   - Create a vector layer with point features
   - Add the layer to your QGIS project
   - Zoom to the layer extent

### 3. View 360 Images

**Method 1: Automatic (Click on Map)**
- Simply click on any point in the ARD 360 Points layer
- The 360 viewer will open automatically

**Method 2: Manual Selection**
- Select a feature using the QGIS selection tool
- Go to **ARD360 � View Selected 360 Image**

### 4. 360 Viewer Controls

- **Pan**: Click and drag
- **Zoom**: Mouse wheel or zoom controls
- **Auto-rotate**: Enabled after 3 seconds of inactivity
- **Fullscreen**: Click the fullscreen button
- **Close**: Click the close button