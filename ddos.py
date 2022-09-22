import socket
import struct
from datetime import datetime
import time
import psutil
import sendgrid
from sendgrid.helpers.mail import *
import configparser
import logging
import os
import base64
import sys



def create_message(sender, to, subject, message_text):
  logging.info("send email::" + message_text)
  from_email = Email(sender)
  to_email = To(to)
  subject = subject
  content = Content("text/plain", message_text)
  return Mail(from_email, to_email, subject, content)

config = configparser.ConfigParser()
config.optionxform = str
config.read('project.conf')
SENDGRID_API_KEY = config.get('Email', 'SENDGRID_API_KEY')

service = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)



def send_message(service, message):
  return service.client.mail.send.post(request_body=message.get())


have_sent = False


def mailer():

    with open('tcpdump.pcap', 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedfile = Attachment(
        FileContent(encoded_file),
        FileName('DDOS.pcap'),
        FileType('application/pdf'),
        Disposition('attachment')
    )

    message = create_message(
        config.get('Email', 'from'),
        config.get('Email', 'to'),
        config.get('Email', 'subject'),
        'DDOS attack was detected')
    message.attachment = attachedfile
    send_message(service, message)
    print("mail sent")


def ddos():
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)

    IP_count = {}

    time_stamp = {}


    blocked_ip = set()

    white_ip = ('127.0.0.1', '192.168.200.1', '10.0.0.1', '192.168.104.1')

    file_txt = open("DDOS.txt", 'w')

    script_timestamp = str(datetime.now())
    file_txt.writelines(script_timestamp)
    file_txt.writelines("\n")

    while True:
        pkt = s.recvfrom(2048)
        ip_time = datetime.now()
        ipheader = pkt[0][14:34]
        ip_hdr = struct.unpack("!8sB3s4s4s", ipheader)
        IP = socket.inet_ntoa(ip_hdr[3])

        if IP not in blocked_ip and IP not in white_ip:

            if IP in IP_count:
                IP_count[IP] = IP_count[IP] + 1
                if IP_count[IP] % 15 == 1:
                    time_stamp[IP] = ip_time

                if (IP_count[IP] == 15) and (ip_time - time_stamp[IP]).seconds < 120:
                    line = "DDOS attack is Detected: "
                    file_txt.writelines(line)
                    file_txt.writelines(IP)
                    file_txt.writelines("\n")
                    blocked_ip.add(IP)
                    print("[*]DDOS attack detected.")
                    cmd = "sudo tcpdump -s 0 -i eth0 -w tcpdump.pcap"
                    os.system(cmd)
                    if KeyboardInterrupt:
                        mailer()
                        print("[*]Mail regarding the incident sent")
                        sys.exit()

                if IP_count[IP] == 15:
                    IP_count[IP] = 0

            else:
                IP_count[IP] = 1

                if IP_count[IP] % 15 == 1:
                    time_stamp[IP] = ip_time


ddos()
