#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "python-dateutil",
# ]
# ///
import argparse
import os
import sys
import json
import requests
from dateutil.parser import parse
from datetime import datetime, timezone

def search_spans(query, limit=10, from_time="now-15m", to_time="now", sort="-timestamp"):
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    site = os.environ.get("DD_SITE", "https://api.us5.datadoghq.com")

    if not api_key or not app_key:
        print("Error: DD_API_KEY and DD_APP_KEY must be set in environment")
        sys.exit(1)

    url = f"{site}/api/v2/spans/events/search"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key
    }

    # Handle sort format
    sort_val = sort
    if sort == "timestamp_asc":
        sort_val = "timestamp"
    elif sort == "timestamp_desc":
        sort_val = "-timestamp"

    payload = {
        "data": {
            "attributes": {
                "filter": {
                    "from": from_time,
                    "query": query,
                    "to": to_time
                },
                "options": {
                    "timezone": "UTC"
                },
                "page": {
                    "limit": limit
                },
                "sort": sort_val
            },
            "type": "search_request"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying Datadog Spans API: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

def format_span(span):
    attr = span.get("attributes", {})
    custom = attr.get("custom", {})
    tags = attr.get("tags", [])
    
    # Flatten important attributes for display
    return {
        "timestamp": attr.get("start_timestamp"),
        "service": attr.get("service"),
        "resource": attr.get("resource_name"),
        "operation": attr.get("operation_name", attr.get("name")), # fallback to name if operation_name missing
        "trace_id": attr.get("trace_id"),
        "span_id": attr.get("span_id"),
        "parent_id": attr.get("parent_id"),
        "duration_ms": (attr.get("duration") or 0) / 1000000.0,
        "status": attr.get("status"),
        "error": (attr.get("error") or 0) > 0,
        "tags": tags,
        # Try to extract interesting custom attributes
        "http.method": attr.get("http", {}).get("method") or custom.get("http.method"),
        "http.status_code": attr.get("http", {}).get("status_code") or custom.get("http.status_code"),
        "grpc.method": custom.get("grpc.method"),
    }

def main():
    parser = argparse.ArgumentParser(description="Search Datadog Spans (Traces)")
    parser.add_argument("query", help="Span search query (e.g. 'service:my-service resource_name:GET /health')")
    parser.add_argument("-n", "--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("-f", "--from-time", default="now-15m", help="Start time (default: now-15m)")
    parser.add_argument("-t", "--to-time", default="now", help="End time (default: now)")
    parser.add_argument("-s", "--sort", choices=["timestamp", "-timestamp"], default="-timestamp", help="Sort order")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print full JSON response")

    args = parser.parse_args()

    print(f"🔎 Querying Datadog Spans...")
    print(f"   Query: {args.query}")
    print(f"   Time:  {args.from_time} to {args.to_time}")

    result = search_spans(args.query, args.limit, args.from_time, args.to_time, args.sort)
    
    data = result.get("data", [])
    print(f"✅ Found {len(data)} spans.\n")

    if args.verbose:
        print(json.dumps(result, indent=2))
    else:
        for item in data:
            span = format_span(item)
            ts = span['timestamp']
            svc = span['service']
            res = span['resource']
            dur = span['duration_ms']
            err = "❌" if span['error'] else "✅"
            
            print(f"[{ts}] {err} [{svc}] {res} ({dur:.2f}ms)")
            print(f"   TraceID: {span['trace_id']} | SpanID: {span['span_id']}")
            if span.get('grpc.method'):
                print(f"   gRPC: {span['grpc.method']}")
            if span.get('http.method'):
                print(f"   HTTP: {span['http.method']} {span['http.status_code']}")
            print("-" * 40)

if __name__ == "__main__":
    main()
