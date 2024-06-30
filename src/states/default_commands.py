from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from src.utils.callback_bodies import cancel_callback_body

router = Router()


@router.callback_query(~StateFilter(default_state), F.data == 'cancel')
async def cancel_operation(callback: CallbackQuery, state: FSMContext):
    await cancel_callback_body(callback, state)
