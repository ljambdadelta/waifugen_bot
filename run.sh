#!/bin/bash

WAIFU_BOT_TOKEN=""

scriptname=$(basename "$0")

if [ -z "$WAIFU_BOT_TOKEN" ]; then
    echo "WAIFU_BOT_TOKEN isnt set. " \
        "Please edit the value of WAIFU_BOT_TOKEN inside $scriptname and try again"
    exit 1
fi
export WAIFU_BOT_TOKEN

exec python -m "src"
