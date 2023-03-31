import os
import smtplib
import time
from concurrent.futures import ThreadPoolExecutor
from distutils.core import setup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import toml
from colorama import Fore, Style


class Sender:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password


    def connect(self):
        self.session = smtplib.SMTP(self.host, self.port)
        self.session.starttls()
        self.session.login(self.user, self.password)


    def send_email(self, sender_email, sender_name, target_email, subject, body):
        try:
            message = MIMEMultipart()
            message['From'] = f'{sender_name} <{sender_email}>'
            message['To'] = target_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))

            text = message.as_string()
            self.session.sendmail(sender_email, target_email, text)

            print(Fore.GREEN)

            print(f'[ Frost Sender ] - [ Email successfully sent to {target_email} ]')

            print(Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED)
            print(f'[ Frost Sender ] - [ Error sending email to {target_email}: {e} ]')
            print(Style.RESET_ALL)


def load_config(path):
    with open(path, 'r') as reader:
        return toml.loads(reader.read())
    

def load_email_list(path):
    with open(path, 'r') as reader:
        return [line.strip() for line in reader]


def load_html_body(path):
    with open(path, 'r', encoding='utf-8') as reader:
        return reader.read()


def delay_print(text: str, delay: float):
    for line in text.split("\n"):
        print(line)
        time.sleep(delay)


def main():
    config = load_config('config.toml')
    smtp_config = config["SMTP"]
    email_config = config["EMAIL"]
    
    host = smtp_config["host"]
    port = smtp_config["port"]
    user = smtp_config["user"]
    password = smtp_config["password"]

    sender_email = email_config["sender_email"]
    sender_name = email_config["sender_name"]
    subject = email_config["subject"]
    body_file = email_config["body_file"]
    emails_file = email_config["emails_file"]

    print(Fore.GREEN)

    print("")

    delay_print("""
          _______            _      _____                _           
         |  ____|           | |    / ____|              | | 
         | |__ _ __ ___  ___| |_  | (___   ___ _ __   __| | ___ _ __ 
         |  __| '__/ _ \/ __| __|  \___ \ / _ \ '_ \ / _` |/ _ \ '__|
         | |  | | | (_) \__ \ |_   ____) |  __/ | | | (_| |  __/ |   
         |_|  |_|  \___/|___/\__| |_____/ \___|_| |_|\__,_|\___|_|   
    """, 0.1)

    print(Style.RESET_ALL + "\n")

    time.sleep(1)
    delay_print("[ Frost Sender - Configuration Information ]", 0.03)
    time.sleep(0.1)

    print("----------------------------------------------")

    time.sleep(0.1)

    print("Host:", host)
    print("Port:", port)
    print("User:", user)
    print("Password:", "**********************")

    time.sleep(0.1)

    print("----------------------------------------------")

    time.sleep(0.1)

    body = load_html_body(body_file)
    emails = load_email_list(emails_file)

    print(f"Loaded body ({len(body)}B)")
    print(f"Loaded emails ({len(emails)})")

    print("----------------------------------------------")

    print("\nPress Enter to continue if the information is correct.")
    input()
    print("")

    threads = int(input('> Enter the desired number of threads: '))

    sender = Sender(host, port, user, password)
    sender.connect()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for email in emails:
            executor.submit(sender.send_email, sender_name, sender_email, email, subject, body, config)


if __name__ == '__main__':
    main()
