#!/usr/bin python
# -*- coding: utf-8 -*-

from urlparse import urljoin
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from lxml import etree
import requests
from fake_useragent import UserAgent

from book.config import (mail_to_list, mail_host, mail_user,
                         mail_pass, mail_postfix)

TIMEOUT = 5
ARTICLES_DICT = {
    'da_url': "大主宰  ",
    'sheng_url': "圣墟  ",
    'yi_url': "一念永恒  "
}

def send_mail(to_list, sub, content):

    me = "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype="plain")
    msg['Subject'] = Header(sub, 'utf-8')
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
    s = requests.Session()
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
    return etree.HTML(r.text)


def parser_url(url):
    tree = get_tree(url)
    if not tree.xpath('//div[@id="list"]/dl/dd/a/@style')[-1]:
        url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-1]
    else:
        url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-2]
    return urljoin(url, url_for)


def parser_article(url, name):
    # url = parser_url(url)
    tree = get_tree(url)
    title = tree.xpath('//div[@class="bookname"]/h1/text()')
    title = title[0].encode('raw_unicode_escape')
    title = ARTICLES_DICT[name] + title
    content = tree.xpath('//div[@id="content"]/text()')
    content = map(lambda x: x.encode('raw_unicode_escape'), content)
    content = map(lambda x: x.replace("\xa0\xa0\xa0\xa0", ""), content)
    content = '\n'.join(content)
    return send_mail(mail_to_list, title, content)
