from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

import urllib.request

mainmenu = [ [InlineKeyboardButton(text="Моё расписание",callback_data="myshedule"), InlineKeyboardButton(text="Настройка",callback_data="myoption")] ] # кнопки главного меню
mainmenu = InlineKeyboardMarkup(inline_keyboard=mainmenu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)

chat_group_dict={} # словарь привязки чата и номера группы

groups_nums=[['111','121','131','141','211','221','231'],['241','311','321','331','341','411','421'],['511','521','531','611','621','631','741'],
['811','821','822','831','911','921','931'],['1011','1021','1031','1041','1121','1131'],['1211','1221','1231','1241','1311','1411']]
group_buttons=[]
for group_row in groups_nums:
    group_buttons_row=[]
    for num in group_row:
        group_buttons_row.append(InlineKeyboardButton(text=num, callback_data="setgroup-"+num))
    group_buttons.append(group_buttons_row)
group_buttons = InlineKeyboardMarkup(inline_keyboard=group_buttons)

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    greet = "Привет, {name}, я бот, предоставляющий текущее расписание занятий в Алексеевском колледже️"
    await msg.answer(greet.format(name=msg.from_user.full_name), reply_markup=mainmenu)

@router.message(F.text == "/menu")
@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer("Главное меню", reply_markup=mainmenu)

@router.callback_query(F.data == "myshedule")
async def myoption(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    if chat_id in chat_group_dict:
        group=chat_group_dict[chat_id]
        fp = urllib.request.urlopen("http://alcol.deltabest.ru/shedule/api/forgroup/?group="+group)
        mybytes = fp.read()
        shedule_html = mybytes.decode("utf8")
        fp.close()
        await callback.message.answer(shedule_html[0:1000], reply_markup=mainmenu)
    else:
        await callback.message.answer("Выберите номер Вашей группы", reply_markup=group_buttons)

@router.callback_query(F.data == "myoption")
async def myoption(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите номер Вашей группы", reply_markup=group_buttons)

@router.callback_query(F.data.startswith("setgroup"))
async def setgroup(callback: CallbackQuery, state: FSMContext):
    group = callback.data.split('-')[1]
    chat_id = callback.message.chat.id
    chat_group_dict[chat_id]=group
    await callback.message.answer("Вы выбрали группу "+group, reply_markup=mainmenu)

@router.message(F.text)
async def message_with_text(msg: Message):
    await msg.answer("Главное меню", reply_markup=mainmenu)
