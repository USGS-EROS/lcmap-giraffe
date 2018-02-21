""" Concurrent http requests """

from functools import partial
import asyncio
import aiohttp


async def async_fetch(sem, url, data=None, verb='GET'):
    async with aiohttp.ClientSession() as session:
        async with sem:
            async with session.request(verb, url, data=data) as response:
                return await response.json()


def request(reqs, plimit=10):
    sema = partial(async_fetch, sem=asyncio.Semaphore(plimit))
    return asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*(asyncio.ensure_future(
                    sema(**r)) for r in reqs)))


def make_req(url, verb='GET', data=None):
    return dict(url=url, verb=verb, data=data)
