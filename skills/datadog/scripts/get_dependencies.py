#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///

import os
import sys
import argparse
import requests
import json

# Configuration
API_KEY = os.environ.get("DD_API_KEY")
APP_KEY = os.environ.get("DD_APP_KEY")
SITE = os.environ.get("DD_SITE", "https://api.us5.datadoghq.com")

if not API_KEY or not APP_KEY:
    print("Error: DD_API_KEY and DD_APP_KEY must be set.")
    sys.exit(1)
DEFAULT_ENV = "ns-testing"

def get_dependencies(service_name, env=DEFAULT_ENV):
    url = f"{SITE}/api/v1/service_dependencies/{service_name}"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": API_KEY,
        "DD-APPLICATION-KEY": APP_KEY
    }
    
    params = {
        "env": env
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Output strictly in JSON for easy parsing by LLM Agents
        print(json.dumps(data, indent=2))

    except requests.exceptions.HTTPError as e:
        # Check for 404 or specific Datadog errors
        if e.response.status_code == 404:
            print(json.dumps({
                "error": "Service not found or no dependencies data available.",
                "service": service_name,
                "env": env
            }, indent=2))
        else:
            print(json.dumps({
                "error": f"HTTP Error: {str(e)}",
                "detail": e.response.text
            }, indent=2))
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({
            "error": f"Unexpected error: {str(e)}"
        }, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query Datadog Service Dependencies")
    parser.add_argument("service", help="Service name (e.g. moego-svc-payment)")
    parser.add_argument("--env", "-e", default=DEFAULT_ENV, help=f"Environment (default: {DEFAULT_ENV})")
    
    args = parser.parse_args()
    get_dependencies(args.service, args.env)
