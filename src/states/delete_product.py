from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from src.http_errors import HTTPException, Error404
from src.services import product_api_service
from src.validators import id_validator
from src.keyboards import inline_keyboard
from src.strings import http_error_answer, product_with_id_was_not_found, product_id_must_be_int_gt_0, enter_id
from src.utils.callback_bodies import cancel_callback_body

router = Router()


class DeleteProductStates(StatesGroup):
    id = State()
    confirm = State()


@router.message(Command('delete_by_id'), StateFilter(default_state))
async def start_delete_query(message: Message, state: FSMContext):
    await state.set_state(DeleteProductStates.id)
    await message.answer(
        text=enter_id,
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(DeleteProductStates.id), id_validator)
async def id_sent(message: Message, state: FSMContext):
    entered_id = id_validator(message)
    await state.update_data(id=entered_id)
    try:
        product = await product_api_service.get_product(entered_id)
        await state.set_state(DeleteProductStates.confirm)

        await message.answer(
            text=f'Вы уверены, что хотите удалить этот продукт?\n'
                 f'{product.name} ({product.price} руб.)',
            reply_markup=inline_keyboard.confirm_yes_no
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


@router.message(StateFilter(DeleteProductStates.id))
async def warning_wrong_id(message: Message):
    await message.answer(
        text=product_id_must_be_int_gt_0,
        reply_markup=inline_keyboard.cancel
    )


@router.callback_query(StateFilter(DeleteProductStates.confirm), F.data == 'accept')
async def confirm_of_delete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    product_id = data.get('id')
    await state.clear()

    try:
        await product_api_service.delete_product(product_id)
        await callback.message.edit_text(text='Успешно удалено!')

    except HTTPException as error:
        await callback.message.answer(
            text=http_error_answer(status_code=error.status_code),
            reply_markup=inline_keyboard.cancel
        )


@router.callback_query(StateFilter(DeleteProductStates.confirm), F.data == 'reject')
async def not_confirm_of_delete(callback: CallbackQuery, state: FSMContext):
    await cancel_callback_body(callback, state)
