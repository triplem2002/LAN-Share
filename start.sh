#!/usr/bin/env bash

cd "$(dirname "$0")"

PYTHON=$(command -v python3 || command -v python)

$PYTHON server.py &

sleep 1

if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
else
    xdg-open http://localhost:8000 >/dev/null 2>&1 &
fi

wait
