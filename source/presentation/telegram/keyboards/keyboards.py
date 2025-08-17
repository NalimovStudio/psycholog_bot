from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from source.presentation.telegram.callbacks.method_callbacks import (
    MethodCallback,
    CalmingCallback,
    VentingCallback,
    SubscriptionCallback,
    ProblemSolvingCallback,
)


class ButtonText:
    # Reply Keyboard
    START_DIALOG = "Начать диалог"
    SUPPORT_METHOD = "Метод поддержки"
    SUBSCRIPTION = "Подписка"

    # Inline Keyboard - Methods
    CALM_DOWN = "Успокоиться"
    CBT_DIARY = "КПТ (Дневник эмоций)"
    PROBLEM_SOLVING = "Потенциальное решение проблемы"
    VENT_OUT = "Высказаться"

    # Inline Keyboard - Calming flow
    ANOTHER_CYCLE = "ещё 1 цикл"
    FEEL_BETTER = "стало чуть легче"
    TO_TALK = "перейти к разговору"

    # Inline Keyboard - Venting summary
    SAVE = "Сохранить"
    DELETE = "Удалить"
    TO_CBT = "Превратить в запись дневника"

    # Inline Keyboard - Subscription
    RENEW_DISCOUNT = "Продлить со скидкой -40%"


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ButtonText.START_DIALOG)],
            [KeyboardButton(text=ButtonText.SUPPORT_METHOD)],
            [KeyboardButton(text=ButtonText.SUBSCRIPTION)],
        ],
        resize_keyboard=True,
    )


def get_support_methods_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=ButtonText.CALM_DOWN,
                callback_data=MethodCallback(name="calm").pack()
            )],
            [InlineKeyboardButton(
                text=ButtonText.CBT_DIARY,
                callback_data=MethodCallback(name="cbt").pack()
            )],
            [InlineKeyboardButton(
                text=ButtonText.PROBLEM_SOLVING,
                callback_data=MethodCallback(name="problem").pack()
            )],
            [InlineKeyboardButton(
                text=ButtonText.VENT_OUT,
                callback_data=MethodCallback(name="vent").pack()
            )],
        ]
    )


def get_calming_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ButtonText.ANOTHER_CYCLE,
                    callback_data=CalmingCallback(action="another_cycle").pack()
                ),
                InlineKeyboardButton(
                    text=ButtonText.FEEL_BETTER,
                    callback_data=CalmingCallback(action="feel_better").pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ButtonText.TO_TALK,
                    callback_data=CalmingCallback(action="to_talk").pack()
                )
            ],
        ]
    )


def get_venting_summary_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=ButtonText.SAVE, callback_data=VentingCallback(action="save").pack()),
                InlineKeyboardButton(text=ButtonText.DELETE, callback_data=VentingCallback(action="delete").pack()),
            ],
            [InlineKeyboardButton(
                text=ButtonText.TO_CBT,
                callback_data=VentingCallback(action="to_cbt").pack()
            )],
        ]
    )


def get_subscription_offer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=ButtonText.RENEW_DISCOUNT,
                callback_data=SubscriptionCallback(action="renew_discount").pack()
            )],
        ]
    )


def get_problem_solutions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Вариант 1",
                    callback_data=ProblemSolvingCallback(action="choose_option", option_id=0).pack()
                ),
                InlineKeyboardButton(
                    text="Вариант 2",
                    callback_data=ProblemSolvingCallback(action="choose_option", option_id=1).pack()
                ),
                InlineKeyboardButton(
                    text="Вариант 3",
                    callback_data=ProblemSolvingCallback(action="choose_option", option_id=2).pack()
                ),
            ]
        ]
    )


def get_back_to_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вернуться в меню")]
        ],
        resize_keyboard=True,
    )
