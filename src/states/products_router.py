from aiogram import Router

from src.states.create_product import router as create_product_router
from src.states.get_product import router as get_product_router
from src.states.update_product import router as update_product_router
from src.states.default_commands import router as default_commands_router

router = Router()
router.include_routers(
    create_product_router,
    default_commands_router,
    get_product_router,
    update_product_router
)
