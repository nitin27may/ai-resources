"""
MkDocs hook to add cache-busting query parameters to assets
"""
import os
import time
from pathlib import Path

def on_post_build(config, **kwargs):
    """
    Add cache control headers file for GitHub Pages
    """
    site_dir = Path(config['site_dir'])
    
    # Create _headers file for Netlify-style deployment (if needed)
    headers_content = """/*
  Cache-Control: no-cache, no-store, must-revalidate
  Pragma: no-cache
  Expires: 0

/*.html
  Cache-Control: no-cache, no-store, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/blog/*
  Cache-Control: no-cache, no-store, must-revalidate
"""
    
    headers_file = site_dir / '_headers'
    with open(headers_file, 'w') as f:
        f.write(headers_content)
    
    print(f"✓ Created cache control headers file")
    
    # Create .nojekyll file to prevent GitHub Pages from ignoring _headers
    nojekyll = site_dir / '.nojekyll'
    nojekyll.touch()
    
    print(f"✓ Created .nojekyll file")

def on_env(env, config, files, **kwargs):
    """
    Add cache-busting timestamp to Jinja environment
    """
    env.globals['cache_bust'] = str(int(time.time()))
    return env
