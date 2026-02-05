#!/bin/bash

# Datadog Log Query Tool for OpenClaw
# Usage: ./datadog.sh <query> [limit] [from] [to] [-v]

# 1. Try to get keys from Environment Variables (Best Practice)
API_KEY="${DD_API_KEY}"
APP_KEY="${DD_APP_KEY}"
SITE="${DD_SITE:-https://api.us5.datadoghq.com}"

if [ -z "$API_KEY" ] || [ -z "$APP_KEY" ]; then
  echo "Error: DD_API_KEY and DD_APP_KEY must be set."
  exit 1
fi

if [ -z "$1" ]; then
  echo "Error: Query string required."
  echo "Usage: $0 <query> [limit] [from] [to] [-v]"
  echo "Example: $0 'service:moego-api-v3' 5 now-4h now -v"
  exit 1
fi

QUERY="$1"
LIMIT=${2:-10}

# Default time window (4 hours) or user provided
FROM=${3:-"now-4h"}
TO=${4:-"now"}
VERBOSE=${5:-false}

# Use GET method with storage_tier=flex for ALL queries.
# This covers both recent (Standard) and older (Flex/Rehydrated) logs.
# Using --data-urlencode handles all special characters automatically.

response=$(curl -s -G "$SITE/api/v2/logs/events" \
  -H "DD-API-KEY: $API_KEY" \
  -H "DD-APPLICATION-KEY: $APP_KEY" \
  --data-urlencode "filter[query]=$QUERY" \
  --data-urlencode "filter[from]=$FROM" \
  --data-urlencode "filter[to]=$TO" \
  --data-urlencode "filter[storage_tier]=flex" \
  --data-urlencode "page[limit]=$LIMIT")

# Check for errors
if echo "$response" | grep -q "\"errors\""; then
  echo "❌ Datadog API Error:" >&2
  echo "$response" >&2
  exit 1
fi

count=$(echo "$response" | jq '.data | length')
if [ "$count" -eq 0 ]; then
  echo "⚠️ No logs found." >&2
else 
  if [ "$VERBOSE" = "true" ] || [ "$VERBOSE" = "-v" ]; then
    # Verbose Mode: Print the full attributes JSON object for each log
    # This ensures we don't miss ANY field (Body, Headers, Custom Attributes, etc.)
    echo "$response" | jq '.data[].attributes'
  else
    # Summary Mode: Clean one-line output
    echo "$response" | jq -r '.data[] | 
    "[\(.attributes.timestamp)] [\(.attributes.service)] [\(.attributes.status)] " + 
    if .attributes.message then .attributes.message
    elif .attributes.attributes.message then .attributes.attributes.message
    elif .attributes.attributes.path then "\(.attributes.attributes.method) \(.attributes.attributes.path) (\(.attributes.attributes.status))"
    else "No message" end'
  fi
fi

