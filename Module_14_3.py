from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


buttom_1 = KeyboardButton(text='Расчитать')
buttom_2 = KeyboardButton(text='Информация')
buttom_3 = KeyboardButton(text='Купить')
kb = ReplyKeyboardMarkup(resize_keyboard=True).row(buttom_1, buttom_2).add(buttom_3)
buttom_3 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
buttom_4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
ikb = InlineKeyboardMarkup(resize_keyboard=True).row(buttom_3, buttom_4)
product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
ikb_product = InlineKeyboardMarkup(resize_keyboard=True).row(product1, product2, product3, product4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью! \n"
                         "Давай я помогу расчитать твою ежедневную норму калорий.", reply_markup=kb)


@dp.message_handler(text=['Расчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=ikb)


@dp.message_handler(text=['Информация'])
async def information(message):
    await message.answer("Данный бот используется для подсчета калорий по упрощенной формуле"
                         "Миффлина-Сан Жеора.")


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1,5):
        await message.answer(f'Название: Product{i} | Описание: описание{i} | Цена: {i * 100}')
        with open (f'File/{i}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Веберите продукт для покупки', reply_markup=ikb_product)


@dp.callback_query_handler(text='product_buying')
async def set_confirm_message(call):
    await call.message.answer("Вы успешно приобрелди продукт!")
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;')
    await call.answer()


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data['weight'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5
    await message.answer(f"Норма ваших калорий составляет {calories}")
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
