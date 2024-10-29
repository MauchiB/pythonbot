from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='profile')],
                                     [KeyboardButton(text='information')]],
                                     resize_keyboard=False)

inline = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='profile', callback_data='_profile_')],
                                               [InlineKeyboardButton(text='write', callback_data='_write_'),
                                               InlineKeyboardButton(text='show entries', callback_data='_show_')],
                                               [InlineKeyboardButton(text='delete note', callback_data='_delete_note_')]])
