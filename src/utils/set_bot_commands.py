from aiogram import types, Bot


async def set_bot_commands(bot: Bot):
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Запустить бота"),
        types.BotCommand(command="help", description="Помощь"),
        types.BotCommand(command="add", description="Добавить продукт"),
        types.BotCommand(command="get_by_id", description="Получить данные продукта по id"),
        types.BotCommand(command="update_by_id", description="Обновить данные продукта по id"),

    ])
