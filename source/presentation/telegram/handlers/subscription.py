from aiogram import F, Router
from aiogram.types import CallbackQuery

from source.core.lexicon.bot import (
    SUBSCRIPTION_MENU_TEXT,
    STANDARD_SUB_DETAIL_TEXT,
    PRO_SUB_DETAIL_TEXT,
)
from source.presentation.telegram.callbacks.method_callbacks import SubscriptionCallback
from source.presentation.telegram.keyboards.keyboards import (
    get_subscriptions_menu_keyboard,
    get_standard_subscription_options_keyboard,
    get_pro_subscription_options_keyboard,
)

router = Router(name=__name__)


@router.callback_query(SubscriptionCallback.filter(F.menu == "main"))
async def handle_back_to_main_menu(query: CallbackQuery):
    await query.message.edit_text(
        text=SUBSCRIPTION_MENU_TEXT,
        reply_markup=get_subscriptions_menu_keyboard(),
    )
    await query.answer()


@router.callback_query(SubscriptionCallback.filter(F.menu == "standard"))
async def handle_standard_sub_menu(query: CallbackQuery):
    await query.message.edit_text(
        text=STANDARD_SUB_DETAIL_TEXT,
        reply_markup=get_standard_subscription_options_keyboard(),
    )
    await query.answer()


@router.callback_query(SubscriptionCallback.filter(F.menu == "pro"))
async def handle_pro_sub_menu(query: CallbackQuery):
    await query.message.edit_text(
        text=PRO_SUB_DETAIL_TEXT,
        reply_markup=get_pro_subscription_options_keyboard(),
    )
    await query.answer()


@router.callback_query(SubscriptionCallback.filter(F.menu == "buy"))
async def handle_buy_subscription(query: CallbackQuery, callback_data: SubscriptionCallback):
    sub_type = "Стандарт" if callback_data.sub_type == "standard" else "Pro"
    months = callback_data.months
    text = f"🎉 Спасибо за покупку подписки «{sub_type}» на {months} мес.! (Это заглушка)"

    await query.message.edit_text(text=text, reply_markup=None)
    await query.answer(text="Покупка совершена!", show_alert=True)
