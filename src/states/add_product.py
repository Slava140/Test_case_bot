from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from src.http_errors import HTTPException
from src.api_schemas import ProductWithoutID

from src.keyboards import inline_keyboard
from src.services import product_api_service
from src.validators import name_validator, price_validator
from src.strings import (
    http_error_answer,
    product_name_must_be_str_ge_2_le_50_string_chars,
    price_must_be_int_gt_0,
    do_you_want_create
)

router = Router()


class CreateProductStates(StatesGroup):
    name = State()
    price = State()
    confirm = State()


@router.message(Command('add'), StateFilter(default_state))
async def start_creation(message: Message, state: FSMContext):
    await state.set_state(CreateProductStates.name)
    await message.answer(
        text='Пожалуйста, введите название продукта.',
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(CreateProductStates.name), name_validator)
async def name_sent(message: Message, state: FSMContext):
    input_text = message.text.strip()
    await state.update_data(name=input_text)
    await state.set_state(CreateProductStates.price)
    await message.answer(
        text='Хорошо, теперь цену в рублях',
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(CreateProductStates.name))
async def warning_wrong_name(message: Message):
    await message.answer(
        text=product_name_must_be_str_ge_2_le_50_string_chars,
        reply_markup=inline_keyboard.cancel
    )


@router.message(StateFilter(CreateProductStates.price),
                price_validator)
async def price_sent(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text.strip()))
    await state.set_state(CreateProductStates.confirm)

    entered_data = await state.get_data()
    product = ProductWithoutID(**entered_data)

    await message.answer(
        text=do_you_want_create(product),
        reply_markup=inline_keyboard.confirm_yes_no
    )


@router.message(StateFilter(CreateProductStates.price))
async def warning_wrong_price(message: Message):
    await message.answer(
        text=price_must_be_int_gt_0,
        reply_markup=inline_keyboard.cancel
    )


@router.callback_query(StateFilter(CreateProductStates.confirm), F.data == 'accept')
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    product_dict = await state.get_data()
    input_product = ProductWithoutID(**product_dict)
    await state.clear()
    try:
        product = await product_api_service.create_product(input_product)
        await callback.message.edit_text(
            text=f'Данные успешно сохранены.\n'
                 f'id созданного продукта: {product.id}')
    except HTTPException as error:
        await callback.message.answer(
            text=http_error_answer(status_code=error.status_code),
            reply_markup=inline_keyboard.cancel
        )


@router.callback_query(StateFilter(CreateProductStates.confirm), F.data == 'reject')
async def not_confirm_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text='Отменено'
    )
