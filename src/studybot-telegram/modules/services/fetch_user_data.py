import grequests
import aiohttp
import jwt
import datetime
from os import getenv
from modules.misc.settings import days_of_week, user_id_file
from bs4 import BeautifulSoup

class fetchData:
    async def post(url: str, headers:dict[str]=None, data_row:str=None) -> tuple:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers = headers, data = data_row) as response:
                return await response.json(),  response.ok
    
    async def get(url: str, headers:dict[str]=None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers = headers) as response:
                return await response.json()
               