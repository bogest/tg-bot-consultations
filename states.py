from aiogram.fsm.state import StatesGroup, State


class AskQuestion(StatesGroup):
    channel_name = State()
    question_text = State()


class InsertChannel(StatesGroup):
    channel_text = State()
    channel_id = State()
    channel_url = State()


class DeleteChannel(StatesGroup):
    channel_id = State()


class NewSending(StatesGroup):
    sending_text = State()