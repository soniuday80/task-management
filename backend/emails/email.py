#import stmplib
import os
import resend


def send(to , subject , body):


    """
    SMTP email sender. 
    Note: Standard SMTP (port 465) is blocked by default on cloud hosts like Railway.
    Use this for local development or if your deployment environment supports SMTP.
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = current_app.config["SMTP_USER"]
    message["To"] = to
    message.set_content(body)
    """

    resend.api_key = os.getenv("RESEND_API_KEY")

    try:
        params = {
            "from": "onboarding@resend.dev",  # Resend's default test sender domain
            "to": [to],
            "subject": subject,
            "text": body,
        }
        
        response = resend.Emails.send(params)
        print(f"Email sent successfully via Resend: {response}")
        return True
    except Exception as e:
        print(f"Resend error: {e}")
        return False

    

def send_task_created_email(to, task):
    send(to, f"New task assigned: {task['title']}",
          f"You've been assigned a task: {task['title']}\n\n{task.get('description') or ''}")

def send_task_completed_email(to, task):
    send(to, f"Task completed: {task['title']}",
          f"Your assigned task \"{task['title']}\" was marked complete.")