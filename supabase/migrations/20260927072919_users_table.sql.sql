
CREATE extension IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users(
    id uuid primary key default gen_random_uuid(),
    email text unique not null,
    name text not null,
    google_id text unique not null,
    created_at timestamp not null default now()
)