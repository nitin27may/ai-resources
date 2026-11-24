# Single stage: this image only ever runs `mkdocs serve` for local authoring.
# It is not the deployment artifact -- GitHub Actions builds the static site and
# publishes that. There was a second, byte-identical Dev.Dockerfile; only one is
# needed and two guarantee they drift.
FROM python:3.14-slim

# git is required by the git-revision-date-localized plugin, which reads commit
# dates to show "last updated" on each page.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

# Dependencies first, so editing content does not invalidate this layer.
# Installed from pyproject.toml and uv.lock, the same inputs CI uses. The venv
# lives outside /docs because the compose file bind-mounts the repo over it.
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml uv.lock /tmp/deps/
RUN cd /tmp/deps && uv sync --locked --no-install-project --no-cache \
    && rm -rf /tmp/deps

# Run as a non-root user.
RUN useradd --create-home --uid 1000 docs
WORKDIR /docs
USER docs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/').status==200 else 1)"

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000", "--livereload"]
