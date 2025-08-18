import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.enums import ParseMode
from dishka.integrations.aiogram import FromDishka

from source.presentation.telegram.callbacks.method_callbacks import MethodCallback
from source.presentation.telegram.keyboards.keyboards import get_venting_summary_keyboard, get_main_keyboard
from source.presentation.telegram.states.user_states import SupportStates
from source.application.ai_assistant.ai_assistant_service import AssistantService
from source.application.message_history.message_history_service import MessageHistoryService
from source.core.schemas.assistant_schemas import ContextMessage

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(MethodCallback.filter(F.name == "vent"), SupportStates.METHOD_SELECT)
async def handle_vent_out_method(query: CallbackQuery, state: FSMContext):
    logger.info(f"User {query.from_user.id} chose 'vent' method.")
    await state.set_state(SupportStates.VENTING)
    text = "Можешь просто писать всё, как идёт. Я буду отвечать коротко и бережно.\n\nКогда захочешь закончить, отправь команду /stop."
    await query.message.edit_text(text, reply_markup=None)
    await query.answer()




@router.message(Command("stop"), SupportStates.VENTING)
async def handle_stop_venting(message: Message, state: FSMContext, history: FromDishka[MessageHistoryService]):
    user_id = message.from_user.id
    context_scope = "venting"
    logger.info(f"User {user_id} stopped venting session.")
    
    await state.clear()
    await history.clear_history(user_id, context_scope)
    
    await message.answer(
        "Хорошо, мы закончили. Что бы ты хотел сделать с этой беседой?",
        reply_markup=get_venting_summary_keyboard()
    )
    await message.answer("Возвращаю в главное меню.", reply_markup=get_main_keyboard())


@router.message(SupportStates.VENTING)
async def handle_venting_message(
        message: Message,
        state: FSMContext,
        assistant: FromDishka[AssistantService],
        history: FromDishka[MessageHistoryService]
):
    user_id = message.from_user.id
    context_scope = "venting"
    logger.info(f"User {user_id} is venting. Msg: '{message.text[:30]}...'")

    user_message = ContextMessage(role="user", message=message.text)
    await history.add_message_to_history(user_id, context_scope, user_message)
    message_history = await history.get_history(user_id, context_scope)

    try:
        response = await assistant.get_speak_out_response(
            message=message.text,
            context_messages=message_history
        )
        response_text = response.message
        
        ai_message = ContextMessage(role="assistant", message=response_text)
        await history.add_message_to_history(user_id, context_scope, ai_message)

        await message.answer(response_text)
    except Exception as e:
        logger.error(f"Ошибка при получение сообщения {user_id} в скопе {context_scope}: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")
