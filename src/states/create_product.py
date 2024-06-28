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


router = Router()


class CreateProductStates(StatesGroup):
    name = State()
    price = State()
    confirm = State()


@router.message(Command('create'), StateFilter(default_state))
async def start_creation(message: Message, state: FSMContext):
    await state.set_state(CreateProductStates.name)
    await message.answer(
        text='Введите название продукта\n\n'
             'Чтобы отменить создание нажмите сюда: /cancel или введите эту команду вручную'
    )


@router.message(StateFilter(CreateProductStates.name), name_validator)
async def name_sent(message: Message, state: FSMContext):
    input_text = message.text.strip()
    await state.update_data(name=input_text)
    await state.set_state(CreateProductStates.price)
    await message.answer(
        text='Спасибо!\n'
             'Теперь введите цену продукта в рублях\n\n'
             'Чтобы отменить создание нажмите сюда: /cancel или введите эту команду вручную')


@router.message(StateFilter(CreateProductStates.name), ~F.text.startswith('/'))
async def warning_wrong_name(message: Message):
    await message.answer(
        text='Название должно быть не меньше 2 и не больше 50 буквенных символов\n'
             'Вы можете попробовать еще раз\n\n'
             'Чтобы отменить создание нажмите сюда: /cancel или введите эту команду вручную'
    )


@router.message(StateFilter(CreateProductStates.price),
                price_validator)
async def price_sent(message: Message, state: FSMContext):
    await state.update_data(price=int(message.text.strip()))
    await state.set_state(CreateProductStates.confirm)

    entered_data = await state.get_data()
    product = ProductWithoutID(**entered_data)

    await message.answer(
        text=f'Название: {product.name}\n'
             f'Цена: {product.price}\n\n'
             f'Создать продукт с введенными данными?',
        reply_markup=inline_keyboard.confirm
    )


@router.message(StateFilter(CreateProductStates.price))
async def warning_wrong_price(message: Message):
    await message.answer(
        text='Цена должна быть целым числом больше нуля\n'
             'Вы можете попробовать еще раз\n\n'
             'Чтобы отменить создание нажмите сюда: /cancel или введите эту команду вручную'
    )


@router.callback_query(StateFilter(CreateProductStates.confirm), F.data == 'accept')
async def confirm_data(callback: CallbackQuery, state: FSMContext):
    product_dict = await state.get_data()
    input_product = ProductWithoutID(**product_dict)
    await state.clear()
    await callback.answer()
    try:
        await product_api_service.create_product(input_product)
        await callback.message.edit_text(
            text=f'Данные успешно сохранены.'
        )
    except HTTPException as error:
        await callback.message.edit_text(
            text=f'Что-то пошло не так.\n\n'
                 f'Код ошибки: {error.status_code}'
        )


@router.callback_query(StateFilter(CreateProductStates.confirm), F.data == 'reject')
async def not_confirm_data(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text='Отменено'
    )
