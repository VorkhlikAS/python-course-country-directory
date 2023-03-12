"""
Тестирование функций клиента для получения информации о курсах валют.
"""

import pytest

from clients.currency import CurrencyClient


@pytest.mark.asyncio
class TestClientCountry:
    """
    Тестирование клиента для получения информации о валютах.
    """

    base_url = "https://api.apilayer.com/fixer/latest{params}"

    @pytest.fixture
    def client(self):
        return CurrencyClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url.format(params="")

    async def test_get_currency(self, mocker, client):
        mocker.patch("clients.currency.CurrencyClient._request")
        await client.get_rates()
        client._request.assert_called_once_with(
            self.base_url.format(params="?base=rub")
        )

        await client.get_rates("test")
        client._request.assert_called_with(self.base_url.format(params="?base=test"))
