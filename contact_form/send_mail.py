from django.core.mail import send_mail
from django.conf import settings

def send_ticket_update_email(user_email, username, ticket_title, message, status, sender):
    
    subject = f"Ticket Update: {ticket_title}"

    # Generate dynamic email message based on action
    if status.lower() == "closed":
        action_message = f"Your ticket '{ticket_title}' has been closed by {sender}."
    elif status.lower() == "in progress":
        action_message = f"Your ticket '{ticket_title}' is now in progress. {sender} is working on it."
    elif status.lower() == "open":
        action_message = f"Your ticket '{ticket_title}' has been reopened by {sender}."
    else:
        action_message = f"Your ticket '{ticket_title}' has been updated by {sender} with a new reply."

    body = f"""
    Dear {username},

    {action_message}

    Status: {status}

    {sender} sent the following message:
    -----------------------------------
    {message}
    -----------------------------------

    You can check further details in your account.

    Best regards,  
    Support Team
    """

    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,   
            [user_email],   
            fail_silently=False
        )
        print(f"Email sent successfully to {user_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")
