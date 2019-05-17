import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import join
from string import Template

with open(join("omniscientus", "utils", "emails", "outlook-info"), "r", encoding="utf-8") as f:
    OUTLOOK_INFO = f.readline().split()


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_verification_email(to_name, to_email, confirmation_url):
    domain = "http://127.0.0.1:5000"
    message_template = read_template(join("omniscientus", "utils", "emails", "verification_message.html"))

    # set up the SMTP server
    try:
        s = smtplib.SMTP('smtp-mail.outlook.com', 587)
    except ConnectionError as e:
        print(e)
        s = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
    s.starttls()
    s.login(OUTLOOK_INFO[0], OUTLOOK_INFO[1])

    msg = MIMEMultipart()  # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=to_name, CONFIRMATION_URL=(domain + confirmation_url))

    # Prints out the message body for our sake
    # print(message)

    # setup the parameters of the message
    msg['From'] = OUTLOOK_INFO[0]
    msg['To'] = to_email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Nakkar2 Onaylama e-Postası"

    # add in the message body
    msg.attach(MIMEText(message, 'html'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
