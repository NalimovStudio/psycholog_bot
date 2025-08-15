import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from source.presentation.telegram.keyboards.keyboards import get_calming_keyboard
from source.presentation.telegram.states.user_states import SupportStates
from .support_methods.calming import CALMING_EXERCISE_TEXT

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(SupportStates.RISK_PROTOCOL)
async def handle_risk_protocol(message: Message, state: FSMContext):
    """
    Обрабатывает диалог, когда у пользователя обнаружен риск.
    Ведет пользователя по шагам протокола безопасности.
    """
    # Это упрощенный пошаговый протокол. В реальности потребовался бы более сложный NLP.
    current_data = await state.get_data()
    step = current_data.get("risk_step", 1)

    logger.warning(f"User {message.from_user.id} in RISK_PROTOCOL, step {step}. Msg: '{message.text[:30]}...'")

    if step == 1:
        # Пользователь ответил на первый вопрос ("Были ли мысли?"). Задаем второй.
        await state.update_data(risk_step=2)
        text = (
            "Спасибо, что сказал мне это. Это очень серьезно, и я здесь, чтобы помочь.\n\n"
            "<b>Есть ли у тебя конкретный план или средства? Находится ли сейчас рядом кто-то, кто может тебя поддержать?</b>"
        )
        await message.answer(text)

    elif step == 2:
        # Пользователь ответил на второй вопрос. Предоставляем номера помощи.
        await state.update_data(risk_step=3)
        text = (
            "Пожалуйста, не оставайся с этим один. Ты можешь получить помощь прямо сейчас.\n\n"
            "Позвони по номеру экстренной службы: <b>112</b> (в России и Европе) или <b>911</b> (в Северной Америке). "
            "Скажи оператору, что тебе нужна психологическая помощь.\n\n"
            "Пожалуйста, пообещай, что позвонишь или свяжешься с кем-то из близких прямо сейчас."
        )
        await message.answer(text)

    elif step == 3:
        # Последний шаг: пытаемся заземлить пользователя и передать в поток "Успокоиться".
        await state.set_state(SupportStates.CALMING)
        text = (
            "Я остаюсь здесь, с тобой. Твоя жизнь очень важна.\n\n"
            "Давай попробуем сфокусироваться на дыхании, чтобы немного успокоиться, пока ты ждешь помощи. "
            "Можем сделать упражнение на заземление."
        )
        await message.answer(text)
        await message.answer(CALMING_EXERCISE_TEXT, reply_markup=get_calming_keyboard())
