#!/usr/bin/env sh
# Placeholder script to ensure IPFS daemon is running (Kubo) and reachable via API

if ! command -v ipfs >/dev/null 2>&1; then
  echo "ipfs binary not found. Install Kubo (ipfs) first: https://docs.ipfs.io/install/"
  exit 1
fi

ipfs daemon &

echo "IPFS daemon started."
