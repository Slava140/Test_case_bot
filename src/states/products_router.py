from aiogram import Router

from src.states.add_product import router as add_product_router
from src.states.get_product import router as get_product_router
from src.states.update_product import router as update_product_router
from src.states.delete_product import router as delete_product_router
from src.states.default_commands import router as default_commands_router

router = Router()
router.include_routers(
    default_commands_router,
    add_product_router,
    get_product_router,
    update_product_router,
    delete_product_router,
)
