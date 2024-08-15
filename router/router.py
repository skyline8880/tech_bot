from aiogram import Router

from handlers.autorization.authorization import router as authorization_router
from handlers.commands.commands import router as commands_router
from handlers.report_stat.report_stat import router as report_stat_router
from handlers.requests.requests import router as requests_router
from handlers.users.users import router as users_router

router = Router()

router.include_routers(
    commands_router,
    authorization_router,
    users_router,
    requests_router,
    report_stat_router
)
