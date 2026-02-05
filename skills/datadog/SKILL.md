---
name: moego:datadog
description: Datadog 日志/Trace/依赖查询工具集合，支持 Flex/Rehydrated 日志、Trace span 解析与服务依赖分析
triggers:
  - /moego:datadog
  - 需要查询 Datadog 日志
  - 需要查看 Trace/Span
  - 需要分析服务依赖
---

# MoeGo Datadog Skill

用于在 Datadog 中快速查询 MoeGo 相关日志、Trace 和服务依赖。

## Quick start
1. **设置凭证**（环境变量）:
   - `DD_API_KEY`, `DD_APP_KEY`, 可选 `DD_SITE` (默认: https://api.us5.datadoghq.com)
2. **查询日志**（支持 Flex/Rehydrated via GET）:
   - `bash skills/datadog/scripts/datadog.sh "service:moego-api-v3" 10 now-4h now -v`
3. **查询日志（POST search）**:
   - `uv run skills/datadog/scripts/query_logs.py "service:moego-api-v3 status:error" -n 20 -f now-1h -t now`
4. **获取 Trace**:
   - `uv run skills/datadog/scripts/get_trace.py <trace_id>`
5. **查看服务依赖**:
   - `uv run skills/datadog/scripts/get_dependencies.py moego-svc-payment` (默认 env: ns-testing)
   - `uv run skills/datadog/scripts/get_dependencies.py moego-svc-payment --env ns-production`

## Tools
- **scripts/datadog.sh**: 通过 `/api/v2/logs/events` 搜索日志，支持 `storage_tier=flex`。
  - 使用 `-v` 输出完整 JSON attributes（body/headers/trace IDs 等）。
- **scripts/query_logs.py**: POST 搜索 `/api/v2/logs/events/search`（最新优先的摘要输出）。
- **scripts/get_trace.py**: GET trace `/api/v1/trace/<trace_id>` 并渲染 spans（突出 SQL/payload）。
- **scripts/get_dependencies.py**: 查询 `/api/v1/service_dependencies` 获取上下游依赖。

## Dependencies
- `datadog.sh`: `curl`, `jq`
- Python scripts: `requests`, `python-dateutil`（建议使用 `uv`）
