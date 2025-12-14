from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    wait_for_broadcast_content = State()

class Registration(StatesGroup):
    waiting_for_payment = State()
    waiting_for_name = State()
    waiting_for_phone = State()