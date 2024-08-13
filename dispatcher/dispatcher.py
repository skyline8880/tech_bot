from aiogram import Dispatcher

from router.router import router as main_router

dp = Dispatcher()
dp.include_router(main_router)
