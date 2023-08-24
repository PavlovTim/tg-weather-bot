import logging
from aiogram import Bot, Dispatcher, executor, types
import requests, json
from config import BOT_TOKEN, OPENWEATHERMAP_ID


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    username = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_weather = types.KeyboardButton(text="Weather")
    button_about = types.KeyboardButton(text="About")
    keyboard.add(button_weather, button_about)

    await message.answer(
        f"Hi, {username}!",
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.text == "Weather")
async def get_coord(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_weather = types.KeyboardButton(text="Weather")
    button_about = types.KeyboardButton(text="About")
    keyboard.add(button_weather, button_about)
    await message.answer(
        f"Enter coordinates through ', '",
        reply_markup=keyboard
    )


@dp.message_handler(lambda message: message.text == "About")
async def about(message: types.Message):
    username = message.from_user.username
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_weather = types.KeyboardButton(text="Weather")
    button_about = types.KeyboardButton(text="About")
    keyboard.add(button_weather, button_about)
    await message.answer(
        f"Hi, {username}!\nI'm weather-bot and I show the weather by u'rs Latitude and Longitude",
        reply_markup=keyboard
    )


@dp.message_handler()
async def get_weather(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_weather = types.KeyboardButton(text="Weather")
    button_about = types.KeyboardButton(text="About")
    keyboard.add(button_weather, button_about)
    try:
        p = message.text.split(", ")
        latitude = float(p[0])
        longitude = float(p[1])
        response = bytes.decode(
            requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPENWEATHERMAP_ID}").content
            )
        response_json = json.loads(response)
        await message.answer(
            f"Current weather in {latitude}, {longitude} is\n"
            f"{response_json['weather']}",
            reply_markup=keyboard
        )
    except Exception:
        await message.answer(
            f"Enter correct Latitude and Longitude",
            reply_markup=keyboard
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)