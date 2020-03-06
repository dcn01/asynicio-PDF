#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 10:28
# @Author  : ZhangChaowei
# @Site    : 
# @File    : download_pdf.py
# @Software: PyCharm

import requests
import aiohttp
import asyncio
import aiofiles
import time
import re


def read_data():
    with open('xxx/article_urls.txt', 'r', encoding='utf-8') as f:
        return [i.strip() for i in f.readlines()]


async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.content.read()
    await session.close()
    return result


async def download_data(url):
    print(f"waiting for: {url}")
    try:
        result = await get(url)
    except:
        print(f"下载超时: {url}")
    await store_data(url, result)
    print(f"写入数据完成: {url}")


async def store_data(filename, data):
    name = re.match(r'.*WP/(.*)\.pdf', filename).group(1)
    print(name)
    async with aiofiles.open(f'xxx/{name}.pdf', mode='wb') as f:
        await f.write(data)
        await f.close()


if __name__ == '__main__':
    start_time = time.time()
    urls = read_data()[1499:2000]
    tasks = [asyncio.ensure_future(download_data(url)) for url in urls]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print("last time: ", time.time() - start_time)






