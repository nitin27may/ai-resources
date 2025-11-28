# EA Notes Documentation

This repository contains Enterprise Architecture documentation and notes.

## Introduction

This project serves as a centralized location for Enterprise Architecture documentation, including system capabilities, architectural decisions, and technical specifications.

## Getting Started

### Prerequisites

Choose one of the following development environments:

**Option 1: Dev Container (Recommended)**
- Visual Studio Code with Remote-Containers extension
- Docker installed on your machine

**Option 2: Docker Compose**
- Docker and Docker Compose installed on your machine

### Development Environment Setup

#### Option 1: Using Dev Container (Recommended)

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd EA-Notes
   ```

2. **Open in Visual Studio Code**:
   ```bash
   code .
   ```

3. **Open in Dev Container**:
   - When prompted, click "Reopen in Container"
   - Or use Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and select "Dev Containers: Reopen in Container"

4. **Automatic Setup**:
   - VS Code will build the dev container (this may take a few minutes on first run)
   - Dependencies will be automatically installed via `requirements.txt`
   - MkDocs development server will start automatically on port 8000

5. **Access the site**:
   - Open your browser and navigate to [http://localhost:8000](http://localhost:8000)
   - The documentation site will automatically reload when you make changes to any Markdown files

**The dev container includes**:
- Python 3.12 slim environment with native setup (no Docker Compose)
- All required MkDocs dependencies and plugins
- Live reload functionality with hot reloading
- PDF export capabilities via WeasyPrint
- Pre-configured VS Code extensions:
  - Python support with Black formatter
  - Markdown All in One
  - Markdown lint
  - Mermaid diagram support
- Useful VS Code tasks for building and serving
- Non-root user setup for security

#### Option 2: Using Docker Compose

1. Clone this repository
2. Navigate to the repository root directory
3. Run the following command to start the MkDocs Material container:

```bash
docker-compose up
```

4. Open your browser and navigate to [http://localhost:8000](http://localhost:8000)
5. The documentation site will automatically reload when you make changes to any of the Markdown files

### Stopping the Documentation Site

**For Dev Container:**
- The server runs automatically in the background
- To stop: Use the VS Code terminal and press `Ctrl+C`

**For Docker Compose:**
To stop the running container, press `Ctrl+C` in the terminal or run:
```bash
docker-compose down
```

## Documentation Structure

- `/docs/` - Contains all Markdown documentation files
- `mkdocs.yml` - MkDocs configuration file
- `docker-compose.yml` - Docker Compose configuration for running MkDocs Material

## Adding New Documentation

1. Create a new Markdown file in the `/docs/` directory
2. Add the new file to the navigation in the `mkdocs.yml` file
3. Restart the container if needed

## Build and Deploy

### Development Build
The dev container and docker-compose setup automatically serve the documentation with live reload.

### Production Build

To build a static version of the documentation site for deployment:

**Using Dev Container:**
```bash
# Open terminal in VS Code (dev container) and run:
mkdocs build
```

**Using Docker:**
```bash
docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material build
```

**Using Docker with custom Dockerfile:**
```bash
docker build -t ea-notes-mkdocs .
docker run --rm -v ${PWD}:/workspace ea-notes-mkdocs mkdocs build
```

This will create a `site` directory with the static HTML files that can be deployed to any web server.

### PDF Export

The project is configured to generate PDF exports of the documentation. To enable PDF generation:

1. Ensure the `ENABLE_PDF_EXPORT=1` environment variable is set (included in dev container)
2. Run the build command as shown above
3. PDF files will be generated alongside the HTML output

## Development Tips

### Working with the Dev Container

- **Terminal Access**: Use the integrated terminal in VS Code to run MkDocs commands
- **File Changes**: All file changes are automatically synced and trigger live reload
- **Port Forwarding**: Port 8000 is automatically forwarded and accessible at `http://localhost:8000`
- **Extensions**: The dev container includes pre-configured extensions for Markdown editing and Mermaid diagrams

### Useful Commands

```bash
# Start the development server manually (if needed)
mkdocs serve --dev-addr=0.0.0.0:8000 --livereload

# Build the site
mkdocs build

# Check for configuration issues
mkdocs config

# Install additional dependencies
pip install <package-name>
```

### Troubleshooting

**Dev Container Issues:**
- **Config not found**: Ensure the `.devcontainer/devcontainer.json` file exists
- **Port already in use**: If port 8000 is busy, stop any other services using port 8000 or change the port in `devcontainer.json`
- **Container won't start**: Ensure Docker is running and you have sufficient permissions
- **Dependencies not installing**: Try rebuilding the container (Command Palette → "Dev Containers: Rebuild Container")

**General Issues:**
- **PDF export issues**: PDF export requires additional system dependencies which are included in the dev container
- **Mermaid diagrams not rendering**: Check that the `pymdownx.superfences` extension is configured correctly in `mkdocs.yml`
- **Live reload not working**: Ensure the development server is running with the `--livereload` flag

## Contributing

Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request