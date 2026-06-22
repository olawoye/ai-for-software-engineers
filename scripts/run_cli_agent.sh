#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 project-todo/module-XX/lesson.py"
  exit 1
fi

python -m src.cli_agent "$1"
