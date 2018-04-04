#!/usr/bin/env bash

if [ "$1" = "sync" ]; then
  exec python sync.py
fi

exec "$@"
