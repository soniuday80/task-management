from flask import request, jsonify
from auth.jwt_utils import get_current_user_id
from extentions import get_db
from emails.email import send_task_created_email, send_task_completed_email


def register_task_routes(app):

    @app.route('/tasks', methods=['POST'])
    def create_task():
        user_id = get_current_user_id()
        if user_id is None:
            return jsonify({"error": "unauthorized"}), 401

        data = request.get_json(silent=True) or {}
        title = (data.get("title") or "").strip()
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        if not title:
            return jsonify({"error": "title is missing"}), 400
        if not assigned_to:
            return jsonify({"error": "assigned_to is missing"}), 400

        db = get_db()
        cur = db.cursor()

        try:
            cur.execute("SELECT id, name, email FROM users WHERE id = %s", (assigned_to,))
            assignee_row = cur.fetchone()
        except Exception:
            db.rollback() 
            return jsonify({"error": "invalid assigned_to id"}), 400

        if assignee_row is None:
            return jsonify({"error": "assigned user does not exist"}), 400

        cur.execute(
            """
            INSERT INTO tasks (title, description, user_id, assigned_to)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, description, status, user_id, assigned_to, created_at
            """,
            (title, description, user_id, assigned_to)
        )
        task = cur.fetchone()
        db.commit()

        if str(user_id) != str(assigned_to):
            try:
                send_task_created_email(to=assignee_row['email'], task=task)
                pass
            except Exception as e:
                print("email failed:", e)

        return jsonify({
            "id": str(task["id"]),
            "title": task["title"],
            "description": task["description"],
            "status": task["status"],
            "created_by": str(task["user_id"]),
            "assigned_to": str(task["assigned_to"]),
            "created_at": task["created_at"].isoformat(),
        }), 201

    @app.route('/tasks', methods=['GET'])
    def list_tasks():
        user_id = get_current_user_id()
        if user_id is None:
            return jsonify({"error": "unauthorized"}), 401

        cur = get_db().cursor()
        cur.execute("""
            SELECT
                t.id, t.title, t.description, t.status, t.created_at,
                c.id AS creator_id, c.name AS creator_name,
                a.id AS assignee_id, a.name AS assignee_name
            FROM tasks t
            JOIN users c ON c.id = t.user_id
            JOIN users a ON a.id = t.assigned_to
            ORDER BY t.created_at DESC
        """)
        rows = cur.fetchall()

        return jsonify([
            {
                "id": str(r["id"]),
                "title": r["title"],
                "description": r["description"],
                "status": r["status"],
                "created_at": r["created_at"].isoformat(),
                "creator_id": str(r["creator_id"]),
                "creator_name": r["creator_name"],
                "assignee_id": str(r["assignee_id"]),
                "assignee_name": r["assignee_name"],
            }
            for r in rows
        ])

    @app.route('/tasks/<task_id>/complete', methods=['PATCH'])
    def complete_task(task_id):
        user_id = get_current_user_id()
        if user_id is None:
            return jsonify({"error": "unauthorized"}), 401

        db = get_db()
        cur = db.cursor()

        try:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'completed'
                WHERE id = %s AND assigned_to = %s AND status <> 'completed'
                RETURNING id, title, user_id
                """,
                (task_id, user_id)
            )
            task = cur.fetchone()
        except Exception:
            db.rollback()
            return jsonify({"error": "invalid task id"}), 400

        if task is None:
            return jsonify({"error": "task not found, not yours, or already completed"}), 404

        db.commit()

        try:
            cur.execute("SELECT email FROM users WHERE id = %s", (task["user_id"],))
            creator = cur.fetchone()
            if creator and str(task["user_id"]) != str(user_id):
                send_task_completed_email(to=creator['email'], task=task)
                pass
        except Exception as e:
            print("email failed:", e)

        return jsonify({"id": str(task["id"]), "status": "completed"}), 200