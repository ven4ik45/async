import asyncio
import aiohttp
from typing import Union
from more_itertools import chunked
from models import init_db, close_db, SwapiPeople, Session

CHUNK_SIZE = 10


async def fill_hero(hero_list: list):
    people_list = list()
    for person in hero_list:
        match person:
            case {'detail': detail}:
                continue
            case _:
                rm_list = ['created', 'edited', 'url']
                [person.pop(i) for i in rm_list]
                links_list = ['homeworld', 'films', 'species', 'starships', 'vehicles']
                coro = [handler_links(person.pop(i)) for i in links_list]
                result = await asyncio.gather(*coro)
                fix = dict(zip(links_list, result))
                people_list.append(SwapiPeople(**person, **fix))

    async with Session() as session:
        session.add_all(people_list)
        await session.commit()


async def handler_links(links: Union[str, list]) -> str:
    match links:
        case str():
            return await get_link(links)
        case list():
            result = list()
            for i in links:
                result.append(get_link(i))
            hero_data = await asyncio.gather(*result)
            return ", ".join(hero_data)


async def get_link(link: str):
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    response = await session.get(link)
    get_text = await response.json()
    await session.close()
    if 'title' in get_text:
        result = get_text.get('title')
    elif 'name' in get_text:
        result = get_text.get('name')
    return result


async def get_request(hero_id: int):
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
    response = await session.get(f'https://swapi.py4e.com/api/people/{hero_id}/')
    get_json = await response.json()
    await session.close()
    return get_json


async def main():
    await init_db()

    for hero_list in chunked(range(1, 89), CHUNK_SIZE):
        pre_request = list()
        for i in hero_list:
            coro = get_request(i)
            pre_request.append(coro)
        result = await asyncio.gather(*pre_request)
        asyncio.create_task(fill_hero(list(result)))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())
