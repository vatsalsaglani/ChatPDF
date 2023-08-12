import json
import asyncio
import aiohttp
from typing import List
from tqdm.auto import tqdm

# added to avoid ClientOSError: Cannot write to closing transport
semaphore = asyncio.Semaphore(10)


async def http_get(
    session: aiohttp.ClientSession, url: str, return_content=True, cnt: int = 0
):
    if cnt > 2:
        return None
    try:
        async with semaphore:
            async with session.get(url) as response:
                if return_content:
                    return await response.content.read()
                else:
                    return await response.json()
    except Exception as err:
        print(f"EXCEPTION: {str(err)}")
        cnt += 1
        return await http_get(session, url, return_content, cnt)


async def __con_http_get__(urls: List[str]):
    tasks = []
    results = []

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60)
    ) as session:  # Instantiate session here
        tasks = [http_get(session, url) for url in urls]

        with tqdm(total=len(urls)) as pbar:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                pbar.update(1)

    return results


def con_http_get(urls: List[str]):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(__con_http_get__(urls))
    return results
