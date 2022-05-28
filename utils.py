import asyncio
import json
import logging
import logging.handlers
from asyncio.events import get_event_loop
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor  # noqa
from email.message import EmailMessage
from multiprocessing import cpu_count
from pathlib import Path
from urllib.parse import urljoin

import aiofiles
import aiohttp
import aiosmtplib
import fake_useragent
from lxml import html

from config import mail_port  # type: ignore
from config import JSON_FILE, mail_host, mail_pass, mail_to_list, mail_user

TIMEOUT = 5

log = logging.getLogger("utils")
log.info("utils.name: {}".format(__name__))


executor = ThreadPoolExecutor(max_workers=2 * cpu_count() + 1)


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


# async def fetch(session: ClientSession, url, retry=0):
async def fetch(url, retry=0):
    loop = asyncio.get_event_loop()
    agent = await loop.run_in_executor(executor, get_user_agent)
    headers = {'user-agent': agent}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as r:
                # async with session.get(url, headers={}, timeout=TIMEOUT) as r:
                log.debug(f'fetch url: {url}')
                resp = await r.read()
                return resp
    except (aiohttp.ServerDisconnectedError, ConnectionResetError, asyncio.TimeoutError):
        if retry < 3:
            await fetch(url, retry=retry + 1)
        raise


async def get_resp(url):
    resp = await fetch(url)
    return resp


def get_tree(resp):
    parse = html.fromstring(resp)
    return parse


async def parser_url(url, loop=None):
    if not loop:
        loop = get_event_loop()
    resp = await get_resp(url)
    parse = await loop.run_in_executor(executor, get_tree, resp)
    log.info("parser url: {}".format(url))
    try:
        last_urls = parse.xpath('//div[@id="list"]/dl/dd/a/@href')
        if last_urls:
            url_for = last_urls[-1]
            return urljoin(url, url_for)
    except IndexError as e:
        log.exception("parser url error: {}".format(e))


async def parser_article(name, url, loop=None):
    if not loop:
        loop = asyncio.get_event_loop()
    lastest_url = await parser_url(url)
    need_update = await filter_url(name, lastest_url)
    if need_update:
        resp = await get_resp(lastest_url)
        parse = await loop.run_in_executor(executor, get_tree, resp)
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
                return
            else:
                result = await send_mail(name + title[0], content_str)
                log.info("send result: {}".format(result))
                await save_lastest_url(name, lastest_url)


async def filter_url(name, url):
    if not JSON_FILE.exists():
        JSON_FILE.touch()
        return False
    async with aiofiles.open(JSON_FILE, mode='r') as f:
        contents = await f.read()
        if not contents:
            return True
        name_urls = json.loads(contents)
        last_url = name_urls.get(name)
        if not last_url:
            return True
        if last_url and last_url != url:
            return True
    return False


async def save_lastest_url(name, url):
    async with aiofiles.open(JSON_FILE, mode='r') as f:
        contents = await f.read()
        if not contents:
            name_urls = {}
            name_urls[name] = url
        else:
            name_urls = json.loads(contents)
    async with aiofiles.open(JSON_FILE, mode='w') as f:
        name_urls[name] = url
        await f.write(json.dumps(name_urls))
