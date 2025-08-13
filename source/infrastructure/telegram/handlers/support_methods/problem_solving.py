import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from source.infrastructure.telegram.callbacks.method_callbacks import MethodCallback, ProblemSolvingCallback
from source.infrastructure.telegram.keyboards.keyboards import get_main_keyboard, get_problem_solutions_keyboard
from source.infrastructure.telegram.states.user_states import SupportStates

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(MethodCallback.filter(F.name == "problem"), SupportStates.METHOD_SELECT)
async def handle_problem_solving_method(query: CallbackQuery, state: FSMContext):
    logger.info(f"User {query.from_user.id} chose 'problem' method.")
    await state.set_state(SupportStates.PROBLEM_S1_DEFINE)
    text = "Давай разберем это по шагам. Сформулируй проблему в одном предложении."
    await query.message.edit_text(text)
    await query.answer()


@router.message(SupportStates.PROBLEM_S1_DEFINE)
async def handle_ps_s1_define(message: Message, state: FSMContext):
    await state.update_data(problem_definition=message.text)
    await state.set_state(SupportStates.PROBLEM_S2_GOAL)
    text = "Хорошо. А как ты поймешь, что проблема решена? Что будет твоим критерием успеха?"
    await message.answer(text)


@router.message(SupportStates.PROBLEM_S2_GOAL)
async def handle_ps_s2_goal(message: Message, state: FSMContext):
    data = await state.update_data(problem_goal=message.text)
    await state.set_state(SupportStates.PROBLEM_S3_OPTIONS)

    await message.answer("Спасибо. Я подумаю и предложу 3 варианта действий. Минутку...")
    #TODO Тут нужно решить заглушку и поставить нейронку на создании 3 вариантой решении проблемы
    solutions = [
        {
            "option": "Поговорить с другом о том, что беспокоит.",
            "pros": "Поддержка, другой взгляд.", "cons": "Может не быть времени/ресурсов у друга."
        },
        {
            "option": "Выделить 30 минут на прогулку на свежем воздухе.",
            "pros": "Смена обстановки, физическая активность.", "cons": "Может быть плохая погода."
        },
        {
            "option": "Записать все мысли о проблеме на бумаге.",
            "pros": "Помогает структурировать мысли.", "cons": "Может усилить зацикливание на проблеме."
        },
    ]
    await state.update_data(solutions=solutions)

    response_text = "Вот несколько вариантов:\n\n"
    for i, sol in enumerate(solutions):
        response_text += f"<b>Вариант {i+1}:</b> {sol['option']}\n"
        response_text += f"<i>Плюсы:</i> {sol['pros']}\n"
        response_text += f"<i>Риски:</i> {sol['cons']}\n\n"

    response_text += "Какой из вариантов тебе кажется наиболее подходящим сейчас?"
    await message.answer(response_text, reply_markup=get_problem_solutions_keyboard(solutions))


@router.callback_query(ProblemSolvingCallback.filter(F.action == "choose_option"), SupportStates.PROBLEM_S3_OPTIONS)
async def handle_ps_s3_choice(query: CallbackQuery, callback_data: ProblemSolvingCallback, state: FSMContext):
    await state.set_state(SupportStates.PROBLEM_S4_CHOICE)
    data = await state.get_data()
    chosen_option = data["solutions"][callback_data.option_id]
    await state.update_data(chosen_option=chosen_option)

    text = f"Отличный выбор. Теперь давай разобьем '{chosen_option['option']}' на самый маленький первый шаг, который можно сделать за 10-15 минут."
    await query.message.edit_text(text)
    await query.answer()


@router.message(SupportStates.PROBLEM_S4_CHOICE)
async def handle_ps_s4_step(message: Message, state: FSMContext):
    await state.update_data(problem_step=message.text)
    await state.set_state(SupportStates.PROBLEM_S5_PACT)
    text = "Супер. Это звучит как отличный, выполнимый шаг. Давай заключим 'пакт'. Когда ты планируешь это сделать? (Например, 'сегодня вечером' или 'завтра в 12:00')."
    await message.answer(text)


@router.message(SupportStates.PROBLEM_S5_PACT)
async def handle_ps_s5_pact(message: Message, state: FSMContext):
    await state.update_data(problem_pact=message.text)
    # TODO: Добавить логику для создания напоминания через APScheduler/Celery
    logger.info(f"User {message.from_user.id} finished Problem-Solving entry: {await state.get_data()}")
    await state.clear()
    text = "Договорились! Я верю, у тебя получится. Если хочешь, я могу напомнить тебе об этом. (Функция напоминаний в разработке).\n\nВозвращаю в главное меню."
    await message.answer(text, reply_markup=get_main_keyboard())
