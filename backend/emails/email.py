import smtplib
from email.message import EmailMessage
from flask import current_app


def send(to , subject , body):
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = current_app.config["SMTP_USER"]
    message["To"] = to
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(current_app.config["SMTP_USER"], current_app.config["SMTP_PASSWORD"])
        server.send_message(message)

def send_task_created_email(to, task):
    send(to, f"New task assigned: {task['title']}",
          f"You've been assigned a task: {task['title']}\n\n{task.get('description') or ''}")

def send_task_completed_email(to, task):
    send(to, f"Task completed: {task['title']}",
          f"Your assigned task \"{task['title']}\" was marked complete.")