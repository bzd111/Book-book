#!/usr/bin python
# -*- coding: utf-8 -*-
import os
import smtplib
import logging
import logging.handlers
from urlparse import urljoin
from email.header import Header
from email.mime.text import MIMEText

import requests
from lxml import etree
from requests import ReadTimeout
from fake_useragent import UserAgent

from .config import (mail_to_list, mail_host, mail_user,
                     mail_pass, mail_postfix, ARTICLES_DICT,
                     YUAN_URL, SHENG_URL_1, YI_URL_1)

TIMEOUT = 5

log = logging.getLogger("utils")
log.info("utils.name: {}".format(__name__))

def send_mail(to_list, sub, content):
    me = "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype="plain", _charset='utf-8')
    msg['Subject'] = Header(sub, 'utf-8')
    msg['From'] = mail_user
    msg['To'] = ";".join(to_list)

    log.info("msg")
    log.info("{}, {}, {}".format(mail_user, mail_pass, mail_host))
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        log.info("send success: {}".format(1))
        return 1
    except Exception as e:
        log.exception("send error")
        return 0


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
            return fetch(url, retry=retry + 1)
        raise
    except ReadTimeout:
        mydict = vars()
        standby_url = mydict.get(mydict.keys()[mydict.values().index('b')] + '_1')
        return s.get(standby_url, timeout=TIMEOUT)


def get_tree(url):
    r = fetch(url)
    return etree.HTML(r.text)


def parser_url(url):
    log.info("parser url: {}".format(url))
    tree = get_tree(url)
    url_for = ""
    try:
        if "291" not in url:
            if not tree.xpath('//div[@id="list"]/dl/dd/a/@style')[-1]:
                url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-1]
            else:
                url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-2]
        else:
            if not tree.xpath('//div[@id="list"]/dl/dd/a/@style')[-1]:
                url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-6]
            else:
                url_for = tree.xpath('//div[@id="list"]/dl/dd/a/@href')[-7]
    except IndexError as e:
        log.error("parser url error: {}".format(e))
    finally:
        return urljoin(url, url_for)


def parser_article(url, name):
    log.info("parser_article: {}, {}".format(url, name))
    title = content = None
    tree = get_tree(url)
    try:
        title = tree.xpath('//div[@class="bookname"]/h1/text()')
        content = tree.xpath('//div[@id="content"]/text()')
    except Exception as e:
        print('parser_article', e)
    if title and content:
        title = title[0].encode('utf-8')
        title = ARTICLES_DICT[name] + title
        content = tree.xpath('//div[@id="content"]/text()')
        content = map(lambda x: x.encode('utf-8'), content)
        content = map(lambda x: x.replace("\u3000\u3000", ""), content)
        content = map(lambda x: x.replace("\r\n\t\t\t\t", ""), content)
        content = '\n'.join(content)
        # a = send_mail(mail_to_list, title, content)
        result = send_mail(mail_to_list, title, content)
        log.info("send result: {}".format(result))
        return result
