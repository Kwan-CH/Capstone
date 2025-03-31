import smtplib

def sendEmail(password, target):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'noreplytoewastegov@gmail.com'
    smtp_password = 'yumk vxyf tdpa dtla'

    from_email = 'noreplytoewastegov@gmail.com'
    to_email = target
    subject = 'Reset Password Request'
    body = f'Your password has been reset \n New Password:{password}'

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(from_email, to_email, message)