#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
# Use the installed Ruby that has this project's Jekyll dependencies.
export PATH="$HOME/.rbenv/versions/3.2.2/bin:$PATH"
exec bundle exec jekyll serve --host 127.0.0.1 --port 4000
