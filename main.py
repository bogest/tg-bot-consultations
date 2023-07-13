import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink

from settings import BOT_TOKEN, ADMIN_CHAT, ADMIN_ID
from db import Database
from keyboards import *
from states import *
from const_func import get_unix


# Базовые параметры
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database('storage_bot.db')


########################################################################################################################
############################################ КЛИЕНТСКАЯ ЧАСТЬ ##########################################################
@dp.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        await message.answer("<b>Добро пожаловать в админ панель!</b>\n"
                             "Выберите необходимое действие:\n",
                              reply_markup=get_admin_main_kb(),
                              parse_mode="HTML")
    except Exception as e:
        print(e)


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        if not db.get_banned_userx(message.from_user.id):
            channel_text = db.get_all_channels_text()
            await message.answer('Привет🖐🏻Выбери нужный канал, нажми на кнопку, задай свой вопрос⤵️\n'
                                 'Внимание ☝🏻Бот только принимает и размещает вопросы! Ответы поступают в чат!\n'
                                 'Вопросы или заказать рекламу ➡️ @alina_tech',
                                 reply_markup=get_main_menu_kb(channel_text),
                                 parse_mode="HTML"
                                 )
            if not db.check_user_exist(message.from_user.id):
                db.add_userx(message.from_user.id)
            await state.set_state(AskQuestion.channel_name)
    except Exception as e:
        print(e)


@dp.message(AskQuestion.channel_name, F.text.startswith('Задать вопрос'))
async def user_set_channel(message: types.Message, state: FSMContext):
    try:
        if not db.get_banned_userx(message.from_user.id):
            await state.update_data(channel=message.text)
            await message.answer('<b>✍🏻 Напиши свой вопрос в этом сообщении ⤵️</b>',
                             parse_mode='HTML')
            await state.set_state(AskQuestion.question_text)
    except Exception as e:
        print(e)


@dp.message(AskQuestion.question_text)
async def user_set_text(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        channel = data['channel']
        question_id = get_unix()
        question_text = message.text
        await message.answer('<b>Ваш вопрос успешно принят✅</b>\n'
                             'Ожидайте модерации.',
                             parse_mode='HTML')
        await message.answer('<b>Желаете задать еще вопрос?</b>\n',
                             reply_markup=get_user_new_question_kb(),
                             parse_mode='HTML')

        channel_url = db.get_channel(channel)
        db.add_new_question(str(question_text), str(channel_url[0]), int(message.from_user.id), int(question_id))
        await bot.send_message(ADMIN_CHAT, '<b>Новый вопрос❗️</b>\n\n'
                                           f'<b>Канал для размещения:</b> {channel_url[0]}\n'
                                           f'<b>Текст:</b> {question_text}',
                                           parse_mode='HTML',
                                           disable_web_page_preview=True,
                                           reply_markup=get_admin_inline_kb(question_id))
        await state.clear()
    except Exception as e:
        print(e)


@dp.callback_query(F.data.startswith('accept_question:'))
async def accepting_question(call: types.CallbackQuery):

        await bot.delete_message(call.message.chat.id, call.message.message_id)
        question_id = str(call.data).split(':')[1]
        question_data = db.get_question(question_id)
        question_text = question_data[0]
        question_channel = question_data[1]
        question_from_user = question_data[2]
        channel_for_post = db.get_question_channel_id(question_channel)[0]
        bot_url = hlink('боту', 'https://t.me/lyuda123bot')
        data = await bot.send_message(channel_for_post, f'<b>{question_text}</b>\n\n🤖'
                                                        f'Напиши свой вопрос {bot_url}, текст выделится сам',
                                                        parse_mode='HTML')
        await bot.send_message(question_from_user, '<b>Ваш вопрос успешно выложен!</b>\n\n'
                                               f'<b>Ссылка на пост:</b> {str(question_channel) + str("/") + str(data.message_id)}',
                                               parse_mode="HTML",
                                               disable_web_page_preview=True)



@dp.callback_query(F.data.startswith('decline_question:'))
async def declining_question(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        question_id = str(call.data).split(':')[1]
        question_data = db.get_question(question_id)
        question_from_user = question_data[2]
        await bot.send_message(question_from_user,
                               '<b>К сожалению, ваш вопрос был отклонен! Обратитесь к @alina_tech</b>',
                               parse_mode="HTML")
        db.delete_question(question_id)
    except Exception as e:
        print(e)


@dp.message(F.text == 'Добавленные каналы', F.from_user.id == ADMIN_ID)
async def admin_menu_channels(message: types.Message, state: FSMContext):
    try:
        await message.answer('Выберите необходимый вариант:',
                             reply_markup=get_admin_channel_kb())
    except Exception as e:
        print(e)


@dp.callback_query(F.data == 'add_channel')
async def admin_inserting_channels(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await call.message.answer('<b>Введите текст для кнопки:</b>',
                                  parse_mode='HTML',
                                  reply_markup=get_admin_cancel_kb())
        await state.set_state(InsertChannel.channel_text)
    except Exception as e:
        print(e)


@dp.message(InsertChannel.channel_text)
async def admin_channel_text(message: types.Message, state: FSMContext):
    try:
        await state.update_data(channel_text=message.text)
        await message.answer('<b>Введите айди чата:</b>',
                              parse_mode='HTML',
                             reply_markup=get_admin_cancel_kb())
        await state.set_state(InsertChannel.channel_id)
    except Exception as e:
        print(e)


@dp.message(InsertChannel.channel_id)
async def admin_channel_id(message: types.Message, state: FSMContext):
    try:
        await state.update_data(channel_id=message.text)
        await message.answer('<b>Введите ссылку чата:</b>',
                             parse_mode='HTML',
                             reply_markup=get_admin_cancel_kb())
        await state.set_state(InsertChannel.channel_url)
    except Exception as e:
        print(e)


@dp.message(InsertChannel.channel_url)
async def admin_channel_id(message: types.Message, state: FSMContext):
    try:
        channel_data = await state.get_data()
        channel_text = channel_data['channel_text']
        channel_id = int(channel_data['channel_id'])
        channel_url = message.text
        db.add_channelx(channel_url, channel_text, channel_id)
        await message.answer('<b>Кнопка успешно добавлена!</b>',
                             parse_mode='HTML')
    except Exception as e:
        print(e)


@dp.callback_query(F.data == 'view_channel')
async def admin_inserting_channels(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        channel_text = db.get_all_channels_text()
        await call.message.answer('<b>Выберите необходимую кнопку для удаления</b>',
                                  reply_markup=get_main_menu_kb(channel_text),
                                  parse_mode='HTML')
        await state.set_state(DeleteChannel.channel_id)
    except Exception as e:
        print(e)


@dp.message(DeleteChannel.channel_id)
async def deleting_channel(message: types.Message, state: FSMContext):
    try:
        db.delete_channelx(str(message.text))
        await message.answer('<b>Канал успешно удалён!</b>',
                             parse_mode='HTML',
                             reply_markup=get_admin_cancel_kb())
    except Exception as e:
        print(e)


@dp.message(F.text == 'Информация', F.from_user.id == ADMIN_ID)
async def get_information_about_bot(message: types.Message, state: FSMContext):
    try:
        count_of_users = db.get_count_userx()[0]
        await message.answer(f'<b>Количество пользователей: {count_of_users}</b>',
                             parse_mode='HTML',
                             reply_markup=get_admin_cancel_kb())
    except Exception as e:
        print(e)


@dp.message(F.text == 'Рассылка', F.from_user.id == ADMIN_ID)
async def admin_start_sending(message: types.Message, state: FSMContext):
    try:
        await message.answer(f'<b>Введите текст для рассылки:</b>',
                             parse_mode="HTML",
                             reply_markup=get_admin_cancel_kb())
        await state.set_state(NewSending.sending_text)
    except Exception as e:
        print(e)


@dp.message(NewSending.sending_text)
async def admin_sending_process(message: types.Message, state: FSMContext):
    try:
        users_id = db.get_all_userx()
        await message.answer(f'<b>Рассылка начата!</b>',
                             parse_mode='HTML')
        for user_id in users_id:
            user_id = user_id[0]
            await bot.send_message(user_id, str(message.text))
        await message.answer(f'<b>Рассылка завершена!</b>',
                             parse_mode='HTML',
                             reply_markup=get_admin_main_kb())
    except Exception as e:
        print(e)


@dp.callback_query(F.data == 'new_question')
async def user_new_question(call: types.CallbackQuery, state: FSMContext):
    try:
        print(call.from_user.id)
        if not db.get_banned_userx(call.from_user.id):
            channels_text = db.get_all_channels_text()
            await call.message.answer('Привет🖐🏻Выбери нужный канал, нажми на кнопку, задай свой вопрос⤵️\n'
                                      'Внимание ☝🏻Бот только принимает и размещает вопросы! Ответы поступают в чат!\n'
                                      'Вопросы или заказать рекламу ➡️ @alina_tech',
                                      reply_markup=get_main_menu_kb(channels_text))
            await state.set_state(AskQuestion.channel_name)
        else:
            await call.answer('Вы были заблокированы в боте!')
    except Exception as e:
        print(e)


@dp.callback_query(F.data == 'cancel')
async def user_new_question(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        await state.clear()
        await call.message.answer('<b>Главное меню</b>',
                                  parse_mode='HTML',
                                  reply_markup=get_admin_main_kb())
    except Exception as e:
        print(e)


@dp.callback_query(F.data.startswith('ban_user:'))
async def user_new_question(call: types.CallbackQuery, state: FSMContext):
    try:
        question_id = call.data.split(":")[1]
        user_id = db.get_question_userx(question_id)[0]
        await call.message.delete()
        await state.clear()
        db.ban_userx(user_id)
    except Exception as e:
        print(e)


async def main():
    bot_commands = [
        types.BotCommand(command="/start", description="Задать вопрос"),
    ]
    await bot.set_my_commands(bot_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
