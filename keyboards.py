from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def get_main_menu_kb(channels_text):
    builder = ReplyKeyboardBuilder()
    for i in channels_text:
        builder.add(KeyboardButton(text=str(i[0])))
    builder.adjust(2)
    return builder.as_markup()


def get_admin_inline_kb(question_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Принять",
        callback_data=f"accept_question:{question_id}")
    )
    builder.add(InlineKeyboardButton(
        text="Отклонить",
        callback_data=f"decline_question:{question_id}")
    )
    builder.add(InlineKeyboardButton(
        text="Забанить",
        callback_data=f"ban_user:{question_id}")
    )

    return builder.as_markup()


def get_admin_main_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Добавленные каналы'))
    builder.add(KeyboardButton(text='Рассылка'))
    builder.add(KeyboardButton(text='Информация'))
    return builder.as_markup(resize_keyboard=True)


def get_admin_channel_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Добавить канал",
        callback_data=f"add_channel")
    )
    builder.add(InlineKeyboardButton(
        text="Удалить канал",
        callback_data=f"view_channel")
    )
    return builder.as_markup()


def get_admin_cancel_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Назад",
        callback_data=f"cancel")
    )
    return builder.as_markup()


def get_user_new_question_kb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Да",
        callback_data=f"new_question")
    )
    return builder.as_markup()

