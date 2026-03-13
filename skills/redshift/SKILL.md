---
name: redshift
description: Use this skill ANY TIME you need to query MoeGo production data, look up business emails, company IDs, or payment tables (legacy or new), or troubleshoot local psql connection errors to prod (like fe_sendauth). It handles routing to the correct Redshift database (mysql_prod, pg_moego_*_prod), cross-database joins, and account lookups. Use this for ANY request mentioning Redshift, prod databases, MoeGo accounts, transactions, or finding references across tables.
compatibility: opencode
metadata:
  domain: data
  database: redshift
  mode: read-only-first
---

## What I do

- **Context**: This Redshift cluster is a read-only sync of production databases. You cannot break production data (write access is physically disabled), so you can query confidently.
- Route MoeGo production queries to the correct Redshift database before querying.
- Even though reading is safe, prefer fast metadata discovery and bounded SQL over exploratory full scans to get faster answers and save cluster resources.
- Return concise findings with the SQL used, assumptions, and caveats.

## Quick start

1. Infer `target_db` from domain, table names, or field clues before connecting.
2. Check local `psql` and `~/.pg_service.conf`.
3. Validate the connection with `select current_database(), current_user;`.
4. Check schema, table, and columns with bounded metadata queries.
5. Run a bounded `SELECT` with explicit columns, filters, and `LIMIT`.
6. Return the conclusion first, then SQL, assumptions, and next checks.

## Routing decision tree

- Never default to `mysql_prod` unless the requested object is known MySQL-origin.
- Route MySQL-origin business data to `mysql_prod`.
- Route Postgres service data to `pg_moego_<service>_prod`.
- Route shared Postgres domains to `pg_moego_data_<domain>_prod`.
- Expect `moe_*` schemas in `mysql_prod` and usually `public` in `pg_moego_*_prod`.
- If two routes are plausible, state the inference; ask one focused question only when the database choice materially changes the answer.

Common route hints:

- `mysql_prod` for `moe_business`, `moe_payment`, `moe_grooming`

## Connection modes

### Local psql fallback

- Check `command -v psql`.
- Check `~/.pg_service.conf` for a `[redshift]` service before asking for connection details.
- Validate the target database before discovery work:

```sql
select current_database(), current_user;
```

- Preferred bootstrap command shape:

```bash
psql "service=redshift dbname=<target_db>" -X -qAt -c "select current_database(), current_user;"
```

- For machine-friendly terminal output, prefer `-X -qAt` and use `-F $'\t'` when tab-separated output helps.
- Never print secret values or credential file contents in the chat response.

### Passfile matching gotcha

- `psql` passfile matching is exact on `host:port:dbname:user`.
- If a local service points to `dev` but the query overrides `dbname` to a prod database such as `mysql_prod` or `pg_moego_*_prod`, a passfile row for `dev` will not match.
- A common symptom is `fe_sendauth: no password supplied` even when the service looks valid.
- When this happens, inspect the configured auth source and confirm there is a credential entry for the overridden database name or a safe wildcard match.
- Never print passfile contents or secret values in the final response.

## Metadata probe order

1. Infer `target_db` from the request.
2. Validate the connection in that database.
3. Verify expected schema and table existence with bounded `information_schema` queries.
4. Inspect only the needed columns.
5. Run the content query with explicit filters and `LIMIT`.

Table existence template:

```sql
select table_schema, table_name
from information_schema.tables
where table_schema = :schema
  and table_name in (:table_list)
order by 1, 2;
```

Column lookup template:

```sql
select table_name, column_name
from information_schema.columns
where table_schema = :schema
  and table_name in (:table_list)
order by table_name, ordinal_position;
```

## Common recipes

### Email -> company or business

Use this when the user asks which company or business an email belongs to, and replicate admin profile behavior exactly.

- `target_db`: `pg_moego_account_prod` + `mysql_prod` (cross-database query)
- Primary tables: `pg_moego_account_prod.public.account`, `mysql_prod.moe_business.moe_staff`, `mysql_prod.moe_business.moe_company`, `mysql_prod.moe_business.moe_business`
- Canonical chain (admin parity): `account.email -> account.id -> staff.account_id -> staff.company_id -> business.company_id`
- Required account filters (admin parity): `status <> 2`, `namespace_type = 'MOEGO'`, `namespace_id = 0`
- Do not use `legacy_moe_account`, `moe_account_0514_pc`, or `moe_staff.profile_email` for this lookup.
- Do not rely on `moe_staff.business_id` alone; it can be `0` or missing.

Canonical query template (returns both company and business):

```sql
with matched_account as (
  select id as account_id, email
  from pg_moego_account_prod.public.account
  where lower(email) = lower(:email)
    and status <> 2
    and namespace_type = 'MOEGO'
    and namespace_id = 0
)
select distinct
  a.account_id,
  s.company_id,
  c.name as company_name,
  b.id as business_id,
  b.business_name
from matched_account a
join mysql_prod.moe_business.moe_staff s
  on s.account_id = a.account_id
left join mysql_prod.moe_business.moe_company c
  on c.id = s.company_id
left join mysql_prod.moe_business.moe_business b
  on b.company_id = s.company_id
order by s.company_id, b.id;
```

If no rows are returned, verify the email exists in `pg_moego_account_prod.public.account` with the required namespace and status filters before checking other causes.

Supporting email fields for validation, not identity source:

- `moe_business.moe_business_email.notification_email`
- `moe_business.moe_business.contact_email`
- `moe_grooming.moe_book_online_profile.business_email`

### Payment table routing

Use this when the request mentions payment data but does not name the exact table.

- Legacy payment table: `mysql_prod.moe_payment.payment`
- Newer payment table: `pg_moego_data_payment_prod.public.payment`
- Do not assume payment version from context alone.
- If the request does not specify version and the fields do not disambiguate, ask one focused question.
- If the user provides fields that exist only in one version, infer the version and state the inference before querying.

## Output format

When returning results:

- Start with a 1-2 sentence conclusion.
- Name the database used and say whether the result came from the canonical path or a fallback, when relevant.
- Provide the SQL used or a compact excerpt.
- List assumptions, data quality concerns, and next checks.
- If confidence is low, say what additional data is needed.

## When to use me

Use this skill for MoeGo Redshift exploration, prod database routing, schema discovery,
metric debugging, anomaly triage, payment-table selection, and validated lookup queries.

## When not to use me

Do not attempt write operations or destructive maintenance (they will fail anyway as this is a read-only replica). Avoid unbounded full-table scans to maintain performance.
Ask one focused clarifying question only after narrowing the likely databases if the request is still materially ambiguous.
