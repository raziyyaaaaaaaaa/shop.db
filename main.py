import asyncio
import logging
import os
from aiogram import Bot,Dispatcher,types,F
from aiogram.filters.command import Command,CommandObject
logging.basicConfig(level=logging.INFO)
from utils import db_add_category,db_add_product,db_get_categories,db_get_products_by_category,create_tables, db_get_products_by_category
import kb
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest 
from aiogram.types import FSInputFile
token="6908131922:AAEioAlw_9KY4f_35bNB_TvXF33WvMc7iJo"
admin_id = 5308654174
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message:types.Message):
    await message.answer("Hello")
"/add_category Food"
@dp.message(F.from_user.id == admin_id, Command('add_category'))
async def add_category(message: types.Message, command: CommandObject):
    argue = command.args
    db_add_category(argue)
    await message.answer(f"Новая запись в таблице Category {argue}")

@dp.message(Command('categories'))
async def get_categories(message:types.Message):
    categories = ''
    for i in db_get_categories():
        categories+=f"{i[0]} {i[1]}\n"
    await message.answer(str(categories))

@dp.message(Command('add_product'), F.from_user.id == admin_id)
async def add_product(message : types.Message,command : CommandObject, bot : Bot):
    argue = command.args
    try:
        category_id, name = argue.split()
    except Exception as e:
        print(e)
    if not os.path.exists(f"media/{category_id}"):
        os.mkdir(f"media/{category_id}")
    destination=f'media/{category_id}/{name}.jpg'
    await bot.download(
        message.photo[-1],
        destination=destination
    )
    db_add_product(int(category_id), name, destination)
    await message.answer(f"Новая запись {destination}")

@dp.callback_query(kb.Pagination.filter(F.action.in_(['prev', 'next'])))
async def pagination_handler(call: types.CallbackQuery, callback_data: kb.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    products = db_get_products_by_category()
    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(products) - 1) else page_num

    with suppress(TelegramBadRequest):
        photo = FSInputFile(str(products[page][3]))
        text = str(products[page][2])
        new_media = types.InputMediaPhoto(media=photo, caption=text)

        await call.message.edit_media(
            media=new_media,
            reply_markup=kb.paginator(page=page), 
        )

    await call.answer()


@dp.message(Command('products'))
async def get_products(message:types.Message):
    products = db_get_products_by_category()
    photo =  FSInputFile(str(products[0][3]))
    text = str(products[0][2])
    await message.answer_photo(photo=photo, caption=text, reply_markup=kb.paginator())



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    create_tables()
    asyncio.run(main())
