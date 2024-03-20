# Здесь пока без комментариев ) Будут на следующем шаге
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

import urllib.request

mainmenu = [
    [InlineKeyboardButton(text="Моё расписание", callback_data="myshedule"),
    InlineKeyboardButton(text="Настройка", callback_data="myoption")]
]
mainmenu = InlineKeyboardMarkup(inline_keyboard=mainmenu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)

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
async def myoption(clbck: CallbackQuery, state: FSMContext):
    fp = urllib.request.urlopen("http://alcol.deltabest.ru/shedule/api/forgroup/?group=1411")
    mybytes = fp.read()
    shedule_html = mybytes.decode("utf8")
    fp.close()
    await clbck.message.answer(shedule_html[0:1000], reply_markup=exit_kb)

@router.callback_query(F.data == "myoption")
async def myoption(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer("Здесь будут Ваши настрйки...", reply_markup=exit_kb)


