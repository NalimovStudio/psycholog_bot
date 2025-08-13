import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from source.infrastructure.telegram.callbacks.method_callbacks import MethodCallback, CalmingCallback
from source.infrastructure.telegram.keyboards.keyboards import (
    get_calming_keyboard,
    get_main_keyboard,
    get_support_methods_keyboard,
)
from source.infrastructure.telegram.states.user_states import SupportStates

logger = logging.getLogger(__name__)
router = Router(name=__name__)

CALMING_EXERCISE_TEXT = (
    "Давай попробуем технику <b>5-4-3-2-1</b>, чтобы вернуться в настоящий момент.\n\n"
    "• Назови <b>5 вещей</b>, которые ты видишь вокруг себя.\n"
    "• Назови <b>4 звука</b>, которые ты слышишь.\n"
    "• Назови <b>3 ощущения</b> в теле (например, касание одежды, поверхность под ногами).\n"
    "• Назови <b>2 запаха</b>, которые ты чувствуешь.\n"
    "• Назови <b>1 вещь</b>, которую ты можешь попробовать на вкус (или просто сделай глоток воды).\n\n"
    "Сделай это медленно, в своем темпе. Когда закончишь, нажми на кнопку ниже."
)


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
