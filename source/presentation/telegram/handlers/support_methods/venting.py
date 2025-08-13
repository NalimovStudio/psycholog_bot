import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from source.presentation.telegram.callbacks.method_callbacks import MethodCallback
from source.presentation.telegram.keyboards.keyboards import get_venting_summary_keyboard, get_main_keyboard
from source.presentation.telegram.states.user_states import SupportStates

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
async def handle_stop_venting(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} stopped venting session.")
    # TODO: В будущем здесь можно добавить логику для сохранения диалога.
    await state.clear()
    await message.answer(
        "Хорошо, мы закончили. Что бы ты хотел сделать с этой беседой?",
        reply_markup=get_venting_summary_keyboard()
    )
    # После выбора на инлайн-клавиатуре, нужно будет вернуть основную клавиатуру.
    # Пока просто выводим ее следующим сообщением.
    await message.answer("Возвращаю в главное меню.", reply_markup=get_main_keyboard())


@router.message(SupportStates.VENTING)
async def handle_venting_message(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} is venting. Msg: '{message.text[:30]}...'")

    response_text = "Спасибо, что делишься. Я рядом и слышу тебя." #TODO, Пока стоит заглушка, нужно сделать бота, что бы принимал сообщения
    await message.answer(response_text)
