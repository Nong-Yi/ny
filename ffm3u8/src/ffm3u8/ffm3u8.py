import requests
import aiohttp
import asyncio
import aiofiles
from Crypto.Cipher import AES


async def download(url, session, line, op, headers):
    async with session.get(url=url, headers=headers) as resp:
        reader = resp.content
        data = await reader.read()
        data_bytes = data
    async with aiofiles.open(f'{op}{line}.ts', mode="wb") as f:
        await f.write(data_bytes)
    print(f"{url}下载完毕")


async def aio_download(name, name2, op, headers):
    tasks = []
    timeout = aiohttp.ClientTimeout(total=10000)
    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with aiofiles.open(f'{name}', mode="r", encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                else:
                    line = line.strip()
                    line2 = name2 + line
                    li = line.split('/')[-1]
                    task = asyncio.create_task(download(url=line2, session=session, line=li, op=op, headers=headers))
                    tasks.append(task)

                await asyncio.wait(tasks)


async def get_key(key, op, line):
    async with aiofiles.open(f'{op}{line}', mode='rb') as f:
        ts_data = await f.read()
    cipher = AES.new(key, mode=AES.MODE_CBC, IV=b"0000000000000000")
    decrypt_data = cipher.decrypt(ts_data)
    async with aiofiles.open(f'{op}{line}', mode='wb') as f1:
        await f1.write(decrypt_data)
    await f1.close()


async def download_key(url, session, headers, key, op, line):
    tasks = []
    async with session.get(url=url, headers=headers) as resp:
        reader = resp.content
        data = await reader.read()
        data_bytes = data
    async with aiofiles.open(f'{op}{line}', mode="wb") as f:
        await f.write(data_bytes)
    print(f"{url}下载完毕")
    task = asyncio.create_task(get_key(key=key, op=op, line=line))
    tasks.append(task)

    await asyncio.wait(tasks)


async def aio_download_key(name, name2, op, headers, key):
    tasks = []
    timeout = aiohttp.ClientTimeout(total=10000)
    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        async with aiofiles.open(f'{name}', mode="r", encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                else:
                    line = line.strip()
                    line2 = name2 + line
                    li = line.split('/')[-1]
                    task = asyncio.create_task(
                        download_key(url=line2, session=session, op=op, headers=headers, key=key, line=li))
                    tasks.append(task)

                await asyncio.wait(tasks)


def get_url_key(key_url):
    keyurls = requests.get(key_url)
    keyurl = keyurls.text
    keyurl2 = str(keyurl)
    key = str.encode(keyurl2)
    return key


def get_aio_url(name, name2, op, headers):
    asyncio.run(aio_download(name, name2, op, headers))


def get_aio_url_key(name, name2, op, headers, key_url):
    key = get_url_key(key_url)
    asyncio.run(aio_download_key(name=name, name2=name2, op=op, headers=headers, key=key))


if __name__ == '__main__':
    pass
