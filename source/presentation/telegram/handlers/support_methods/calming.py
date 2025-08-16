import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from source.presentation.telegram.callbacks.method_callbacks import MethodCallback, CalmingCallback
from source.presentation.telegram.keyboards.keyboards import (
    get_calming_keyboard,
    get_main_keyboard,
    get_support_methods_keyboard,
)
from source.presentation.telegram.states.user_states import SupportStates
from source.core.lexicon.bot import CALMING_EXERCISE_TEXT

logger = logging.getLogger(__name__)
router = Router(name=__name__)



@router.callback_query(MethodCallback.filter(F.name == "calm"), SupportStates.METHOD_SELECT)
async def handle_calm_down_method(query: CallbackQuery, state: FSMContext):
    logger.info(f"User {query.from_user.id} chose 'calm' method.")
    await state.set_state(SupportStates.CALMING)
    await query.message.edit_text(CALMING_EXERCISE_TEXT, reply_markup=get_calming_keyboard())
    await query.answer()


@router.callback_query(CalmingCallback.filter(), SupportStates.CALMING)
async def handle_calming_feedback(query: CallbackQuery, callback_data: CalmingCallback, state: FSMContext):
    action = callback_data.action
    logger.info(f"User {query.from_user.id} chose '{action}' in calming flow.")

    if action == "another_cycle":
        await query.answer("Хорошо, давай попробуем еще раз.")
        await query.message.edit_text(CALMING_EXERCISE_TEXT, reply_markup=get_calming_keyboard())

    elif action == "feel_better":
        await state.clear()
        await query.message.edit_text(
            "Я рад, что тебе стало немного легче. Помни, что ты можешь вернуться к этому упражнению в любой момент.",
            reply_markup=None
        )
        await query.message.answer(
            "Ты можешь выбрать другой метод или начать новый диалог.",
            reply_markup=get_main_keyboard()
        )
        await query.answer()

    elif action == "to_talk":
        await state.set_state(SupportStates.METHOD_SELECT)
        await query.message.edit_text(
            "Хорошо, давай вернемся к выбору. Что тебе могло бы помочь сейчас?",
            reply_markup=get_support_methods_keyboard()
        )
        await query.answer()
