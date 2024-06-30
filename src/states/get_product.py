from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from src.http_errors import HTTPException, Error404
from src.services import product_api_service
from src.validators import id_validator
from keyboards import inline_keyboard
from src.strings import http_error_answer, product_with_id_was_not_found, product_id_must_be_int_gt_0, enter_id


router = Router()


class GetProductStates(StatesGroup):
    id = State()


@router.message(Command('get_by_id'), StateFilter(default_state))
async def start_get_query(message: Message, state: FSMContext):
    await state.set_state(GetProductStates.id)
    await message.answer(
        text=enter_id,
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(GetProductStates.id), id_validator)
async def id_sent(message: Message, state: FSMContext):
    entered_id = id_validator(message)
    await state.update_data(id=entered_id)
    try:
        product = await product_api_service.get_product(entered_id)
        await state.clear()
        await message.answer(
            text=f'{product.name} ({product.price} руб.)'
        )
    except Error404:
        await message.answer(
            text=product_with_id_was_not_found,
            reply_markup=inline_keyboard.cancel
        )
    except HTTPException as error:
        await message.answer(
            text=http_error_answer(error.status_code),
            reply_markup=inline_keyboard.cancel
        )


@router.message(StateFilter(GetProductStates.id))
async def warning_wrong_id(message: Message):
    await message.answer(
        text=product_id_must_be_int_gt_0,
        reply_markup=inline_keyboard.cancel
    )
