#!/usr/bin/env python
import os
import subprocess
import smtplib
import socket
import datetime
import time
from email.mime.text import MIMEText


def start(action):
    os.system('. /lib/lsb/init-functions; log_begin_msg "' + action + ' ..."')


def success():
    os.system('. /lib/lsb/init-functions; log_progress_msg done; log_end_msg 0')


def fail():
    os.system('. /lib/lsb/init-functions; log_end_msg 1')


def get_hostname():
    return socket.gethostname()


def get_ipaddr():
    p = subprocess.Popen('ip route list', shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src') + 1]
    return ipaddr



def sendmail(smtp_setting, mail_setting, send_list):
    """
    Connect to smtp server, try several times, if smtp servers were
    successfully connected, then send the mail.
    """
    start('Connect to [' + smtp_setting['smtp_server'] + ']')
    try_max = 5
    try_times = 0
    try_delay = 1
    while try_times <= try_max:
        try_times += 1
        try:
            smtpserver = smtplib.SMTP(smtp_setting['smtp_server'],
                                      smtp_setting['smtp_port'])
            success()
            break
        except Exception, err:
            if try_times > try_max:
                fail()
                exit()
            else:
                time.sleep(try_delay)
                try_delay *= 2

    # Login to mail system
    start('Login with ( ' + mail_setting['mail_user'] + ' )')
    try:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(mail_setting['mail_user'],
                         mail_setting['mail_password'])
        success()
    except Exception, err:
        fail()
        exit()

    today = datetime.date.today()
    ipaddr = get_ipaddr()
    my_ip = 'Your ip is %s' % get_ipaddr()
    hostname = "The host %s" % get_hostname()
    start('Send ip mail ( ' + ipaddr + ' )')
    msg = MIMEText(hostname + '\n' + my_ip)
    msg['Subject'] = 'IP For' + hostname + 'on %s' % today.strftime('%b %d %Y')
    msg['From'] = mail_setting['mail_user']
    for send_user in send_list:
        msg['To'] = send_user
        try:
            smtpserver.sendmail(mail_setting['mail_user'],
                                [send_user], msg.as_string())
            success()
        except Exception, err:
            fail()
    smtpserver.quit()

if __name__ == '__main__':
    # smtp server settings
    smtp_setting = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
        }

    # Mail account settings
    mail_setting = {
        'mail_user': 'username@gmail.com',
        'mail_password': 'password'
        }

    send_to_list = [
        'username@gmail.com',
        'username2@gmail.com'
        ]

    sendmail(smtp_setting, mail_setting, send_to_list)
