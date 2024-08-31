import asyncio
import logging

from aiogram import Bot, Dispatcher
from middlewares_learning_bot.config_data.config import Config, load_config
from middlewares_learning_bot.handlers.other import other_router
from middlewares_learning_bot.handlers.user import user_router
from middlewares_learning_bot.middlewares.inner import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from middlewares_learning_bot.middlewares.outer import (
    FirstOuterMiddleware,
    SecondOuterMiddleware,
    ThirdOuterMiddleware,
)
from middlewares_learning_bot.middlewares.i18n import TranslatorMiddleware
from middlewares_learning_bot.lexicon.lexicon_en import LEXICON_EN
from middlewares_learning_bot.lexicon.lexicon_ru import LEXICON_RU


translations = {
    'default': 'ru',
    'en': LEXICON_EN,
    'ru': LEXICON_RU,
}

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main() -> None:
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Здесь будем регистрировать миддлвари
    dp.update.middleware(TranslatorMiddleware())
    dp.update.outer_middleware(FirstOuterMiddleware())
    user_router.callback_query.outer_middleware(SecondOuterMiddleware())
    other_router.message.outer_middleware(ThirdOuterMiddleware())
    user_router.message.middleware(FirstInnerMiddleware())
    user_router.callback_query.middleware(SecondInnerMiddleware())
    other_router.message.middleware(ThirdInnerMiddleware())

    # Запускаем polling
    await dp.start_polling(bot, _translations=translations)


if __name__ == '__main__':
    asyncio.run(main())
