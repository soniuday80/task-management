# Task Management App

A multi-user task management application with Google OAuth login, task creation and assignment between users, and email notifications on task creation and completion.

**Live URL (frontend):** `https://task-management-noxs.vercel.app/`

---

## Features

- Sign in with Google (OAuth 2.0)
- Create tasks and assign them to any registered user
- View all tasks with creator and assignee
- Mark a task complete (only the assignee can do this)
- Email notification sent to the assignee when a task is created (skipped if self-assigned)
- Email notification sent to the creator when a task is completed (skipped if self-completed)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router) + TypeScript + Tailwind CSS |
| Backend | Flask (Python) |
| Database | Supabase (Postgres) — used as a direct Postgres database only |
| Auth | Google OAuth 2.0, implemented directly in Flask using Authlib (not Supabase Auth) |
| Sessions | Custom-issued JWTs (HS256), verified on every protected request |
| Email | Gmail SMTP (`smtplib`), sent from an app-password-authenticated account |
| Frontend hosting | Vercel |
| Backend hosting | Railway |

---

## Architecture

```
┌──────────────┐        Google OAuth        ┌──────────────┐
│              │ ─────────────────────────▶ │              │
│   Browser    │                             │   Google     │
│  (Next.js)   │ ◀───────────────────────── │              │
└──────┬───────┘        auth code            └──────────────┘
       │
       │ 1. GET /auth/google/login  → redirect to Google
       │ 2. Google redirects back to Flask's /auth/google/callback
       │ 3. Flask exchanges the code for the user's Google profile,
       │    creates/finds a row in `users`, mints its own JWT,
       │    and redirects the browser back with the token
       │
       │  Authorization: Bearer <JWT> on every request after login
       ▼
┌──────────────┐                             ┌──────────────┐
│    Flask     │ ─── direct Postgres conn ─▶ │   Supabase   │
│   Backend    │ ◀────────────────────────  │  (Postgres)  │
│              │                             └──────────────┘
│              │
│              │ ─── SMTP (smtplib) ───────▶  Gmail → recipient inbox
└──────────────┘
```


### Database schema

**`users`**
| column | type | notes |
|---|---|---|
| id | uuid, primary key | generated via `gen_random_uuid()` |
| google_id | text, unique, not null | Google's account identifier |
| email | text, unique, not null | |
| name | text | may be null if Google didn't supply one |
| created_at | timestamptz | defaults to `now()` |

**`tasks`**
| column | type | notes |
|---|---|---|
| id | uuid, primary key | |
| title | text, not null | |
| description | text | nullable |
| status | text, not null | `'pending'` or `'completed'` |
| user_id | uuid, FK → users.id | the task's creator |
| assigned_to | uuid, FK → users.id | the task's assignee |
| created_at | timestamptz | defaults to `now()` |

Migrations live in `supabase/migrations/`.

---

## API Endpoints

All endpoints except the two auth routes require `Authorization: Bearer <token>`.

| Method | Path | Description |
|---|---|---|
| GET | `/auth/google/login` | Redirects to Google's OAuth consent screen |
| GET | `/auth/google/callback` | Handles Google's redirect, issues a JWT, redirects to frontend |
| GET | `/me` | Returns the current user's id (used to verify a token is valid) |
| GET | `/users` | Returns all registered users (id, name, email) — used to populate the assignee dropdown |
| GET | `/tasks` | Returns all tasks, joined with creator and assignee names |
| POST | `/tasks` | Creates a task. Body: `{ title, description, assigned_to }`. Creator is taken from the token, not the request body |
| PATCH | `/tasks/<task_id>/complete` | Marks a task complete. Only succeeds if the caller is the task's assignee |

---

## Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Supabase project (Postgres database)
- A Google Cloud Console OAuth 2.0 Client ID/Secret
- A Gmail account with an App Password (requires 2-Step Verification enabled)

### 1. Clone and configure environment variables

```bash
git clone <repo-url>
cd task-management
```

Copy `.env.example` to `backend/.env` and `frontend/.env.local`, and fill in real values. See `.env.example` for the full list of required variables.

### 2. Database

```bash
npm install -D supabase   # or brew install supabase/tap/supabase
npx supabase link --project-ref <your-project-ref>
npx supabase db push
```

This applies the migrations in `supabase/migrations/` to your Supabase project.

### 3. Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Runs on `http://localhost:5000`.

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs on `http://localhost:3000`.

### 5. Google Cloud Console setup

In your OAuth 2.0 Client's Authorized redirect URIs, add:
- `http://localhost:5000/auth/google/callback` (local dev)
- `<your production backend URL>/auth/google/callback` (production)

While the OAuth consent screen is in "Testing" mode, only accounts added under Test Users can log in.

---

## Deployment

- **Frontend**: deployed to Vercel, root directory `frontend/`, env var `NEXT_PUBLIC_API_URL` pointing at the live backend URL.
- **Backend**: deployed to Railway, root directory `backend/`, running via `gunicorn run:app --bind 0.0.0.0:$PORT`. All backend env vars (see `.env.example`) are set directly in Railway's dashboard, with a distinct `JWT_SECRET` from the one used locally.
- **Database**: hosted on Supabase, connected via a direct Postgres connection string (`DATABASE_URL`).


