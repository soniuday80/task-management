-- uuid_generate_v4() is not available in Supabase, so we use gen_random_uuid() instead
CREATE extension IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS tasks(
    id uuid primary key default gen_random_uuid(),
    title text not null,
    description text,
    status text default 'pending',
    creater_id uuid references users(id) on delete cascade,
    assigned_to uuid references users(id) on delete set null,
    created_at timestamp not null default now()
)