"""
Функции для взаимодействия с внешним сервисом-провайдером данных о новостях.
"""
from http import HTTPStatus
from typing import Optional
from clients.base import BaseClient
from logger import trace_config
from settings import API_KEY_NEWSPORTAL

import aiohttp


class NewsClient(BaseClient):
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о новостях.
    """

    async def get_base_url(self) -> str:
        return "https://newsapi.org/v2/everything"

    async def _request(self, endpoint: str) -> Optional[dict]:

        async with aiohttp.ClientSession(trace_configs=[trace_config]) as session:
            async with session.get(endpoint) as response:
                if response.status == HTTPStatus.OK:
                    return await response.json()
                return None

    async def get_news(self, country: str) -> Optional[dict]:
        """
        Получение новостей по стране

        :param country: Страна
        :return:
        """

        endpoint = "{base_url}?q={country}&sortBy=publishedAt&apiKey={key}"
        return await self._request(
            endpoint.format(
                base_url=await self.get_base_url(),
                country=country,
                key=API_KEY_NEWSPORTAL,
            )
        )
