from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

def sendEmail(email_type, recipient_email, context):
    def send():
        email_templates = {
            'password_reset': {
                'subject': "Password Reset Request",
                'template': 'email/resetPassword.html'
            },
            'driver_assignment': {
                'subject': "Your Assigned Driver Details",
                'template': 'email/driverDetail.html'
            }
        }

        # Get the email details
        email_config = email_templates.get(email_type)
        if not email_config:
            raise ValueError("Invalid email type provided.")

        # Render the HTML template with dynamic data
        html_content = render_to_string(email_config['template'], context)
        text_content = strip_tags(html_content)  # Fallback plain text email

        # Create email message
        email = EmailMultiAlternatives(email_config['subject'], text_content, 'your-email@gmail.com', [recipient_email])
        email.attach_alternative(html_content, "text/html")  # Attach HTML version
        email.send()

    threading.Thread(target=send).start()