---
name: datadog
description: Use this skill to fetch live telemetry (logs, traces, spans, and dependencies) for cloud services. Trigger immediately whenever the user asks to get, check, or show logs, spans, or dependencies for ANY remote service (e.g., moego-api-v3, payment, user-service) or endpoint. If the user asks for logs, spans, or errors for a service or endpoint, they mean Datadog—use this skill! This is essential for debugging 500s, tracing requests, or checking service health in recent timeframes. Do not use for reading local log files, local code dependencies, or explaining tracing concepts.
---

# Datadog

## Quick start
1. **Set credentials** in the environment:
   - `DD_API_KEY`, `DD_APP_KEY`, optional `DD_SITE` (default: https://api.us5.datadoghq.com)
2. **Query logs** (supports Flex/Rehydrated via GET):
   - `bash skills/datadog/scripts/datadog.sh "service:moego-api-v3" 10 now-4h now -v`
3. **Query logs (POST search)**:
   - `uv run skills/datadog/scripts/query_logs.py "service:moego-api-v3 status:error" -n 20 -f now-1h -t now`
4. **Search by Request ID**:
   - `uv run skills/datadog/scripts/query_logs.py "@id:26c6d5d6-79cb-4ff8-80c8-be840bfaff99" -f now-7d`
   - *Note: `x-request-id` is indexed as `@id` in Datadog.*
5. **Fetch a trace**:
   - `uv run skills/datadog/scripts/get_trace.py <trace_id>`
5. **Check Service Dependencies**:
   - `uv run skills/datadog/scripts/get_dependencies.py moego-svc-payment` (Defaults to env:ns-testing)
   - `uv run skills/datadog/scripts/get_dependencies.py moego-svc-payment --env ns-production`

## URL Construction
When asked for a Datadog link, use these parameters to match user preference:
- **Base URL**: `https://us5.datadoghq.com/logs`
- **Required Params**:
  - `storage=flex_tier` (Search Flex logs)
  - `viz=stream` (Stream view)
  - `messageDisplay=inline` (Compact rows)
  - `refresh_mode=sliding` & `live=true` (Live tail)
  - `cols=host,service` (Custom columns)

## Search Tips
- **x-request-id**: Use `@id:<uuid>` (e.g., `@id:26c6d5d6-79cb-4ff8-80c8-be840bfaff99`). The attribute name in Datadog is `@id`, not `x_request_id`.
- **Trace IDs**: Use `trace_id:<id>`.
- **Flex Logs**: The tools default to searching Flex/Rehydrated logs (`storage_tier=flex`), so older logs are searchable.

## Tools
- **scripts/datadog.sh**: Log search via `/api/v2/logs/events` with `storage_tier=flex`.
  - Use `-v` to print full JSON attributes (body/headers/trace IDs).
- **scripts/query_logs.py**: POST search to `/api/v2/logs/events/search` (newest-first summary output).
- **scripts/get_trace.py**: GET trace via `/api/v1/trace/<trace_id>` and render spans (highlights SQL/payloads).
- **scripts/query_spans.py**: POST search to `/api/v2/spans/events/search` to find traces by tag/resource (e.g. gRPC methods).
- **scripts/get_dependencies.py**: Fetch service upstream/downstream dependencies via `/api/v1/service_dependencies`. Useful for impact analysis and root cause finding.

## Dependencies
- `datadog.sh`: `curl`, `jq`
- Python scripts: `requests`, `python-dateutil` (use `uv` or your venv)
