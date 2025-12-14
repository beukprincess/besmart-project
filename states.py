from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    wait_for_broadcast_content = State()