# -*- coding: utf-8 -*-

import telebot
from telebot import types
from extensions import APIException, ClassBot
from tokens import token
from config import help_command, values_command, help_text

######################################################################################################################


bot = telebot.TeleBot(token)


######################################################################################################################


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, )
    button1 = types.KeyboardButton(text=help_command, )
    button2 = types.KeyboardButton(text=values_command, )
    markup.add(button1, button2)
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Приветствую, {message.chat.username}!\n{help_text}',
        reply_markup=markup
    )


######################################################################################################################


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=help_text
    )


######################################################################################################################


@bot.message_handler(commands=['values'])
def command_values(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=ClassBot.get_list_currency()
    )


######################################################################################################################


@bot.message_handler(content_types=['text'])
def command_text(message):
    if message.text == help_command:
        text = help_text
    elif message.text == values_command:
        text = ClassBot.get_list_currency()
    else:
        try:
            text = ClassBot.data_process(message=message)
        except APIException as ex:
            text = f'Ошибка: {ex}'
    bot.send_message(
        chat_id=message.chat.id,
        text=text
    )


######################################################################################################################


if __name__ == '__main__':
    bot.infinity_polling()


######################################################################################################################
