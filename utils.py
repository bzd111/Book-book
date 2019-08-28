#!/usr/bin python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
from urlparse import urljoin

import yagmail
import requests
from lxml import etree
from requests import Timeout
import fake_useragent

from .config import (mail_to_list, mail_host, mail_user, mail_pass, URLS_DICT)

TIMEOUT = 50

log = logging.getLogger("utils")
log.info("utils.name: {}".format(__name__))


def send_mail(to_list, title, content):
    log.info("{}, {}, {}".format(mail_user, mail_pass, mail_host))
    try:
        email = yagmail.SMTP(
            user=mail_user, password=mail_pass, host=mail_host)
        email.send(to_list, subject=[title, "✧(≖ ◡ ≖✿)"], contents=content)
        return True
    except Exception as e:
        log.exception("send error: {}".format(e.message))
        return False


def get_user_agent():
    fake_useragent.settings.DATA_DB = '/opt/Book-book/fake_useragent.json'
    ua = fake_useragent.UserAgent(cache=True)
    return ua.random


def fetch(url, retry=0):
    s = requests.Session()
    s.headers.update({'user-agent': get_user_agent(), 'referer': url})
    try:
        return s.get(url, timeout=TIMEOUT)
    except requests.exceptions.RequestException:
        if retry < 3:
            return fetch(url, retry=retry + 1)
        raise
    except Timeout:
        mydict = vars()
        standby_url = mydict.get(mydict.keys()[mydict.values().index('b')] +
                                 '_1')
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
        log.exception("parser url error: {}".format(e))
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
        log.exception('parser_article', e.message)
    if title and content:
        title = title[0].encode('utf-8')
        title = URLS_DICT[name][1] + title
        content = tree.xpath('//div[@id="content"]/text()')
        content = map(lambda x: x.encode('utf-8'), content)
        content = map(lambda x: x.replace("\u3000\u3000", ""), content)
        content = map(lambda x: x.replace("\r\n\t\t\t\t", ""), content)
        content_str = '\n'.join(content)
        if "正在手打中" in content_str:
            log.info("正在手打中,尴尬")
            return False
        result = send_mail(mail_to_list, title, content)
        log.info("send result: {}".format(result))
        return result
