from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.services import product_api_service
from src.http_errors import Error404, Error500

product_router = Router()


@product_router.message(Command('get_product'))
async def get_product_command(message: Message):
    product_id = int(message.text.split('/get_product')[-1].strip())
    try:
        product = await product_api_service.get_product(product_id)
        await message.answer(text=f"Product(id={product.id}, name={product.name}, price={product.price})")
    except Error404:
        await message.answer("Продукта с таким ID не существует")
    except (Error500, Exception) as e:
        print(e)
        await message.answer("Что-то пошло не так")



