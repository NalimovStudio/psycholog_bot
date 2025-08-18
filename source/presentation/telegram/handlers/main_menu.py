from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from source.core.lexicon.bot import PROFILE_TEXT, HELP_TEXT, SUBSCRIPTION_MENU_TEXT
from source.presentation.telegram.keyboards.keyboards import (
    ButtonText,
    get_subscriptions_menu_keyboard,
    get_help_keyboard,
)
from source.presentation.telegram.states.user_states import SupportStates

router = Router(name=__name__)


@router.message(F.text == ButtonText.START_DIALOG)
async def handle_start_dialog(message: Message, state: FSMContext):
    await state.set_state(SupportStates.CHECK_IN)
    text = (
        "Я рядом. Как ты себя чувствуешь сейчас? "
        "Если бы это было погодой — какой она была бы?"
    )
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


@router.message(F.text == ButtonText.HELP)
async def handle_help(message: Message):
    """
    Обрабатывает нажатие на кнопку 'Помощь'.
    Отправляет информационное сообщение с клавиатурой.
    """
    await message.answer(text=HELP_TEXT, reply_markup=get_help_keyboard())


@router.message(F.text == ButtonText.SUBSCRIPTION)
async def handle_subscription(message: Message):
    await message.answer(
        text=SUBSCRIPTION_MENU_TEXT,
        reply_markup=get_subscriptions_menu_keyboard()
    )


@router.message(F.text == ButtonText.PROFILE)
async def handle_profile(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "не указан"
    # Заглушка для типа подписки
    #TODO Решить заглушку
    subscription_type = "Бесплатная"

    text = PROFILE_TEXT.format(
        user_id=user_id,
        username=username,
        subscription_type=subscription_type,
    )
    await message.answer(text=text)
