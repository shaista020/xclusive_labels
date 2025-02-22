from django.core.mail import send_mail
from django.conf import settings

def send_ticket_update_email(user_email, username, ticket_title, message, status, sender):
    
    subject = f"Ticket Update: {ticket_title}"

    body = f"""
    Dear {username},

    Your ticket "{ticket_title}" has been updated.

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
