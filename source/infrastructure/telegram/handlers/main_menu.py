from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from source.infrastructure.telegram.keyboards.keyboards import (
    ButtonText,
    get_support_methods_keyboard,
    get_subscription_offer_keyboard,
)
from source.infrastructure.telegram.states.user_states import SupportStates

router = Router(name=__name__)


@router.message(F.text == ButtonText.START_DIALOG)
async def handle_start_dialog(message: Message, state: FSMContext):
    await state.set_state(SupportStates.CHECK_IN)
    text = (
        "Я рядом. Как ты себя чувствуешь сейчас? "
        "Если бы это было погодой — какой она была бы?"
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(F.text == ButtonText.SUPPORT_METHOD)
async def handle_support_method(message: Message):
    text = "Выбери, как тебе помочь сейчас:"
    await message.answer(text=text, reply_markup=get_support_methods_keyboard())


@router.message(F.text == ButtonText.SUBSCRIPTION)
async def handle_subscription(message: Message):
    """
    Обрабатывает нажатие на кнопку 'Подписка'.
    Показывает информацию о подписке (заглушка).
    """
    # Это заглушка. 
    # Реальная логика будет проверять статус подписки пользователя.
    text = (
        "Сейчас у вас активна бесплатная подписка. "
        "Часть функций (дневник, напоминания, длинные сессии) может быть ограничена.\n\n"
        "Хотите получить полный доступ и поддержать проект?"
    )
    await message.answer(text=text, reply_markup=get_subscription_offer_keyboard())
