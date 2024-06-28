from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from src.http_errors import HTTPException, Error404
from src.services import product_api_service
from src.validators import id_validator


router = Router()


class GetProductStates(StatesGroup):
    id = State()


@router.message(Command('get_by_id'), StateFilter(default_state))
async def start_get_query(message: Message, state: FSMContext):
    await state.set_state(GetProductStates.id)
    await message.answer(
        text='Введите id продукта\n\n'
             'Чтобы отменить нажмите сюда: /cancel или введите эту команду вручную'
    )


@router.message(StateFilter(GetProductStates.id), id_validator)
async def id_sent(message: Message, state: FSMContext):
    entered_id = int(message.text.strip())
    await state.update_data(id=entered_id)

    try:
        product = await product_api_service.get_product(entered_id)
        await message.answer(text=f'{product.name} ({product.price} руб.)')
    except Error404:
        await message.answer(
            text='Продукт с таким id не найден'
        )
    except HTTPException as error:
        await message.answer(
            text=f'Что-то пошло не так\n\n'
                 f'Код ошибки: {error.status_code}'
        )


@router.message(StateFilter(GetProductStates.id))
async def warning_wrong_id(message: Message):
    await message.answer(
        text=f'id должен быть целым числом больше нуля.\n\n'
             f'Попробуйте еще раз.'
             'Чтобы отменить нажмите сюда: /cancel или введите эту команду вручную'
    )