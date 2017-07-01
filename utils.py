#!/usr/bin python
# -*- coding: utf-8 -*-

from urlparse import urljoin

from lxml import etree
import requests
from fake_useragent import UserAgent

from config import (mail_to_list, mail_host, mail_user,
                    mail_pass, mail_postfix)


def send_mail(to_list, sub, content):

    me = "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype="plain")
    msg['Subject'] = Header(sub,'utf-8')
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print (str(e))
        return False


def get_user_agent():
    ua = UserAgent()
    return ua.random


def fetch(url, retry=0):
    pas = requests.Session()
    url = "http://www.biquge.cc/html/156/156129/"
    s.headers.update({'user-agent': get_user_agent(),
                      'referer': url})
    try:
        return s.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry+1)
        raise


def get_tree(url):
    r = fetch(url)
    tree = etree.HTML(r.text)
    if not tree.xpath('//a/@style')[-1]:
        url_for = tree.xpath('//a/@href')[-1]
    else:
        url_for = tree.xpath('//a/@href')[-2]
    return urljoin(url, url_for)
