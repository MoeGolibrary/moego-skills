#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///

import os
import sys
import requests
import json
from datetime import datetime

# Configuration
API_KEY = os.environ.get("DD_API_KEY")
APP_KEY = os.environ.get("DD_APP_KEY")
SITE = os.environ.get("DD_SITE", "https://api.us5.datadoghq.com")

if not API_KEY or not APP_KEY:
    print("Error: DD_API_KEY and DD_APP_KEY must be set.")
    sys.exit(1)

def get_trace(trace_id):
    url = f"{SITE}/api/v1/trace/{trace_id}"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY
    }
    
    print(f"🔎 Fetching Trace {trace_id} from {SITE}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        spans = []
        # Correctly handle { trace: { spans: { ... } } }
        if "trace" in data and isinstance(data["trace"], dict) and "spans" in data["trace"]:
             spans_map = data["trace"]["spans"]
             spans = list(spans_map.values())
        # Correctly handle { spans: ... }
        elif "spans" in data:
             if isinstance(data["spans"], dict):
                 spans = list(data["spans"].values())
             else:
                 spans = data["spans"]
        # Fallback
        elif "trace" in data and isinstance(data["trace"], dict):
             # Maybe raw map without spans key?
             spans = [v for v in data["trace"].values() if isinstance(v, dict)]
        else:
             print("⚠️ Unknown response format keys:", data.keys())

        print(f"✅ Found {len(spans)} spans.\n")
        
        spans.sort(key=lambda x: x.get("start", 0))
        
        for span in spans:
            service = span.get("service", "unknown")
            name = span.get("name", "unknown") 
            resource = span.get("resource", "unknown")
            duration_ms = span.get("duration", 0) / 1000000.0
            error = span.get("error", 0)
            meta = span.get("meta", {})
            
            status = "🔴" if error else "🟢"
            
            print(f"{status} [{service}] {name}")
            print(f"   Resource: {resource}")
            print(f"   Duration: {duration_ms:.2f}ms")
            
            if meta:
                print("   Tags:")
                for k, v in meta.items():
                    if "db.statement" in k or "sql" in k or "query" in k:
                         print(f"     💾 SQL: {v}")
                    elif "body" in k or "payload" in k or "json" in k or "input" in k:
                        # Highlight payloads
                        print(f"     👉 {k}: {v[:500]}..." if len(v) > 500 else f"     👉 {k}: {v}")
                    elif "error" in k:
                         print(f"     🔥 {k}: {v}")
                    elif k in ["env", "version", "component", "language", "runtime-id", "process_id"]:
                        continue
                    else:
                        # Optional: filter out standard http tags to reduce noise
                        if not k.startswith("http.") and not k.startswith("_dd."):
                            print(f"     - {k}: {v}")
            print("-" * 60)

    except Exception as e:
        print(f"❌ Error fetching trace: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run get_trace.py <trace_id>")
        sys.exit(1)
    
    get_trace(sys.argv[1])
