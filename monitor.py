import time
import psutil
import sendgrid
from sendgrid.helpers.mail import *
import configparser
import logging

config = configparser.ConfigParser()
config.optionxform = str
config.read('project.conf')

NETWORK_INTERFACE = config.get('Network', 'INTERFACE')
NETWORK_LIMIT = int(config.get('Network', 'LIMIT'))
NETWORK_MAX = int(config.get('Network', 'MAX'))
SENDGRID_API_KEY = config.get('Email', 'SENDGRID_API_KEY')
TIME_INTER = config.get('Misc', 'TIME_INTER')

loggingFile = logging.FileHandler('my.log', 'w', 'utf-8')

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[loggingFile, ])
def create_message(sender, to, subject, message_text):
  logging.info("send email::" + message_text)
  from_email = Email(sender)
  to_email = To(to)
  subject = subject
  content = Content("text/plain", message_text)
  return Mail(from_email, to_email, subject, content)


def send_message(service, message):
  return service.client.mail.send.post(request_body=message.get())

service = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

have_sent = False

while True:

  time.sleep(int(TIME_INTER))
  netio = psutil.net_io_counters(pernic=True)
  net_usage = netio[NETWORK_INTERFACE].bytes_sent + netio[NETWORK_INTERFACE].bytes_recv
  if net_usage > NETWORK_LIMIT and not have_sent:
    message = create_message(
      config.get('Email', 'from'),
      config.get('Email', 'to'),
      config.get('Email', 'subject'),
      'The network usage has exceeded the limit, Usage is %s bytes' %net_usage)
    send_message(service, message)
    print("[*]Network usage limit exceeded")
    print("[*]Mail sent to IT team")
    have_sent = True
