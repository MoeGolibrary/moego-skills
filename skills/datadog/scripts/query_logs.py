#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dateutil",
# ]
# ///

import os
import sys
import argparse
import requests
import json
from datetime import datetime, timedelta

# Configuration
API_KEY = os.environ.get("DD_API_KEY", "2c2dae1ad5d7952998d15af901a7f60d")
APP_KEY = os.environ.get("DD_APP_KEY", "e37c634b854ddd117e546b8bf0511345cc735583")
SITE = os.environ.get("DD_SITE", "https://api.us5.datadoghq.com")

def query_logs(query, from_time=None, to_time=None, limit=10):
    url = f"{SITE}/api/v2/logs/events/search"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY
    }
    
    # Default window: last 15 minutes if not specified
    if not from_time:
        from_time = "now-15m"
    if not to_time:
        to_time = "now"

    payload = {
        "filter": {
            "from": from_time,
            "to": to_time,
            "query": query
        },
        "page": {
            "limit": limit
        },
        "sort": "-timestamp" # Newest first
    }
    
    print(f"🔎 Querying Datadog Logs...")
    print(f"   Query: {query}")
    print(f"   Time:  {from_time} to {to_time}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        logs = data.get("data", [])
        
        print(f"✅ Found {len(logs)} logs.\n")
        
        for log in logs:
            attr = log.get("attributes", {})
            ts = attr.get("timestamp")
            service = attr.get("service")
            status = attr.get("status")
            
            # Try to find the message
            message = attr.get("message")
            if not message:
                # Look deeper in attributes
                inner = attr.get("attributes", {})
                message = inner.get("message")
                
                # Fallback for Access Logs
                if not message and "http" in inner:
                    method = inner.get("http", {}).get("method") or inner.get("method")
                    path = inner.get("http", {}).get("url_details", {}).get("path") or inner.get("path")
                    code = inner.get("http", {}).get("status_code") or inner.get("status")
                    message = f"{method} {path} ({code})"
            
            print(f"[{ts}] [{service}] [{status}]")
            print(f"   {message}")
            
            # Print error details if present
            if status == "error":
                inner = attr.get("attributes", {})
                if "error" in inner:
                    err = inner["error"]
                    if isinstance(err, dict):
                        print(f"   🔥 Error: {err.get('message') or err.get('stack')}")
                    else:
                        print(f"   🔥 Error: {err}")
            
            print("-" * 40)

    except Exception as e:
        print(f"❌ Error: {e}")
        if 'response' in locals():
            print(f"Response: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Datadog Logs")
    parser.add_argument("query", help="Datadog search query (e.g. 'service:foo status:error')")
    parser.add_argument("--from", "-f", dest="from_time", help="Start time (e.g. 'now-1h', ISO8601)")
    parser.add_argument("--to", "-t", dest="to_time", help="End time (e.g. 'now', ISO8601)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Max logs to return")
    
    args = parser.parse_args()
    query_logs(args.query, args.from_time, args.to_time, args.limit)
