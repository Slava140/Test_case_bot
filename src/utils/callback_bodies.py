from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def cancel_callback_body(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        text='Отменено'
    )
