import json

from aiohttp import ClientSession

from src.config import settings
from src.http_errors import Error404, Error500, Error422
from src.api_schemas import ProductWithID, ProductWithoutID


class ProductAPIService:
    def __init__(self):
        self.api_url = settings.API_URL

    async def get_product(self, product_id: int) -> ProductWithID:
        url = f"{self.api_url}{product_id}"
        async with ClientSession() as session:
            async with session.get(url) as response:
                match response.status:
                    case 404:
                        raise Error404(f"Продукт с ID {product_id} не найден")
                    case 500:
                        raise Error500(f"Произошла неизвестная ошибка")
                    case 200:
                        data = await response.json()
                        return ProductWithID(**data)

    async def create_product(self, product: ProductWithoutID) -> ProductWithID:
        url = self.api_url
        async with ClientSession() as session:
            async with session.post(url=url, json=product.model_dump()) as response:
                match response.status:
                    case 422:
                        raise Error422(f"Произошла ошибка валидации")
                    case 500:
                        raise Error500("Произошла неизвестная ошибка")
                    case 201:
                        data = await response.json()
                        return ProductWithID(**data)

    async def update_product(self, product_id, product: ProductWithoutID) -> ProductWithID:
        url = self.api_url
        async with ClientSession() as session:
            async with session.put(url=url, data=product.model_dump()) as response:
                match response.status:
                    case 404:
                        raise Error404(f"Продукт с ID {product_id} не найден")
                    case 422:
                        raise Error422(f"Произошла ошибка валидации")
                    case 500:
                        raise Error500("Произошла неизвестная ошибка")
                    case 201:
                        data = await response.json()
                        return ProductWithID(**data)


product_api_service = ProductAPIService()
