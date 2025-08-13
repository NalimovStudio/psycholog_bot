from aiogram.filters.callback_data import CallbackData


class MethodCallback(CallbackData, prefix="method"):
    name: str  # calm, cbt, problem, vent


class CalmingCallback(CallbackData, prefix="calm"):
    action: str  # another_cycle, feel_better, to_talk


class VentingCallback(CallbackData, prefix="vent"):
    action: str  # save, delete, to_cbt


class SubscriptionCallback(CallbackData, prefix="sub"):
    action: str  # renew_discount


class ProblemSolvingCallback(CallbackData, prefix="problem_solving"):
    action: str  # e.g., 'choose_option'
    option_id: int
