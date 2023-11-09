# email if cdd down more than x hours (6 hours default)
import smtplib
import psycopg2
from types import SimpleNamespace
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def fetch(cursor, query, single=True):
    cursor.execute(query)
    return cursor.fetchall()[0][0] if single else cursor.fetchall()

# Get all the info we need to send an email
LD_PROPERTY_OVERRIDE = """SELECT value FROM ld_property_override WHERE key = '{}'"""
SC = SimpleNamespace()
synaptic = psycopg2.connect(dbname='synaptic', user='seurat', host='localhost', port=3247).cursor()
SC.SMTP_HOST = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_HOST'))
SC.SMTP_PORT = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_PORT'))
SC.SMTP_USER = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_USER'))
SC.SMTP_FROM_ADDRESS = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_FROM_ADDRESS'))
SC.SMTP_PASSWORD = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_PASSWORD'))
SC.SMTP_USE_TLS = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_STARTTLS_ENABLE'))
SC.SMTP_AUTH = fetch(synaptic, LD_PROPERTY_OVERRIDE.format('SMTP_AUTH'))

# the send function
def send_email(to_addrs, email_title, email_body):
    mailer = smtplib.SMTP(host=SC.SMTP_HOST, port=587)
    mailer.starttls()
    mailer.login(SC.SMTP_USER, SC.SMTP_PASSWORD)

    message = MIMEMultipart()
    message.attach(MIMEText(email_body, 'html'))
    with open('LD.png', 'rb') as f:
        mime = MIMEBase('image', 'png', filename='LD.png')
        mime.add_header('Content-Disposition', 'attachment', filename='LD.png')
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        message.attach(mime)
    message['Subject'] = email_title
    message['From'] = SC.SMTP_FROM_ADDRESS
    message['To'] = to_addrs
    mailer.sendmail(SC.SMTP_FROM_ADDRESS, [to_addrs], message.as_string())

    mailer.quit()
