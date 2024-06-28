from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from src.http_errors import HTTPException
from src.services import product_api_service
from src.validators import id_validator


router = Router()


class UpdateProductStates(StatesGroup):
    id = State()
    name = State()
    price = State()


@router.message(Command('update'), StateFilter(default_state))
async def start_update(message: Message, state: FSMContext):
    await state.set_state(UpdateProductStates.id)
    await message.answer(
        text='Введите id продукта, который хотите изменить\n\n'
             'Чтобы отменить нажмите сюда: /cancel или введите эту команду вручную'
    )


@router.message(StateFilter(UpdateProductStates.id), id_validator)
async def id_sent(message: Message, state: FSMContext):
    entered_id = int(message.text.strip())
    await state.update_data(id=entered_id)

    try:
        product = await product_api_service.get_product(entered_id)
        await message.answer(
            text=f'{product.name} ({product.price}руб.)'
        )
    except HTTPException as error:
        await message.answer(
            text=f'Что-то пошло не так\n\n'
                 f'Код ошибки: {error.status_code}'
        )
