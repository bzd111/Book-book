import asyncio
import json
import logging
import logging.handlers
from asyncio.events import get_event_loop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # noqa
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Union
from urllib.parse import urljoin

import aiohttp
import aiosmtplib
import fake_useragent
from aiohttp import ClientSession
from lxml import html

from config import mail_port  # type: ignore
from config import URLS_DICT, mail_host, mail_pass, mail_to_list, mail_user

TIMEOUT = 50

log = logging.getLogger("utils")
log.info("utils.name: {}".format(__name__))


async def send_mail(title, content):
    log.info("send email: {}, {}, {}".format(mail_user, mail_pass, mail_host))
    try:
        message = EmailMessage()
        message["From"] = mail_user
        message["To"] = mail_to_list
        message["Subject"] = title + "✧(≖ ◡ ≖✿)"
        message.set_content(content)
        await aiosmtplib.send(
            message,
            hostname=mail_host,
            port=mail_port,
            use_tls=True,
            password=mail_pass,
            username=mail_user,
        )
    except Exception as e:
        log.exception("send error: {}".format(e))


def get_user_agent():
    fake_useragent.settings.DATA_DB = Path.cwd() / 'fake_useragent.json'
    ua = fake_useragent.UserAgent(cache=True)
    return ua.random


async def fetch(session: ClientSession, url, retry=0):
    # loop = asyncio.get_event_loop()
    # agent = await loop.run_in_executor(None, get_user_agent)
    # headers = {'user-agent': agent}
    # headers = {'user-agent': get_user_agent()}
    # try:
    #     r = await session.get(url, headers=headers, timeout=TIMEOUT)
    #     return {url: r.text()}
    # except Exception:
    #     if retry < 3:
    #         return await fetch(session, url, retry=retry + 1)
    #     raise
    # async with session.get(url, headers=headers, timeout=TIMEOUT) as r:
    try:
        async with session.get(url, timeout=TIMEOUT) as r:
            log.info(f'fetch url: {url}')
            resp = await r.text()
            return (url, resp)
    except asyncio.TimeoutError:
        if retry < 3:
            await fetch(session, url, retry=retry + 1)


async def get_resps(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def get_tree(resp):
    parse = html.fromstring(resp)
    return parse


async def parser_urls(urls, loop=None):
    if not loop:
        loop = get_event_loop()
    resps: Dict = await get_resps(urls)
    lastest_urls = []
    for resp in resps:
        url, text = resp
        parse = await loop.run_in_executor(None, get_tree, text)
        log.info("parser url: {}".format(url))
        try:
            last_urls = parse.xpath('//div[@id="list"]/dl/dd/a/@href')
            if last_urls:
                url_for = last_urls[-1]
        except IndexError as e:
            log.exception("parser url error: {}".format(e))
        finally:
            lastest_urls.append(urljoin(url, url_for))
    return lastest_urls


async def parser_articles(urls, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    lastest_urls = await parser_urls(urls)
    diff = await loop.run_in_executor(None, filter_url, 'urls.json', lastest_urls)
    resps = await get_resps(diff)
    title = content = None
    for resp in resps:
        url, text = resp
        name = await loop.run_in_executor(None, get_url, url)
        parse = await loop.run_in_executor(None, get_tree, text)
        try:
            title = parse.xpath('//div[@class="bookname"]/h1/text()')
            content = parse.xpath('//div[@id="content"]/text()')
        except Exception as e:
            log.exception('parser_article', e)
        if title and content:
            title = title
            content = parse.xpath('//div[@id="content"]/text()')
            content = map(lambda x: x.replace("\u3000\u3000", ""), content)
            content = map(lambda x: x.replace("\r\n\t\t\t\t", ""), content)
            content_str = '\n'.join(content)
            if "正在手打中" in content_str:
                log.info("正在手打中,尴尬")
                return False
            result = await send_mail(name + title[0], content_str)
            log.info("send result: {}".format(result))


def filter_url(file, new):
    fpath = Path.cwd() / file
    if not fpath.exists():
        fpath.touch()
    with open(fpath, 'r') as f:
        data = f.read()
        if not data:
            old = set()
        else:
            old = set(json.loads(data))
    diff = set(new) - set(old)
    with open(fpath, 'w') as f:
        json.dump(new, f)
    return list(diff)


def get_url(target: str) -> Union[str]:
    for url in URLS_DICT.keys():
        if target.startswith(url):
            return URLS_DICT[url]
    return ''
