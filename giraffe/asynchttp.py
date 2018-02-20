""" Concurrent http requests """

from functools import partial
import asyncio
import aiohttp


async def async_fetch(url, data=None, verb='GET', limit_per_host=10):
    conn = aiohttp.TCPConnector(limit_per_host=limit_per_host)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.request(verb, url, data=data) as response:
            return await response.json()


def request(reqs, plimit=10):
    func = partial(async_fetch, limit_per_host=plimit)
    return asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*(asyncio.ensure_future(
                    func(**r)) for r in reqs)))


def make_req(url, verb='GET', data=None):
    return dict(url=url, verb=verb, data=data)
