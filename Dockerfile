FROM python:3.12-slim

# Install system dependencies for WeasyPrint and build tools
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libglib2.0-0 \
    libcairo2 \
    libharfbuzz0b \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    fonts-dejavu \
    # Build dependencies
    gcc \
    g++ \
    make \
    libffi-dev \
    # Git for revision date plugin
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install MkDocs and required plugins based on mkdocs.yml configuration
RUN pip install \
    mkdocs>=1.5.0 \
    mkdocs-material>=9.4.0 \
    mkdocs-material-extensions \
    pymdown-extensions>=10.3.0 \
    mkdocs-git-revision-date-localized-plugin>=1.2.0

RUN pip install mkdocs-glightbox

# Install mkdocs-with-pdf - this uses WeasyPrint and has no browser dependencies
RUN pip install mkdocs-to-pdf

# Set environment variable to enable PDF export
ENV ENABLE_PDF_EXPORT=1

# Set working directory
WORKDIR /docs

# Expose MkDocs development server port
EXPOSE 8000

# Start MkDocs development server on container startup
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]