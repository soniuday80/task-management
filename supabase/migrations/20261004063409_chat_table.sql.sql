CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS chat(
    id uuid primary key default gen_random_uuid(),
    user_id uuid references users(id) on delete cascade,
    message text not null,
    created_at timestamp not null default now()
)