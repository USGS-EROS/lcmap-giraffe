""" Concurrent http requests """

from functools import partial
import asyncio
import aiohttp


async def async_fetch(sem, session, url, data=None, verb='GET'):
    async with sem:
        async with session.request(verb, url, data=data) as response:
            return await response.json()


async def gather(reqs, plimit=10):
    sema = partial(async_fetch, sem=asyncio.Semaphore(plimit))
    conn = aiohttp.TCPConnector(limit=plimit)
    async with aiohttp.ClientSession(connector=conn) as session:
        coroutines = (asyncio.ensure_future(
                      sema(session=session, **r)) for r in reqs)
        responses = await asyncio.gather(*coroutines)
    return responses


def request(reqs, plimit=10):
    return asyncio.get_event_loop().run_until_complete(gather(reqs, plimit))


def make_req(url, verb='GET', data=None):
    return dict(url=url, verb=verb, data=data)
