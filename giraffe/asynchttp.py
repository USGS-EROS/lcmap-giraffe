""" Concurrent http requests """

from functools import partial
import asyncio
import aiohttp


async def async_fetch(url, data=None, verb='GET'):
    async with aiohttp.ClientSession() as session:
            async with session.request(verb, url, data=data) as response:
                return await response.json()


async def sema_fetch(sem, url, data=None, verb='GET'):
    async with sem:
        await async_fetch(url, data, verb)


def request(reqs, plimit=10):
    sem = asyncio.Semaphore(plimit)
    func = partial(sema_fetch, sem=sem)
    return asyncio.get_event_loop().run_until_complete(
                asyncio.gather(*(asyncio.ensure_future(
                    func(**r)) for r in reqs)))


def make_req(url, verb='GET', data=None):
    return dict(url=url, verb=verb, data=data)
