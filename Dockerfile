# Single stage: this image only ever runs `mkdocs serve` for local authoring.
# It is not the deployment artifact -- GitHub Actions builds the static site and
# publishes that. There was a second, byte-identical Dev.Dockerfile; only one is
# needed and two guarantee they drift.
FROM python:3.12-slim

# git is required by the git-revision-date-localized plugin, which reads commit
# dates to show "last updated" on each page.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

# Dependencies first, so editing content does not invalidate this layer.
# Installed from requirements.txt rather than a hardcoded list: the previous
# Dockerfiles pinned a different PDF plugin than requirements.txt did, for an
# export that was never enabled.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Run as a non-root user.
RUN useradd --create-home --uid 1000 docs
WORKDIR /docs
USER docs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/').status==200 else 1)"

CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000", "--livereload"]
