from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command('cancel'), StateFilter(default_state))
async def cancel_command(message: Message):
    await message.answer(
        text="Отменять нечего"
    )


@router.message(Command('cancel'), ~StateFilter(default_state))
async def cancel_with_state_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Отменено"
    )
