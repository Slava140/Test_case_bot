from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from api_schemas import ProductWithoutID
from src.http_errors import HTTPException, Error404
from src.services import product_api_service
from src.validators import id_validator, name_validator, price_validator
from src.strings import (
    http_error_answer,
    product_with_id_was_not_found,
    product_id_must_be_int_gt_0,
    product_name_must_be_str_ge_2_le_50_string_chars,
    enter_update_name,
    enter_update_price,
    do_you_want_save_updates,
    enter_id_for_update
)
from src.keyboards import inline_keyboard

router = Router()


class UpdateProductStates(StatesGroup):
    id = State()
    confirm_of_update = State()
    name = State()
    price = State()
    confirm_of_save = State()


@router.message(Command('update_by_id'), StateFilter(default_state))
async def start_update(message: Message, state: FSMContext):
    await state.set_state(UpdateProductStates.id)
    await message.answer(
        text=enter_id_for_update,
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(UpdateProductStates.id), id_validator)
async def id_sent(message: Message, state: FSMContext):
    entered_id = id_validator(message)
    try:
        product = await product_api_service.get_product(entered_id)
        await state.set_state(UpdateProductStates.confirm_of_update)
        await state.update_data(id=entered_id, name=product.name, price=product.price)
        await message.answer(
            text=f'Вы уверены, что хотите изменить этот продукт?\n'
                 f'{product.name} ({product.price} руб.)',
            reply_markup=inline_keyboard.confirm_yes_no_cancel
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


@router.message(StateFilter(UpdateProductStates.id))
async def warning_wrong_id(message: Message):
    await message.answer(
        text=product_id_must_be_int_gt_0,
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(UpdateProductStates.name), name_validator)
async def name_sent(message: Message, state: FSMContext):
    input_text = name_validator(message)
    await state.update_data(name=input_text)
    await state.set_state(UpdateProductStates.price)
    current_data = await state.get_data()
    await message.answer(
        text=f'Прекрасно! {enter_update_price(current_data.get("price"))}',
        reply_markup=inline_keyboard.update_cancel_skip
    )


@router.message(StateFilter(UpdateProductStates.name))
async def warning_wrong_name(message: Message):
    await message.answer(
        text=product_name_must_be_str_ge_2_le_50_string_chars,
        reply_markup=inline_keyboard.update_cancel_skip
    )


@router.message(StateFilter(UpdateProductStates.price), price_validator)
async def price_sent(message: Message, state: FSMContext):
    entered_price = price_validator(message)
    await state.update_data(price=entered_price)
    await state.set_state(UpdateProductStates.confirm_of_save)
    saved_data = await state.get_data()
    product = ProductWithoutID(name=saved_data.get('name'), price=saved_data.get('price'))
    await message.answer(
        text=do_you_want_save_updates(product),
        reply_markup=inline_keyboard.confirm_yes_no
    )


@router.callback_query(StateFilter(UpdateProductStates.confirm_of_update), F.data == 'accept')
async def confirm_of_update(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(UpdateProductStates.name)
    current_data = await state.get_data()
    await callback.message.edit_text(
        text=enter_update_name(current_data.get('name')),
        reply_markup=inline_keyboard.update_cancel_skip
    )


@router.callback_query(StateFilter(UpdateProductStates.confirm_of_update), F.data == 'reject')
async def not_confirm_of_update(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(UpdateProductStates.id)
    await callback.message.edit_text(
        text=enter_id_for_update,
        reply_markup=inline_keyboard.cancel
    )


@router.callback_query(StateFilter(UpdateProductStates.confirm_of_save), F.data == 'accept')
async def confirm_of_save_updates(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    input_data = await state.get_data()
    product_id = input_data.get('id')
    product = ProductWithoutID(**input_data)
    await state.clear()
    try:
        await product_api_service.update_product(product_id, product)
        await callback.message.edit_text(text=f'Данные успешно сохранены.')
    except HTTPException as error:
        await callback.message.answer(
            text=http_error_answer(status_code=error.status_code),
            reply_markup=inline_keyboard.cancel
        )


@router.callback_query(StateFilter(UpdateProductStates.name), F.data == 'skip')
async def skip_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(UpdateProductStates.price)
    current_data = await state.get_data()
    await callback.message.edit_text(
        text=enter_update_price(current_data.get('price')),
        reply_markup=inline_keyboard.update_cancel_skip
    )


@router.callback_query(StateFilter(UpdateProductStates.price), F.data == 'skip')
async def skip_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(UpdateProductStates.confirm_of_save)
    saved_data = await state.get_data()
    product = ProductWithoutID(name=saved_data.get('name'), price=saved_data.get('price'))
    await callback.message.edit_text(
        text=do_you_want_save_updates(product),
        reply_markup=inline_keyboard.confirm_yes_no
    )
