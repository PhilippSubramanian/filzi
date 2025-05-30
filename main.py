import logging
import hashlib
import time
from aiogram.types import InputFile
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import config
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_handler(msg: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🛒 Купить доступ", callback_data='buy_access'),
        InlineKeyboardButton("ℹ️ Помощь", callback_data='help'),
        InlineKeyboardButton("🤔 о паке", callback_data='info'),  
    )   
    await msg.answer("Добро пожаловать! Выберите действие:", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'back_to_menu')
async def back_to_menu(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🛒 Купить доступ", callback_data='buy_access'),
        InlineKeyboardButton("ℹ️ Помощь", callback_data='help'),
        InlineKeyboardButton("🤔 о паке", callback_data='info'),  
    )
    await callback_query.message.edit_text("🔙 Возврат в меню. Выберите действие:", reply_markup=kb)
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data == 'info')
async def handle_buy(callback_query: types.CallbackQuery):
    photo = InputFile("images/welcome.png")  
    btn = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💳 Перейти к оплате",callback_data="buy_access"),
        InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
    )
    await callback_query.message.answer_photo(
        photo=photo,
            caption = """
🎁 В пак входит:

🔠 1000+ вырезанных букв  
🎬 Вырезки из культовых фильмов  
🎧 400+ звуковых эффектов (мемы, гличи, клики и т.д.)  

📱 50 PNG-лого популярных приложений  
😂 650+ мемов (видео и картинки)  

🎵 750+ треков без авторских прав  
🔀 100 трендовых переходов (горизонт + вертикаль)  

💻 Крякнутые Adobe Premiere & After Effects 2023  
🧰 50 плагинов для монтажа (BorisFX, Sapphire и др.)  

📲 Рамки и персонажи для TikTok / Shorts / Reels  
🌄 200+ фонов (горизонтальные и вертикальные)  
📽️ 230 футажей от мемов до иконок  

🔤 8000+ шрифтов для дизайна и видео  
😎 100 анимированных эмодзи в 10 стилях  

💸 Цена: всего 499₽  
Идеально для новичков и профи. Нажимай кнопку оплатить чтобы все увидеть!
""",
        reply_markup=btn,
    )
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data == 'help')
async def handle_buy(callback_query: types.CallbackQuery):
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("💳 Перейти к оплате",callback_data="buy_access"),
                                     InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
    )
    InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
    await callback_query.message.answer("""
🆘 напиши в поддержу если есть вопросы:
                                        -@kinemasterovvvv
                                        """, reply_markup=btn)

    await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == 'buy_access')
async def handle_buy(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    order_id = f"{user_id}_{int(time.time())}"
    amount = 499

    sign_str = f"{config.MERCHANT_ID}:{amount}:{config.SECRET_2}:{order_id}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()

    pay_url = f"https://pay.freekassa.ru?m={config.MERCHANT_ID}&oa={amount}&o={order_id}&s={sign}"
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("💳 Перейти к оплате", url=pay_url),
                                     InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
    )
    InlineKeyboardButton("🔙 Вернуться в меню", callback_data="back_to_menu")
    await callback_query.message.answer("Перейдите по ссылке для оплаты:", reply_markup=btn)
    await callback_query.answer()

  
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
