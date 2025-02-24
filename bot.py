'''
Software Use License

Copyright © 2025 Dmitry Lesin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to use the Software subject to the following conditions:

Copyright Notice and Permission
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

Restrictions on Use and Distribution
The licensee may not:

• Sell, transfer, or sublicense the Software in any form, including modified versions.
• Use the Software for commercial purposes without prior written consent from the Licensor.
• Modify, adapt, create derivative works based on the Software, or distribute such works
without prior written consent from the Licensor.

Personal Use
The Software may only be used for personal, non-commercial purposes. Commercial use of the Software
in any project is prohibited without prior written consent from the Licensor.

Disclaimer
The Software is provided "as is," without any warranties, express or implied, including but not
limited to warranties of merchantability, fitness for a particular purpose, and non-infringement.
In no event shall the authors or copyright holders be liable for any claims, damages, or other
liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in
connection with the Software or the use or other dealings in the Software.
'''



from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram import F
import asyncio
import webbrowser
import random
import os
import time
import sounddevice as sd
import scipy.io.wavfile as wav
import mss
import pyautogui
import keyboard
import platform
import psutil
import requests
import pygetwindow as gw
import json
import shutil
import subprocess
import winreg
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from aiogram.fsm.state import StatesGroup, State
import ctypes
import pyperclip
from aiogram.fsm.context import FSMContext
from cryptography.fernet import Fernet
import sqlite3
import wave
import cv2
from urllib.parse import quote
from typing import Union
import sys
from aiogram.exceptions import TelegramBadRequest
import datetime

CONFIG_FILE = "config.json"

ADMIN_ID = 6516067694


def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} файл не найден. Пожалуйста, создайте файл с необходимыми данными.")
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    return config.get("API_TOKEN"), config.get("authorized_user_id"), config.get("key_user")


def check_user_key(user_key, valid_keys):
    if user_key not in valid_keys:
        raise ValueError("Неверный ключ! Пожалуйста, проверьте свою конфигурацию.")


try:
    API_TOKEN, authorized_user_id, key_user = load_config()

    keys_users = [
        ""
    ]

    check_user_key(key_user, keys_users)


except FileNotFoundError as e:
    print(e)
    exit(1)
except ValueError as e:
    print(e)
    exit(1)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

language_user = "English"
dnd_enabled = False

def is_authorized(user_id):
    return str(user_id.chat.id) == authorized_user_id

SendInput = ctypes.windll.user32.keybd_event

youtube_context = {}
user_notifications = {}
user_data = {}

TEMP_FOLDER = os.getenv("TEMP")
youtube_pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
url_pattern = r"^(https?://)?[^\s/$.?#].[^\s]*$"


def load_settings():
    try:
        with open("settings.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_settings(updated_settings):
    settings = load_settings()
    settings.update(updated_settings)

    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)


def load_disk_path():
    settings = load_settings()
    if "disk_path" not in settings:
        settings["disk_path"] = "C:/"
        save_settings(settings)
    return settings["disk_path"]


def save_disk_path(new_path):
    save_settings({"disk_path": new_path})

settings = load_settings()
browser = settings.get("browser", "Google Chrome")
do_not_disturb_enabled = settings.get("do_not_disturb_enabled", False)

disk_path = load_disk_path()

# enter the SHODAN IP
SHODAN_API_KEY = "BkR5Nt4LBj51KyupnTD2riZlQoNWmwTM"


@dp.callback_query(lambda call: call.data == "btn_murder_ru")
async def shutdown_bot(call: types.CallbackQuery, bot: Bot):
    await call.message.answer("smartPC Pro отключен!")
    await asyncio.sleep(1)
    sys.exit(0)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    if is_authorized(message):
        markup_ru_cont = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить", callback_data="ru_cont")]
            ]
        )
        await message.answer(
            """👋<b>Поздравляем! smartPC Pro | Lexium теперь у вас. Пользуйтесь с удовольствием!</b> 🎯\n\n""",
            reply_markup=markup_ru_cont,
            parse_mode="HTML",
        )
    else:
        await message.reply("Доступ запрещен!")


@dp.callback_query(lambda call: call.data == 'ru_cont')
async def cont_ru(call: types.CallbackQuery):
    await call.message.delete()

    try:
        photo = FSInputFile("assets/image/smartpc_pro.png")

        btn_favourites_ru = InlineKeyboardButton(text="Избранное ❤️", callback_data="favourites_ru")
        btn_main_ru = InlineKeyboardButton(text="Основные команды ⚙️", callback_data="main_commands_ru")
        main_btn_ru = InlineKeyboardButton(text="Основные кнопки🔘", callback_data="main_btn_ru")
        btn_apps_ru = InlineKeyboardButton(text="Приложения 📱", callback_data="apps_commands_ru")
        apps_youtube_ru = InlineKeyboardButton(text="YouTube ▶️", callback_data="apps_youtube_ru")
        btn_sait_ru = InlineKeyboardButton(text="Сайты 🌐", callback_data="sait_commands_ru")
        btn_my_computer_ru = InlineKeyboardButton(text="Про мой компьютер 🖥", callback_data="my_computer_ru")
        btn_clearing_ru = InlineKeyboardButton(text="Очистка🗑", callback_data="clearing_ru")
        btn_keyboard_control_ru = InlineKeyboardButton(text="Управление клавиатурой 📲", callback_data='keyboard_control_ru')
        btn_browser_management = InlineKeyboardButton(text="Управление браузером 🌎", callback_data="btn_browser_management")
        btn_files_ru = InlineKeyboardButton(text="Файловая система 🗂", callback_data="files_ru")
        btn_pro_func_ru = InlineKeyboardButton(text="Pro функции 😈", callback_data="pro_func_ru")
        btn_personal_account_ru = InlineKeyboardButton(text="Личный аккаунт👤", callback_data="personal_account_ru")
        btn_telegraph_ru = InlineKeyboardButton(text="Информация",
                                                url="https://telegra.ph/smartPC-Your-Smart-Assistant-for-PC-Management-in-Jarvis-Style-11-21")
        btn_murder_ru = InlineKeyboardButton(text="❌Выключить smartPC Pro❌", callback_data="btn_murder_ru")
        markup_ru = InlineKeyboardMarkup(inline_keyboard=[
            [btn_favourites_ru],
            [btn_main_ru, main_btn_ru],
            [btn_apps_ru, btn_sait_ru],
            [btn_my_computer_ru, apps_youtube_ru],
            [btn_clearing_ru, btn_keyboard_control_ru],
            [btn_browser_management],
            [btn_files_ru],
            [btn_pro_func_ru],
            [btn_personal_account_ru],
            [btn_telegraph_ru],
            [btn_murder_ru]
        ])

        await call.message.answer_photo(
            photo=photo,
            caption="⚡️ <b>smartPC Pro | Lexium</b> ⚡️",
            reply_markup=markup_ru,
            parse_mode="HTML"
        )
    except Exception as e:
        await call.message.answer(f"Произошла ошибка: {str(e)}")


@dp.callback_query(lambda call: call.data == 'main_commands_ru')
async def main_commands_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Основные команды:</b>\n
""", reply_markup=markup_main_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_shutdown_ru = InlineKeyboardButton(text="Завершение работы ✅", callback_data="btn_shutdown_ru")
btn_restart_ru = InlineKeyboardButton(text="Перезагрузка 🔄", callback_data="btn_restart_ru")
btn_sleep_ru = InlineKeyboardButton(text="Спящий режим 💤", callback_data="btn_sleep_ru")
btn_lock_ru = InlineKeyboardButton(text="Заблокировать экран 👀", callback_data="btn_lock_ru")
btn_screenshot_ru = InlineKeyboardButton(text="Скриншот 📸", callback_data="btn_screenshot_ru")
btn_switch_layout_ru = InlineKeyboardButton(text="Изменить язык 🌐", callback_data="btn_switch_layout_ru")
btn_collapse_ru = InlineKeyboardButton(text="Свернуть окна 🖱️", callback_data="btn_collapse_ru")
btn_scroll_up_ru = InlineKeyboardButton(text="Скролл вверх ⬆️", callback_data="btn_scroll_up_ru")
btn_scroll_down_ru = InlineKeyboardButton(text="Скролл вниз ⬇️", callback_data="btn_scroll_down_ru")
btn_full_screen_ru = InlineKeyboardButton(text="Полный экран 🖥️", callback_data="btn_full_screen_ru")
btn_set_volume_ru = InlineKeyboardButton(text="Изменение звука🔊", callback_data="btn_volume_ru")
btn_set_brightness_ru = InlineKeyboardButton(text="Изменение яркости💡", callback_data="btn_set_brightness_ru")
markup_main_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_shutdown_ru],
    [btn_restart_ru],
    [btn_sleep_ru],
    [btn_lock_ru],
    [btn_screenshot_ru],
    [btn_collapse_ru],
    [btn_scroll_up_ru, btn_scroll_down_ru],
    [btn_full_screen_ru],
    [btn_set_volume_ru],
    [btn_set_brightness_ru]
])


@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")


# The Shutdown button in Russian and the command "/shutdown"
@dp.callback_query(lambda call: call.data == 'btn_shutdown_ru')
@dp.message(Command("shutdown"))
async def shutdown_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            # Выключение ПК
            await message.answer("Выключение ПК...")
            os.system("shutdown /s /t 1")
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Restart" button in Russian and the "/restart" command
@dp.callback_query(lambda call: call.data == 'btn_restart_ru')
@dp.message(Command("restart"))
async def restart_ru(event):
    message = event.message if isinstance(event, CallbackQuery) else event

    if is_authorized(message):
        try:
            await message.answer("Перезагрузка ПК...")

            os.system("shutdown /r /t 1")
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The Sleep button in Russian and the command "/sleep"
@dp.callback_query(lambda call: call.data == 'btn_sleep_ru')
@dp.message(Command("sleep"))
async def sleep_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            sleep_message = await message.reply("Перевожу ПК в спящий режим...")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            await asyncio.sleep(30)
            await sleep_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Lock screen" button in Russian and the "/lock" command
@dp.callback_query(lambda call: call.data == 'btn_lock_ru')
@dp.message(Command("lock"))
async def lock_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            # Блокировка экрана
            await message.answer("Экран заблокирован")
            os.system("rundll32 user32.dll,LockWorkStation")
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")



# Обработчик кнопки "Скриншот" и команды "/screenshot"
@dp.callback_query(lambda call: call.data == 'btn_screenshot_ru')
@dp.message(Command("screenshot"))
async def screenshot_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                monitor_count = len(monitors) - 1

            if monitor_count == 1:
                monitor_index = 1
            else:
                monitor_list = "\n".join([f"{i}. Монитор {i}" for i in range(1, monitor_count + 1)])
                await message.answer(f"Доступные мониторы:\n{monitor_list}\nВведите номер монитора:")

                monitor_index_msg = await bot.wait_for("message")
                try:
                    monitor_index = int(monitor_index_msg.text.strip())
                except ValueError:
                    await message.answer("Некорректный ввод. Отменено.")
                    return

                if monitor_index < 1 or monitor_index > monitor_count:
                    await message.answer("Номер монитора вне диапазона. Отменено.")
                    return

            screenshot_path = f"screenshot_monitor_{monitor_index}.png"
            with mss.mss() as sct:
                monitor = sct.monitors[monitor_index]
                screenshot = sct.grab(monitor)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)

            photo = FSInputFile(screenshot_path)
            await message.answer_photo(photo)

            os.remove(screenshot_path)
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Change language" button in Russian and the command "/switch_layout"
@dp.callback_query(lambda call: call.data == 'btn_switch_layout_ru')
@dp.message(Command("switch_layout"))
async def switch_layout_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            pyautogui.hotkey('win', 'space')

            layout = await message.reply("Раскладка клавиатуры изменена!")

            await asyncio.sleep(30)
            await layout.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Minimize windows" button in Russian and the "/collapse" command
@dp.callback_query(lambda call: call.data == 'btn_collapse_ru')
@dp.message(Command("collapse"))
async def collapse_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            collapse_msg = await message.reply("Окна свернуты")

            keyboard.press('win')
            keyboard.press('m')
            keyboard.release('m')
            keyboard.release('win')

            await asyncio.sleep(30)
            await collapse_msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Scroll up" button in Russian and the command "/scroll_up"
@dp.callback_query(lambda call: call.data == 'btn_scroll_up_ru')
@dp.message(Command("scroll_up"))
async def scroll_up_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            scroll = await message.reply("Scroll выполнен наверх")
            pyautogui.scroll(745)
            await asyncio.sleep(3)
            await scroll.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Scroll down" button in Russian and the "/scroll_down" command
@dp.callback_query(lambda call: call.data == 'btn_scroll_down_ru')
@dp.message(Command("scroll_down"))
async def scroll_down_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            scroll = await message.reply("Scroll выполнен вниз")
            pyautogui.scroll(-745)
            await asyncio.sleep(3)
            await scroll.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The Full screen button in Russian and the command "/full_screen"
@dp.callback_query(lambda call: call.data == 'btn_full_screen_ru')
@dp.message(Command("full_screen"))
async def full_screen_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            screen = await message.reply("Полный экран")

            pyautogui.hotkey('win', 'up')

            await asyncio.sleep(30)
            await screen.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


class VolumeBrightnessStates(StatesGroup):
    set_volume = State()
    set_brightness = State()

# The "Sound" button
@dp.callback_query(F.data == "btn_volume_ru")
async def ask_volume(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите громкость от 0 до 100:")
    await call.answer()
    await state.set_state(VolumeBrightnessStates.set_volume)


@dp.message(VolumeBrightnessStates.set_volume)
async def handle_volume_input(message: types.Message, state: FSMContext):
    try:
        volume = int(message.text)
        if 0 <= volume <= 100:
            set_volume_pycaw(volume)
            await message.reply(f"Громкость была успешно установлена на {volume}%.")
        else:
            error_message = await message.reply("Введите число в диапазоне от 0 до 100.")
            await asyncio.sleep(10)
            await error_message.delete()
    except ValueError:
        error_message = await message.reply("Пожалуйста, введите действительный номер.")
        await asyncio.sleep(10)
        await error_message.delete()
    finally:
        await state.clear()


# Brightness button
@dp.callback_query(F.data == "btn_set_brightness_ru")
async def ask_brightness(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите значение яркости от 0 до 100:")
    await call.answer()
    await state.set_state(VolumeBrightnessStates.set_brightness)


@dp.message(VolumeBrightnessStates.set_brightness)
async def handle_brightness_input(message: types.Message, state: FSMContext):
    try:
        brightness = int(message.text)
        if 0 <= brightness <= 100:
            set_brightness_windows(brightness)
            await message.reply(f"Яркость была успешно установлена на {brightness}%.")
        else:
            error_message = await message.reply("Введите число в диапазоне от 0 до 100.")
            await asyncio.sleep(10)
            await error_message.delete()
    except ValueError:
        error_message = await message.reply("Пожалуйста, введите действительный номер.")
        await asyncio.sleep(10)
        await error_message.delete()
    finally:
        await state.clear()


def set_volume_pycaw(volume: int):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume_interface = interface.QueryInterface(IAudioEndpointVolume)
        volume_interface.SetMasterVolumeLevelScalar(volume / 100.0, None)
    except Exception as e:
        print(f"⚠ Ошибка при настройке громкости: {e}")


# Function for setting brightness
def set_brightness_windows(brightness: int):
    subprocess.run(
        ["powershell", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})"],
        shell=True,
    )



@dp.callback_query(lambda call: call.data == 'main_btn_ru')
async def main_btn_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Основные кнопки:</b>\n
""", reply_markup=markup_btn_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Back🔙", callback_data="btn_back_ru")
btn_space_ru = InlineKeyboardButton(text="Пробел", callback_data="btn_space_ru")
btn_enter_ru = InlineKeyboardButton(text="Enter", callback_data="btn_enter_ru")
btn_esc_ru = InlineKeyboardButton(text="ESC", callback_data="btn_esc_ru")
btn_tab_ru = InlineKeyboardButton(text="TAB", callback_data="btn_tab_ru")
btn_del_ru = InlineKeyboardButton(text="DEL", callback_data="btn_del_ru")
btn_backspace_ru = InlineKeyboardButton(text="Backspace", callback_data="btn_backspace_ru")
btn_capslock_ru = InlineKeyboardButton(text=" CAPS Lock", callback_data="btn_capslock_ru")
btn_rmb_ru = InlineKeyboardButton(text="ПКМ", callback_data="btn_rmb_ru")
btn_lmb_ru = InlineKeyboardButton(text="ЛКМ", callback_data="btn_lmb_ru")
btn_f_ru = InlineKeyboardButton(text="F1-F12", callback_data="btn_f_ru")
markup_btn_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_space_ru],
    [btn_enter_ru],
    [btn_esc_ru],
    [btn_tab_ru],
    [btn_del_ru],
    [btn_backspace_ru],
    [btn_capslock_ru],
    [btn_lmb_ru, btn_rmb_ru],
    [btn_f_ru]
])

# Back button in English
@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")


## The "Пробел" button in Russian and the "/space" command
@dp.callback_query(lambda call: call.data == 'btn_space_ru')
@dp.message(Command("space"))
async def space_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка пробел нажата")
            pyautogui.press('space')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Enter" button in Russian and the "/Enter" command
@dp.callback_query(lambda call: call.data == 'btn_enter_ru')
@dp.message(Command("enter"))
async def enter_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка enter нажата")
            pyautogui.press('enter')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "ESC" button in Russian and the "/esc" command
@dp.callback_query(lambda call: call.data == 'btn_esc_ru')
@dp.message(Command("esc"))
async def esc_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка ESC нажата")
            pyautogui.press('esc')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "TAB" button in Russian and the "/tab" command
@dp.callback_query(lambda call: call.data == 'btn_tab_ru')
@dp.message(Command("tab"))
async def tab_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка TAB нажата")
            pyautogui.press('tab')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "DEL" button in Russian and the "/del" command
@dp.callback_query(lambda call: call.data == 'btn_del_ru')
@dp.message(Command("del"))
async def del_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка DEL нажата")
            pyautogui.press('delete')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Backspace" button in Russian and the "/backspace" command
@dp.callback_query(lambda call: call.data == 'btn_backspace_ru')
@dp.message(Command("backspace"))
async def backspace_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка backspace нажата")
            pyautogui.press('backspace')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "CAPS Lock" button in Russian and the "/capslock" command
@dp.callback_query(lambda call: call.data == 'btn_capslock_ru')
@dp.message(Command("capslock"))
async def capslock_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка CAPS Lock нажата")
            pyautogui.press('capslock')

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "ПКМ" button in Russian and the "/rmb" command
@dp.callback_query(lambda call: call.data == 'btn_rmb_ru')
@dp.message(Command("rmb"))
async def rmb_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка ПКМ нажата")
            pyautogui.click(button="right")

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "ЛКМ" button in Russian and the "/lmb" command
@dp.callback_query(lambda call: call.data == 'btn_lmb_ru')
@dp.message(Command("lmb"))
async def lmb_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            msg = await message.reply("Кнопка ЛКМ нажата")
            pyautogui.click(button="left")

            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_f_ru')
async def f_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Кнопки F:</b>\n
""", reply_markup=markup_f_ru, parse_mode="HTML")


btn_back_f_ru = InlineKeyboardButton(text="Back🔙", callback_data="btn_back_f_ru")
btn_f1_ru = InlineKeyboardButton(text="F1", callback_data="btn_f1_ru")
btn_f2_ru = InlineKeyboardButton(text="F2", callback_data="btn_f2_ru")
btn_f3_ru = InlineKeyboardButton(text="F3", callback_data="btn_f3_ru")
btn_f4_ru = InlineKeyboardButton(text="F4", callback_data="btn_F4_ru")
btn_f5_ru = InlineKeyboardButton(text="F5", callback_data="btn_f5_ru")
btn_f6_ru = InlineKeyboardButton(text="F6️", callback_data="btn_f6_ru")
btn_f7_ru = InlineKeyboardButton(text="F7", callback_data="btn_f7_ru")
btn_f8_ru = InlineKeyboardButton(text="F8", callback_data="btn_f8_ru")
btn_f9_ru = InlineKeyboardButton(text="F9", callback_data="btn_f9_ru")
btn_f10_ru = InlineKeyboardButton(text="F10", callback_data="btn_f10_ru")
btn_f11_ru = InlineKeyboardButton(text="F11", callback_data="btn_f11_ru")
btn_f12_ru = InlineKeyboardButton(text="F12", callback_data="btn_f12_ru")
markup_f_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_f_ru],
    [btn_f1_ru, btn_f2_ru, btn_f3_ru],
    [btn_f4_ru, btn_f5_ru, btn_f6_ru],
    [btn_f7_ru, btn_f8_ru, btn_f9_ru],
    [btn_f10_ru, btn_f11_ru, btn_f12_ru],
    ])


# Back button in English
@dp.callback_query(F.data == 'btn_back_f_ru')
async def go_back_f_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await main_btn_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")

# f1 button in Russian
@dp.callback_query(F.data == 'btn_f1_ru')
async def f1_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f1')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")

# f2 button in Russian
@dp.callback_query(F.data == 'btn_f2_ru')
async def f2_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f2')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")

# f3 button in Russian
@dp.callback_query(F.data == 'btn_f3_ru')
async def f3_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f3')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f4 button in Russian
@dp.callback_query(F.data == 'btn_f4_ru')
async def f4_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f4')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f5 button in Russian
@dp.callback_query(F.data == 'btn_f5_ru')
async def f5_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f5')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f6 button in Russian
@dp.callback_query(F.data == 'btn_f6_ru')
async def f6_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f6')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f7 button in Russian
@dp.callback_query(F.data == 'btn_f7_ru')
async def f7_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f7')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f8 button in Russian
@dp.callback_query(F.data == 'btn_f8_ru')
async def f8_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f8')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f9 button in Russian
@dp.callback_query(F.data == 'btn_f9_ru')
async def f9_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f9')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f10 button in Russian
@dp.callback_query(F.data == 'btn_f10_ru')
async def f10_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f10')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f11 button in Russian
@dp.callback_query(F.data == 'btn_f11_ru')
async def f11_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f11')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# f12 button in Russian
@dp.callback_query(F.data == 'btn_f12_ru')
async def f12_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f12')
        await call.answer("Кнопка нажата!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")



# APPLICATION COMMANDS IN ENGLISH
@dp.callback_query(lambda call: call.data == 'apps_commands_ru')
async def apps_commands_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Команды приложений:</b>\n
""", reply_markup=markup_app_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Back🔙", callback_data="btn_back_ru")
btn_telegram_ru = InlineKeyboardButton(text="Telegram✈️", callback_data="btn_telegram_ru")
btn_chrome_ru = InlineKeyboardButton(text="Google Chrome🌐🔍", callback_data="btn_chrome_ru")
btn_opera_ru = InlineKeyboardButton(text="Opera🌍", callback_data="btn_opera_ru")
btn_edge_ru = InlineKeyboardButton(text="Microsoft Edge🔍", callback_data="btn_edge_ru")
btn_firefox_ru = InlineKeyboardButton(text="Firefox🦊🌍", callback_data="btn_firefox_ru")
btn_yandex_ru = InlineKeyboardButton(text="Яндекс🔎", callback_data="btn_yandex_ru")
btn_discord_ru = InlineKeyboardButton(text="Discord💬🎧", callback_data="btn_discord_ru")
btn_steam_ru = InlineKeyboardButton(text="Steam🎮🔥", callback_data="btn_steam_ru")
btn_console_ru = InlineKeyboardButton(text="Консоль🖥️", callback_data="btn_console_ru")
markup_app_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_telegram_ru],
    [btn_chrome_ru],
    [btn_opera_ru],
    [btn_edge_ru],
    [btn_firefox_ru],
    [btn_yandex_ru],
    [btn_discord_ru],
    [btn_steam_ru],
    [btn_console_ru]
])


# Back button in English
@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещйн!")


# The "Telegram" button in Russian and the "/telegram" command
@dp.callback_query(lambda call: call.data == 'btn_telegram_ru')
@dp.message(Command("telegram"))
async def telegram_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Telegram", reply_markup=btn_exit_telegram_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Telegram")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Google_chrome" button in Russian and the "/google_chrome" command
@dp.callback_query(lambda call: call.data == 'btn_chrome_ru')
@dp.message(Command("google_chrome"))
async def google_chrome_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Google Chrome", reply_markup=btn_exit_chrome_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Google Chrome")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Opera" button in Russian and the "/opera" command
@dp.callback_query(lambda call: call.data == 'btn_opera_ru')
@dp.message(Command("opera"))
async def opera_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Opera", reply_markup=btn_exit_opera_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Opera")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Edge" button in Russian and the "/edge" command
@dp.callback_query(lambda call: call.data == 'btn_edge_ru')
@dp.message(Command("edge"))
async def edge_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Microsoft Edge", reply_markup=btn_exit_edge_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Microsoft Edge")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Firefox" button in Russian and the "/firefox" command
@dp.callback_query(lambda call: call.data == 'btn_firefox_ru')
@dp.message(Command("firefox"))
async def firefox_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Firefox", reply_markup=btn_exit_firefox_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Firefox")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Firefox" button in Russian and the "/firefox" command
@dp.callback_query(lambda call: call.data == 'btn_yandex_ru')
@dp.message(Command("yandex"))
async def yandex_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Яндекс", reply_markup=btn_exit_yandex_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Яндекс")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Discord" button in Russian and the "/discord" command
@dp.callback_query(lambda call: call.data == 'btn_discord_ru')
@dp.message(Command("discord"))
async def discord_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Discord", reply_markup=btn_exit_discord_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Discord")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "steam" button in Russian and the "/steam" command
@dp.callback_query(lambda call: call.data == 'btn_steam_ru')
@dp.message(Command("steam"))
async def steam_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск Steam", reply_markup=btn_exit_steam_ru)
            pyautogui.press("win")
            time.sleep(1)
            keyboard.write("Steam")
            time.sleep(1)
            pyautogui.press('enter')

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Console" button in Russian and the "/console" command
@dp.callback_query(lambda call: call.data == 'btn_console_ru')
@dp.message(Command("console"))
async def console_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            app = await message.reply("Запуск консоли", reply_markup=btn_exit_console_ru)
            os.system("start cmd")

            await asyncio.sleep(30)
            await app.delete()

        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# Exit buttons from applications in English
btn_exit_telegram_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_telegram_ru")]
    ]
)
btn_exit_chrome_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_chrome_ru")]
    ]
)
btn_exit_opera_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_opera_ru")]
    ]
)
btn_exit_edge_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_edge_ru")]
    ]
)
btn_exit_firefox_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_firefox_ru")]
    ]
)
btn_exit_yandex_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_yandex_ru")]
    ]
)
btn_exit_discord_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_discord_ru")]
    ]
)
btn_exit_steam_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_steam_ru")]
    ]
)
btn_exit_console_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌Закрыть❌", callback_data="exit_console_ru")]
    ]
)


# Functions for closing applications in Russian
@dp.callback_query(lambda call: call.data == 'exit_telegram_ru')
async def exit_telegram_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Telegram.exe /F")
            exit_message = await call.message.answer("Telegram закрыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_chrome_ru')
async def exit_chrome_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Chrome.exe /F")
            exit_message = await call.message.answer("Google Chrome закрыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")

    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_opera_ru')
async def exit_opera_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Opera.exe /F")
            exit_message = await call.message.answer("Opera закрыта")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_edge_ru')
async def exit_edge_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM msedge.exe /F")
            exit_message = await call.message.answer("Microsoft Edge закрыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_firefox_ru')
async def exit_firefox_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Firefox.exe /F")
            exit_message = await call.message.answer("Firefox закрыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_discord_ru')
async def exit_discord_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Discord.exe /F")
            exit_message = await call.message.answer("Discord заркыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_yandex_ru')
async def exit_yandex_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM yandex.exe /F")
            exit_message = await call.message.answer("Яндекс заркыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_steam_ru')
async def exit_steam_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM Steam.exe /F")
            exit_message = await call.message.answer("Steam закрыт")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'exit_console_ru')
async def exit_console_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            os.system("taskkill /IM cmd.exe /F")
            exit_message = await call.message.answer("Консоль закрыта")
            await asyncio.sleep(10)
            await exit_message.delete()
        except Exception as e:
            await call.message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")



# YOUTUBE in Russian
@dp.callback_query(lambda call: call.data == 'apps_youtube_ru')
async def youtube_commands_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>YouTube команды:</b>\n
""", reply_markup=markup_youtube_ru, parse_mode="HTML")



btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_play_ru = InlineKeyboardButton(text="Пауза ⏸️/Продолжить ▶️", callback_data="btn_play_ru")
btn_next_ru = InlineKeyboardButton(text="Следующее видео ⏭️", callback_data="btn_next_ru")
btn_full_video_ru = InlineKeyboardButton(text="Полный экран видео📹", callback_data="btn_full_video_ru")
btn_sub_ru = InlineKeyboardButton(text="Вкл/выкл субтитры🔤", callback_data="btn_sub_ru")
btn_sounds_video_ru = InlineKeyboardButton(text="Вкл/выкл звук🔈", callback_data="btn_sounds_video_ru")
btn_mini_player_ru = InlineKeyboardButton(text="Мини-проигрыватель📺", callback_data="btn_mini_player_ru")
btn_update_ru = InlineKeyboardButton(text="Обновить страницу 🔄", callback_data="btn_update_ru")
markup_youtube_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_play_ru],
    [btn_next_ru],
    [btn_full_video_ru],
    [btn_sub_ru],
    [btn_sounds_video_ru],
    [btn_mini_player_ru],
    [btn_update_ru]]
)


# Back button in Russian
@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")


# pause button in Russian
@dp.callback_query(F.data == 'btn_play_ru')
async def play_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        pyautogui.press('space')
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# the next video button is in Russian
@dp.callback_query(F.data == 'btn_next_ru')
async def next_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('shift+n')
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# Обработчик для кнопки
@dp.callback_query(F.data == 'btn_full_video_ru')
async def full_video_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        VK_F = 0x46

        SendInput(VK_F, 0, 0, 0)
        SendInput(VK_F, 0, 2, 0)
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


@dp.callback_query(F.data == 'btn_sub_ru')
async def sub_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        VK_C = 0x43

        SendInput(VK_C, 0, 0, 0)
        SendInput(VK_C, 0, 2, 0)
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


@dp.callback_query(F.data == 'btn_sounds_video_ru')
async def sounds_video_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        VK_M = 0x4D

        SendInput(VK_M, 0, 0, 0)
        SendInput(VK_M, 0, 2, 0)
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


@dp.callback_query(F.data == 'btn_mini_player_ru')
async def mini_player_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        VK_I = 0x49

        SendInput(VK_I, 0, 0, 0)
        SendInput(VK_I, 0, 2, 0)
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# the next video button is in Russian
@dp.callback_query(F.data == 'btn_update_ru')
async def update_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.answer("Доступ запрещён!")
        return
    try:
        keyboard.send('f5')
        await call.answer("Выполнено!", show_alert=False)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


# Sites in Russian
@dp.callback_query(lambda call: call.data == 'sait_commands_ru')
async def sait_commands_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Команды сайта:</b>\n
""", reply_markup=markup_sait_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Назад🔙", callback_data="btn_back_ru")
btn_chatgpt_ru = InlineKeyboardButton(text="Chat GPT🤖", callback_data="btn_chatgpt_ru")
btn_youtube_ru = InlineKeyboardButton(text="Youtube▶️", callback_data="btn_youtube_ru")
btn_vk_ru = InlineKeyboardButton(text="Vk🌐", callback_data="btn_vk_ru")
btn_x_ru = InlineKeyboardButton(text="X⚡", callback_data="btn_x_ru")
btn_rutube_ru = InlineKeyboardButton(text="Rutube🎬", callback_data="btn_rutube_ru")
btn_binance_ru = InlineKeyboardButton(text="Binance💰📈", callback_data="btn_binance_ru")
btn_bybit_ru = InlineKeyboardButton(text="ByBit💹📊", callback_data="btn_bybit_ru")
btn_okx_ru = InlineKeyboardButton(text="OKX🔐💵", callback_data="btn_okx_ru")
btn_git_ru = InlineKeyboardButton(text="GitHub💻", callback_data="btn_git_ru")
btn_gmail_ru = InlineKeyboardButton(text="Gmail📩", callback_data="btn_gmail_ru")
btn_wiki_ru = InlineKeyboardButton(text="ВикипедиЯ🔎", callback_data="btn_wiki_ru")
markup_sait_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_chatgpt_ru, btn_youtube_ru],
    [btn_vk_ru, btn_x_ru, btn_rutube_ru],
    [btn_binance_ru, btn_bybit_ru, btn_okx_ru],
    [btn_git_ru, btn_gmail_ru, btn_wiki_ru],
])


# Back button in Russian
@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")


# ChatGPT button in Russian and the command "/chat_gpt"
@dp.callback_query(lambda call: call.data == 'btn_chatgpt_ru')
@dp.message(Command("chat_gpt"))
async def chatgpt_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            webbrowser.open("https://chatgpt.com")
            msg = await message.answer("Запуск Chat GPT")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# YouTube button in Russian and the command "/youtube"
@dp.callback_query(lambda call: call.data == 'btn_youtube_ru')
@dp.message(Command("youtube"))
async def youtube_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://youtube.com")
            msg = await message.answer("Запуск YouTube")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# vk button in Russian and the command "/vk"
@dp.callback_query(lambda call: call.data == 'btn_vk_ru')
@dp.message(Command("vk"))
async def vk_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            webbrowser.open("https://vk.com")
            msg = await message.answer("Запуск VK")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The x button in Russian and the "/x" command
@dp.callback_query(lambda call: call.data == 'btn_x_ru')
@dp.message(Command("x"))
async def x_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://x.com")
            msg = await message.answer("Запуск X")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The Rutube button in Russian and the command "/rutube"
@dp.callback_query(lambda call: call.data == 'btn_rutube_ru')
@dp.message(Command("rutube"))
async def rutube_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            webbrowser.open("https://rutube.ru")
            msg = await message.answer("Запуск Rutube")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
       await message.answer("Доступ запрещён!")


# Binance button in Russian and the command "/binance"
@dp.callback_query(lambda call: call.data == 'btn_binance_ru')
@dp.message(Command("binance"))
async def binance_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://www.binance.com/ru")
            msg = await message.answer("Запуск Binance")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The ByBit button in Russian and the command "/bybit"
@dp.callback_query(lambda call: call.data == 'btn_bybit_ru')
@dp.message(Command("bybit"))
async def bybit_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://www.bybit.com/ru-RU/")
            msg = await message.answer("Запуск ByBit")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# OKX button in Russian and the command "/okx"
@dp.callback_query(lambda call: call.data == 'btn_okx_ru')
@dp.message(Command("okx"))
async def okx_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://www.okx.com/ru")
            msg = await message.answer("Запуск OKX")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The GitHub button in Russian and the command "/git_hub"
@dp.callback_query(lambda call: call.data == 'btn_git_ru')
@dp.message(Command("git_hub"))
async def git_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://github.com")
            msg = await message.answer("Запуск GitHub")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# Gmail button in Russian and the command "/gmail"
@dp.callback_query(lambda call: call.data == 'btn_gmail_ru')
@dp.message(Command("gmail"))
async def wiki_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://gmail.com")
            msg = await message.answer("Запуск Gmail")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# Wikipedia button in Russian and the command "/wikipedia"
@dp.callback_query(lambda call: call.data == 'btn_wiki_ru')
@dp.message(Command("wikipedia"))
async def wiki_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            webbrowser.open("https://ru.wikipedia.org/wiki/Заглавная_страница")
            msg = await message.answer("Запуск ВикипедиЯ")
            await asyncio.sleep(15)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# information about the computer in Russian
@dp.callback_query(lambda call: call.data == 'my_computer_ru')
async def my_computer_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Команды о моём ПК:</b>\n
""", reply_markup=markup_my_computer_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_systeminfo_ru = InlineKeyboardButton(text="Информация о системе💻", callback_data="btn_systeminfo_ru")
btn_power_info_ru = InlineKeyboardButton(text="Информация о заряде🪫", callback_data="btn_power_info_ru")
btn_ports_info_ru = InlineKeyboardButton(text="Порты🔓", callback_data="btn_ports_info_ru")
btn_disk_usage_ru = InlineKeyboardButton(text="Диски 💾", callback_data="btn_disk_usage_ru")
btn_screen_expansion_ru = InlineKeyboardButton(text="Расширение экрана 📺", callback_data="btn_screen_expansion_ru")
markup_my_computer_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_systeminfo_ru],
    [btn_power_info_ru],
    [btn_ports_info_ru],
    [btn_disk_usage_ru],
    [btn_screen_expansion_ru]
])


# Back button in English
@dp.callback_query(F.data == 'btn_back_ru')
async def go_back_ru(call: CallbackQuery):
    if is_authorized(call.message):
        await cont_ru(call)
    else:
        await call.message.answer("Доступ запрещён!")


# Function for getting information about the processor for Windows
def get_cpu_brand_ru():
    try:
        result = subprocess.check_output("wmic cpu get name", shell=True).decode().strip()
        cpu_brand = result.split("\n")[1].strip()
    except Exception as e:
        cpu_brand = f"Ошибка при получении информации о процессоре: {e}"
    return cpu_brand

# Function for getting information about the system
def get_system_info_ru():
    uname = platform.uname()
    boot_time = psutil.boot_time()
    boot_time_formatted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(boot_time))
    cpu_brand = get_cpu_brand_ru()

    system_info_ru = (
        f"🖥️ **Информация о системе**\n"
        f"**ОС:** {uname.system} {uname.release} (Версия: {uname.version})\n"
        f"**Имя:** {uname.node}\n"
        f"**Процессор:** {cpu_brand}\n"
        f"**Частота процессора:** {psutil.cpu_freq().max:.2f} МГц\n"
        f"**Ядер всего:** {psutil.cpu_count(logical=False)} | **Потоков:** {psutil.cpu_count(logical=True)}\n"
        f"**Время загрузки:** {boot_time_formatted}\n\n"
        f"📊 **Статистика использования**\n"
        f"**Загрузка CPU:** {psutil.cpu_percent()}%\n"
        f"**Использование памяти:** {psutil.virtual_memory().percent}%\n"
    )

    return system_info_ru


# Button handler for displaying system information
@dp.callback_query(lambda call: call.data == "btn_systeminfo_ru")
async def send_system_info_ru(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            info = get_system_info_ru()
            await call.message.reply(info, parse_mode="Markdown")
        except Exception as e:
            error = await call.message.reply(f"Ошибка при получении информации о системе: {str(e)}")
            await asyncio.sleep(10)
            await error.delete()
    else:
        await call.message.answer("Доступ запрещён!")


# Function for getting nutrition information
def get_power_info_ru():
    try:
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Подключено к сети" if battery.power_plugged else "Работает от батареи"
            percent = battery.percent
            time_left = (
                f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m"
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED
                else "Подсчитывается..."
            )
            power_info = (
                f"🔋 **Информация о питании**\n"
                f"**Уровень заряда:** {percent}%\n"
                f"**Состояние:** {plugged}\n"
                f"**Оставшееся время:** {time_left}\n"
            )
        else:
            power_info = "⚠️ Невозможно получить информацию о батарее. Вы используете настольный ПК без батареи?"

        return power_info
    except Exception as e:
        return f"Ошибка при получении информации о питании: {e}"


# Button handler for displaying power information
@dp.callback_query(lambda call: call.data == "btn_power_info_ru")
async def send_power_info_ru(call: CallbackQuery):
    if is_authorized(call.message):
        power_info = get_power_info_ru()
        await call.message.answer(power_info, parse_mode="Markdown")
    else:
        await call.message.answer("Доступ запрещён!")

# Function for getting information about ports
async def get_ports_info_ru(call: CallbackQuery):
    try:
        open_ports = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == psutil.CONN_LISTEN:
                open_ports.append(conn.laddr.port)
        if not open_ports:
            ports_info = "🔒 Открытые порты не обнаружены. Ваш ПК в безопасности."
        else:
            ports_info = "🔓 Найдены открытые порты:\n" + "\n".join([f"• Порт {port}" for port in open_ports])

        public_ip = requests.get("https://api.ipify.org").text
        shodan_response = requests.get(f"https://api.shodan.io/shodan/host/{public_ip}?key={SHODAN_API_KEY}")

        if shodan_response.status_code == 200:
            shodan_data = shodan_response.json()
            advice = "🛡️ Рекомендации по безопасности:\n" + "\n".join(
                [f"• {item['port']} - {item['transport']} ({item['product']})" for item in shodan_data.get('data', [])]
            )
        else:
            advice = "Не удалось получить данные о безопасности из Shodan."

        await call.message.answer(f"{ports_info}\n\n🌍 Ваш публичный IP: {public_ip}\n\n{advice}")
    except Exception as e:
        await call.message.answer(f"⚠ Произошла ошибка: {e}")

# Button handler for getting information about ports
@dp.callback_query(lambda call: call.data == "btn_ports_info_ru")
async def handle_ports_info_ru(call: CallbackQuery):
    await get_ports_info_ru(call)


def get_disk_usage_ru():
    try:
        drives = [f"{partition.device}" for partition in psutil.disk_partitions()]
        usage_info = []

        for drive in drives:
            usage = psutil.disk_usage(drive)
            drive_letter = drive.rstrip(":\\")
            total = round(usage.total / (1024 ** 3), 2)
            used = round(usage.used / (1024 ** 3), 2)
            free = round(usage.free / (1024 ** 3), 2)
            percent = usage.percent

            usage_info.append(f"Диск {drive_letter} :\n"
                              f"Всего: {total} ГБ\n"
                              f"Занято: {used} ГБ ({percent}%)\n"
                              f"Свободно: {free} ГБ\n")

        return "\n".join(usage_info)

    except Exception as e:
        return f"⚠ Ошибка при получении данных о диске: {str(e)}"

@dp.callback_query(lambda call: call.data == "btn_disk_usage_ru")
async def send_disk_usage_ru(call: CallbackQuery):
    try:
        disk_usage = get_disk_usage_ru()
        await call.message.reply(f"💾 Информация о диске:\n\n{disk_usage}", parse_mode="Markdown")
    except Exception as e:
        error = await call.message.reply(f"⚠ Ошибка при получении данных: {str(e)}")
        await asyncio.sleep(10)
        await error.delete()


def get_screen_resolution():
    width, height = pyautogui.size()
    return width, height

@dp.callback_query(F.data == "btn_screen_expansion_ru")
async def send_screen_resolution(call: CallbackQuery):
    if is_authorized(call.message):
        try:
            width, height = get_screen_resolution()
            info = f"Разрешение экрана: **{width}x{height}**"
            await call.message.reply(info, parse_mode="Markdown")
        except Exception as e:
            await call.message.reply(f"⚠ Ошибка: {str(e)}")
    else:
        await call.message.answer("Доступ запрещён!")



@dp.callback_query(lambda call: call.data == 'clearing_ru')
async def clearing_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Команды по очистке:</b>\n
    """, reply_markup=markup_clearing_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_empty_trash_ru = InlineKeyboardButton(text="Очистить корзину 🗑️", callback_data="btn_empty_trash_ru")
btn_empty_temp_ru = InlineKeyboardButton(text="Очистка папки %temp%📁", callback_data="btn_empty_temp_ru")
btn_empty_ram_ru = InlineKeyboardButton(text="Очистка RAM📁", callback_data="btn_empty_ram_ru")
btn_clear_startup_ru = InlineKeyboardButton(text="Очистить автозагрузку🚀", callback_data="btn_clear_startup_ru")
# btn_empty_all_msg_ru = InlineKeyboardButton(text="Очистить все сообщения 💬", callback_data="btn_empty_all_msg_ru")
markup_clearing_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_empty_trash_ru],
    [btn_empty_temp_ru],
    [btn_empty_ram_ru],
    [btn_clear_startup_ru],
])


# The "Empty trash" button in Russian and the command "/empty_trash"
@dp.callback_query(lambda call: call.data == 'btn_empty_trash_ru')
@dp.message(Command("empty_trash"))
async def empty_trash_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:

            os.system('PowerShell -Command "Clear-RecycleBin -Force" >$null 2>&1')

            trash = await message.answer("Корзина успешно очищена!")

            await asyncio.sleep(30)
            await trash.delete()
        except Exception as e:
            error_message = await message.answer(f"⚠ Ошибка: {str(e)}")
            await asyncio.sleep(10)
            await error_message.delete()
    else:
        access_message = await message.answer("Доступ запрещён!")
        await asyncio.sleep(10)
        await access_message.delete()


@dp.callback_query(F.data == "btn_empty_temp_ru")
async def clear_temp_folder_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return
    try:
        if os.path.exists(TEMP_FOLDER):
            for filename in os.listdir(TEMP_FOLDER):
                file_path = os.path.join(TEMP_FOLDER, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    pass
            msg = await call.message.answer("Папка %temp% успешно очищена!")
            await asyncio.sleep(25)
            await msg.delete()
        else:
            msg = await call.message.answer("Папка %temp% не была найдена.")
            await asyncio.sleep(25)
            await msg.delete()
    except Exception as e:
        error = await call.message.answer(f"⚠ Во время очистки произошла ошибка: {str(e)}")
        await asyncio.sleep(15)
        await error.delete()

    await call.answer()


# The "empty ram" button in Russian and the command "/empty_ram"
@dp.callback_query(lambda call: call.data == 'btn_empty_ram_ru')
@dp.message(Command("empty_ram"))
async def empty_ram_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            subprocess.run('powershell -Command "Clear-Content -Path memory://"', shell=True)
            msg = await message.answer("Оперативная память успешно очищена!")
            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


# The "Clear startup" button in Russian and the command "/clear_startup"
@dp.callback_query(lambda call: call.data == 'btn_clear_startup_ru')
@dp.message(Command("clear_startup"))
async def clear_startup_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            registry_key = winreg.OpenKey(registry, registry_path, 0, winreg.KEY_WRITE)

            try:
                winreg.DeleteValue(registry_key, "SomeProgram")
            except FileNotFoundError:
                pass

            success_message = await message.answer("Автозагрузка успешно очищена!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при очистке: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")



@dp.callback_query(lambda call: call.data == 'keyboard_control_ru')
async def keyboard_control_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("""<b>Команды по управлению клавиатурой:</b>\n
""", reply_markup=markup_keyboard_control_ru, parse_mode="HTML")

btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_write_text_ru = InlineKeyboardButton(text="Написать текст ✍️", callback_data="btn_write_text_ru")
btn_send_notification_ru = InlineKeyboardButton(text="Отправить уведомление 🔔", callback_data="btn_send_notification_ru")
markup_keyboard_control_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_write_text_ru],
    [btn_send_notification_ru]
])


class TextInputStates(StatesGroup):
    write_text = State()

# Button "Write Text"
@dp.callback_query(F.data == "btn_write_text_ru")
async def ask_text_input(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите текст, который вы хотите ввести на своем компьютере:")
    await call.answer()
    await state.set_state(TextInputStates.write_text)

@dp.message(TextInputStates.write_text)
async def handle_text_input(message: types.Message, state: FSMContext):
    try:
        user_text = message.text

        keyboard.write(user_text)

        await message.reply(f"Текст написан!")
    except Exception as e:
        await message.reply(f"⚠ Произошла ошибка: {str(e)}")
    finally:
        await state.clear()


class NotificationStates(StatesGroup):
    send_notification = State()

# Button "Send Notification"
@dp.callback_query(F.data == "btn_send_notification_ru")
async def ask_notification_text(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите текст, который вы хотите отобразить в качестве уведомления на вашем компьютере:")
    await call.answer()
    await state.set_state(NotificationStates.send_notification)

@dp.message(NotificationStates.send_notification)
async def handle_notification_input(message: types.Message, state: FSMContext):
    try:
        user_text = message.text

        show_windows_notification("smartPC | Lexium", user_text)

        await message.reply(f"Уведомление было успешно отправлено на ваш компьютер.")
    except Exception as e:
        await message.reply(f"⚠ Ошибка произошла: {str(e)}")
    finally:
        await state.clear()

def show_windows_notification(title: str, message: str):
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, message, title, 0x40 | 0x1)



@dp.callback_query(lambda call: call.data == 'btn_browser_management')
async def browser_management_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(f"""<b>Управление браузером:\n\n🌎 Основной браузер:</b> {browser}
""", reply_markup=markup_browser_management_ru, parse_mode="HTML")

btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_search_browser_ru = InlineKeyboardButton(text="Поиск 🔎", callback_data="btn_search_browser_ru")
btn_open_main_browser_ru = InlineKeyboardButton(text="Открыть основной браузер 🌐", callback_data="btn_open_main_browser_ru")
btn_close_browser_ru = InlineKeyboardButton(text="Закрыть браузер ❌", callback_data="btn_close_browser_ru")
btn_open_new_tab_ru = InlineKeyboardButton(text="Создать новую вкладку 🆕", callback_data="btn_open_new_tab_ru")
btn_close_tab_ru = InlineKeyboardButton(text="Закрыть вкладку ❌", callback_data="btn_close_tab_ru")
btn_refresh_browser_ru = InlineKeyboardButton(text="Обновить страницу 🔄", callback_data="btn_refresh_browser_ru")
btn_open_incognito_ru = InlineKeyboardButton(text="Режим инкогнито 👽", callback_data="btn_open_incognito_ru")
btn_browser_history_ru = InlineKeyboardButton(text="История браузера 📜", callback_data="btn_browser_history_ru")
markup_browser_management_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_search_browser_ru],
    [btn_open_main_browser_ru],
    [btn_close_browser_ru],
    [btn_open_new_tab_ru],
    [btn_close_tab_ru],
    [btn_refresh_browser_ru],
    [btn_open_incognito_ru],
    [btn_browser_history_ru]
])


class SearchState(StatesGroup):
    waiting_for_query = State()


@dp.callback_query(F.data == "btn_search_browser_ru")
@dp.message(Command("search_browser"))
async def ask_search_query(event: Union[types.Message, CallbackQuery], state: FSMContext):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    else:
        message = event

    await message.answer("Введите ваш поисковый запрос:")
    await state.set_state(SearchState.waiting_for_query)

@dp.message(SearchState.waiting_for_query)
async def handle_search_query(message: types.Message, state: FSMContext):
    try:
        if is_authorized(message):
            query = quote(message.text)
            search_url = f"https://yandex.ru/search/?text={query}"

            if browser == "Google Chrome":
                subprocess.Popen(["start", "chrome", search_url], shell=True)
            elif browser == "Edge":
                subprocess.Popen(["start", "msedge", search_url], shell=True)
            elif browser == "Firefox":
                subprocess.Popen(["firefox", search_url], shell=True)
            elif browser == "Opera":
                subprocess.Popen(["start", "opera", search_url], shell=True)
            elif browser == "Opera GX":
                subprocess.Popen(["start", "operagx", search_url], shell=True)
            elif browser == "Yandex":
                subprocess.Popen(["start", "yandex", search_url], shell=True)
            else:
                await message.answer(f"⚠ Браузер '{browser}' не поддерживается.")
                return

            success_message = await message.answer(
                f"🔍 Поиск в браузере {browser} по запросу:\n<b>{message.text}</b>", parse_mode="HTML"
            )
            await asyncio.sleep(30)
            await success_message.delete()

        else:
            await message.answer("Доступ запрещён!")

    except Exception as e:
        await message.answer(f"⚠ Ошибка при поиске: {str(e)}")
    finally:
        await state.clear()


# Команда и кнопка для открытия основного браузера
@dp.callback_query(lambda call: call.data == 'btn_open_main_browser_ru')
@dp.message(Command("open_main_browser"))
async def open_main_browser_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        global browser

        try:
            if browser.lower() == "google chrome":
                subprocess.Popen(["start", "chrome"], shell=True)
            elif browser.lower() == "edge":
                subprocess.Popen(["start", "msedge"], shell=True)
            elif browser.lower() == "firefox":
                subprocess.Popen(["start", "firefox"], shell=True)
            elif browser.lower() == "opera":
                subprocess.Popen(["start", "opera"], shell=True)
            elif browser.lower() == "opera gx":
                subprocess.Popen(["start", "operagx"], shell=True)
            elif browser.lower() == "yandex":
                subprocess.Popen(["start", "yandexbrowser"], shell=True)
            else:
                await message.answer(f"❌ Браузер '{browser}' не поддерживается.")
                return

            success_message = await message.answer(f"🌍 Браузер '{browser}' открыт успешно!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при открытии браузера: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_close_browser_ru')
@dp.message(Command("close_browser"))
async def close_browser_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            browser_processes = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe", "yandexbrowser.exe"]

            closed = []
            for process in psutil.process_iter(['pid', 'name']):
                try:
                    if process.info['name'] in browser_processes:
                        process.terminate()
                        closed.append(process.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            if closed:
                success_message = await message.answer(
                    f"Закрыты браузеры: {', '.join(set(closed))}."
                )
            else:
                success_message = await message.answer("Браузеры не найдены среди запущенных процессов.")

            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при закрытии браузера: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_open_new_tab_ru')
@dp.message(Command("open_new_tab"))
async def open_new_tab_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            keyboard.send('ctrl+t')

            success_message = await message.answer("Открыта новая вкладка в браузере!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_close_tab_ru')
@dp.message(Command("close_tab"))
async def close_tab_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            keyboard.send('ctrl+w')
            msg = await message.answer(f"Закрыта одна вкладка")

            await asyncio.sleep(30)
            await msg.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при закрытии вкладки: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_refresh_browser_ru')
@dp.message(Command("refresh_browser"))
async def refresh_browser(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            keyboard.send('f5')

            success_message = await message.answer("Страница обновлена!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'btn_open_incognito_ru')
@dp.message(Command("open_incognito"))
async def open_incognito(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            if browser == "Google Chrome":
                subprocess.Popen(["start", "chrome", "--incognito"], shell=True)
            elif browser == "Edge":
                subprocess.Popen(["start", "msedge", "--inprivate"], shell=True)
            elif browser == "Firefox":
                subprocess.Popen(["firefox", "-private"], shell=True)
            elif browser == "Opera":
                subprocess.Popen(["start", "opera", "--private"], shell=True)
            elif browser == "Opera GX":
                subprocess.Popen(["start", "operagx", "--private"], shell=True)
            elif browser == "Yandex":
                subprocess.Popen(["start", "yandex", "--incognito"], shell=True)
            else:
                await message.answer(f"Браузер '{browser}' не поддерживается.")
                return

            success_message = await message.answer(f"Открыт режим инкогнито в браузере {browser}!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при открытии режима инкогнито: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


BROWSER_HISTORY_PATHS = {
    "google chrome": os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\History",
    "edge": os.path.expanduser("~") + r"\AppData\Local\Microsoft\Edge\User Data\Default\History",
    "firefox": os.path.expanduser("~") + r"\AppData\Roaming\Mozilla\Firefox\Profiles",
    "yandex": os.path.expanduser("~") + r"\AppData\Local\Yandex\YandexBrowser\User Data\Default\History",
    "opera": os.path.expanduser("~") + r"\AppData\Roaming\Opera Software\Opera Stable\History",
    "opera gx": os.path.expanduser("~") + r"\AppData\Roaming\Opera Software\Opera GX Stable\History"
}


def get_browser_history(browser_name, limit=10):
    browser_name = browser_name.lower()

    if browser_name not in BROWSER_HISTORY_PATHS:
        return f"❌ Браузер '{browser_name}' не поддерживается."

    history_path = BROWSER_HISTORY_PATHS[browser_name]

    if not os.path.exists(history_path):
        return f"📛 История браузера '{browser_name}' не найдена."

    try:
        temp_path = history_path + "_copy"
        shutil.copy2(history_path, temp_path)

        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()

        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?", (limit,))
        history = cursor.fetchall()

        conn.close()
        os.remove(temp_path)

        if not history:
            return f"📂 История браузера '{browser_name}' пуста."

        response = f"📜 <b>История браузера ({browser_name}):</b>\n\n"
        for url, title, _ in history:
            response += f"🔹 <b>{title}</b>\n{url}\n\n"

        return response
    except Exception as e:
        return f"⚠ Ошибка при получении истории: {str(e)}"


@dp.callback_query(lambda call: call.data == 'btn_browser_history_ru')
@dp.message(Command("browser_history"))
async def get_browser_history_command(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        global browser

        if not browser:
            await message.answer("❌ Глобальная переменная 'browser' не задана.")
            return

        history_result = get_browser_history(browser)

        await message.answer(history_result, parse_mode="HTML")
    else:
        await message.answer("Доступ запрещён!")


@dp.callback_query(lambda call: call.data == 'files_ru')
async def files_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(f"""<b>Файловая система:</b>\n\n<b>Диск:</b> {disk_path}
""", reply_markup=markup_files_ru, parse_mode="HTML")

btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_open_explorer_ru = InlineKeyboardButton(text="Открыть Проводник 🖥️", callback_data="btn_open_explorer_ru")
btn_create_folder_ru = InlineKeyboardButton(text="Создать папку 📁", callback_data="btn_create_folder_ru")
btn_create_file_txt_ru = InlineKeyboardButton(text="Создать файл .txt 📝", callback_data="btn_create_file_txt_ru")
btn_create_docx_file_ru = InlineKeyboardButton(text="Создать файл .docx 📄", callback_data="btn_create_docx_file_ru")
btn_upload_file_ru = InlineKeyboardButton(text="Скинуть файл 📤", callback_data="btn_upload_file_ru")
markup_files_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_open_explorer_ru],
    [btn_create_folder_ru],
    [btn_create_file_txt_ru],
    [btn_create_docx_file_ru],
    [btn_upload_file_ru]
])


@dp.callback_query(lambda call: call.data == 'btn_open_explorer_ru')
@dp.message(Command("open_explorer"))
async def open_explorer_ru(event):
    if isinstance(event, CallbackQuery):
        message = event.message
        await event.answer()
    elif isinstance(event, Message):
        message = event

    if is_authorized(message):
        try:
            os.system('explorer.exe')

            success_message = await message.answer("Проводник открыт успешно!")
            await asyncio.sleep(30)
            await success_message.delete()
        except Exception as e:
            await message.answer(f"⚠ Ошибка при открытии проводника: {str(e)}")
    else:
        await message.answer("Доступ запрещён!")


class FolderCreationStates(StatesGroup):
    create_folder = State()

@dp.callback_query(F.data == "btn_create_folder_ru")
async def ask_folder_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите имя папки, которую вы хотите создать:")
    await call.answer()
    await state.set_state(FolderCreationStates.create_folder)

@dp.message(FolderCreationStates.create_folder)
async def handle_folder_creation(message: types.Message, state: FSMContext):
    folder_name = message.text.strip()

    full_path = os.path.join(disk_path, folder_name)

    try:
        if not os.path.exists(full_path):
            os.makedirs(full_path)
            await message.reply(f"📂 Папка '{folder_name}' была успешно создана на {disk_path}.")
        else:
            await message.reply(f"⚠ Папка с именем '{folder_name}' уже существует на {disk_path}.")
    except Exception as e:
        await message.reply(f"⚠ Ошибка: {str(e)}")
    finally:
        await state.clear()


class FileCreationStates_txt(StatesGroup):
    create_file_txt = State()

# Button "Create File"
@dp.callback_query(F.data == "btn_create_file_txt_ru")
async def ask_file_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите имя файла, который вы хотите создать:")
    await call.answer()
    await state.set_state(FileCreationStates_txt.create_file_txt)

@dp.message(FileCreationStates_txt.create_file_txt)
async def handle_file_creation(message: types.Message, state: FSMContext):
    file_name = message.text.strip()
    if not file_name.endswith(".txt"):
        file_name += ".txt"


    full_path = os.path.join(disk_path, file_name)

    try:
        if not os.path.exists(full_path):
            with open(full_path, 'x') as file:
                file.write("")
            await message.reply(f"Файл '{file_name}' был успешно создан на {disk_path}.")
        else:
            await message.reply(f"Файл с именем '{file_name}' уже существует на {disk_path}.")
    except FileExistsError:
        await message.reply(f"Файл с именем '{file_name}' уже существует на {disk_path}.")
    except Exception as e:
        await message.reply(f"⚠ Ошибка: {str(e)}")
    finally:
        await state.clear()


class FileCreationStates(StatesGroup):
    create_docx_file = State()

# Button "Create .docx File"
@dp.callback_query(F.data == "btn_create_docx_file_ru")
async def ask_docx_file_name(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите имя файла, который вы хотите создать:")
    await call.answer()
    await state.set_state(FileCreationStates.create_docx_file)

@dp.message(FileCreationStates.create_docx_file)
async def handle_docx_file_creation(message: types.Message, state: FSMContext):
    try:
        file_name = message.text.strip()
        if not file_name.endswith(".docx"):
            file_name += ".docx"

        full_path = os.path.join(disk_path, file_name)

        if not os.path.exists(full_path):
            with open(full_path, 'w') as file:
                file.write("")
            await message.reply(f"Файл '{file_name}'был успеш"
                                f"но создан на {disk_path}.")
        else:
            await message.reply(f"Файл с именем '{file_name}' уже существует на {disk_path}.")
    except Exception as e:
        await message.reply(f"⚠ Ошибка: {str(e)}")
    finally:
        await state.clear()


class FileUploadStates(StatesGroup):
    upload_file = State()

@dp.callback_query(F.data == "btn_upload_file_ru")
async def ask_for_file(call: CallbackQuery, state: FSMContext):
    await call.message.answer("📂 Отправьте файл, который вы хотите загрузить на компьютер.")
    await call.answer()
    await state.set_state(FileUploadStates.upload_file)

@dp.message(FileUploadStates.upload_file)
async def handle_uploaded_file(message: types.Message, state: FSMContext):
    try:
        file_id = None
        file_name = "unknown_file"

        if message.document:
            file_id = message.document.file_id
            file_name = message.document.file_name
        elif message.photo:
            file_id = message.photo[-1].file_id
            file_name = f"photo_{message.photo[-1].file_unique_id}.jpg"
        elif message.audio:
            file_id = message.audio.file_id
            file_name = message.audio.file_name
        elif message.voice:
            file_id = message.voice.file_id
            file_name = f"voice_{message.voice.file_unique_id}.ogg"
        elif message.video:
            file_id = message.video.file_id
            file_name = message.video.file_name
        elif message.video_note:
            file_id = message.video_note.file_id
            file_name = f"video_note_{message.video_note.file_unique_id}.mp4"

        if not file_id:
            await message.reply("⚠ Этот тип файлов не поддерживается.")
            return

        file = await bot.get_file(file_id)
        file_path = file.file_path
        save_path = os.path.join(disk_path, file_name)

        await bot.download_file(file_path, save_path)

        await message.reply(f"✅ Файл {file_name} успешно сохранён в {disk_path}!")
    except Exception as e:
        await message.reply(f"⚠ Ошибка при загрузке файла: {str(e)}")
    finally:
        await state.clear()


# Pro functions in English
@dp.callback_query(lambda call: call.data == 'pro_func_ru')
async def pro_func_ru(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>Pro функции:</b>\n", reply_markup=markup_pro_func_ru, parse_mode="HTML")


btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
btn_webcam_shot_ru = InlineKeyboardButton(text="Снимок с вебки 📸", callback_data="btn_webcam_shot_ru")
btn_webcam_record_ru = InlineKeyboardButton(text="Запись вебки 📹", callback_data="btn_webcam_record_ru")
btn_audio_record_ru = InlineKeyboardButton(text="Запись звука 🔊", callback_data="btn_audio_record_ru")
btn_clipboard_text_ru = InlineKeyboardButton(text="Буфер обмена 🔤", callback_data="btn_clipboard_text_ru")
btn_active_window_screenshot_ru = InlineKeyboardButton(text="Скриншот активного окна 🖼", callback_data="btn_active_window_screenshot_ru")
btn_secret_mode_ru = InlineKeyboardButton(text="Секретный режим 🔐", callback_data="btn_secret_mode_ru")
markup_pro_func_ru = InlineKeyboardMarkup(inline_keyboard=[
    [btn_back_ru],
    [btn_webcam_shot_ru],
    [btn_webcam_record_ru],
    [btn_audio_record_ru],
    [btn_clipboard_text_ru],
    [btn_active_window_screenshot_ru],
    [btn_secret_mode_ru]
])


@dp.callback_query(F.data == 'btn_webcam_shot_ru')
async def webcam_shot_ru(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("Не удалось получить доступ к веб-камере. Пожалуйста, убедитесь, что она подключена и не используется.")

        ret, frame = cam.read()
        cam.release()
        if not ret:
            raise Exception("Не удалось получить изображение с веб-камеры.")

        image_path = "webcam_shot.jpg"
        cv2.imwrite(image_path, frame)

        photo = FSInputFile(image_path)
        await call.message.answer_photo(photo, caption="Вот снимок с вашей веб-камеры! 📸")
        os.remove(image_path)
    except Exception as e:
        await call.message.answer(f"⚠ Ошибка: {str(e)}")


awaiting_input_type = None

@dp.callback_query(F.data == 'btn_webcam_record_ru')
async def webcam_record_request(call: CallbackQuery):
    global awaiting_input_type
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return

    awaiting_input_type = "video"
    await call.message.answer("Введите продолжительность видеозаписи в секундах (1-60):")

@dp.callback_query(F.data == 'btn_audio_record_ru')
async def audio_record_request(call: CallbackQuery):
    global awaiting_input_type
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return

    awaiting_input_type = "audio"
    await call.message.answer("Введите продолжительность аудиозаписи в секундах (1-60):")

@dp.message()
async def process_duration_input(message: Message):
    global awaiting_input_type
    if not awaiting_input_type:
        return

    try:
        duration = int(message.text)
        if duration < 1 or duration > 60:
            raise ValueError("Продолжительность вне диапазона.")

        if awaiting_input_type == "video":
            await record_video(message, duration)
        elif awaiting_input_type == "audio":
            await record_audio(message, duration)
    except ValueError:
        await message.reply("Неверный ввод. Пожалуйста, введите число от 1 до 60.")
    except Exception as e:
        error = await message.answer(f"Ошибка: {str(e)}")
        await asyncio.sleep(10)
        await error.delete()
    finally:
        awaiting_input_type = None

async def record_video(message: Message, duration: int):
    try:
        video_path = "webcam_recording.avi"
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("Не удалось получить доступ к веб-камере.")

        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (frame_width, frame_height))

        await message.answer(f"Запись видео для {duration} секунд. Пожалуйста подождите...")
        for _ in range(duration * 20):
            ret, frame = cam.read()
            if not ret:
                break
            out.write(frame)

        cam.release()
        out.release()

        video = FSInputFile(video_path)
        await message.answer_video(video, caption="Вот ваша запись! 🎥")
        os.remove(video_path)
    except Exception as e:
        raise e

async def record_audio(message: Message, duration: int):
    try:
        audio_path = "audio_recording.wav"
        sample_rate = 44100
        channels = 2

        await message.answer(f"Запись звука в течение {duration} секунд. Пожалуйста подождите...")
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()

        with wave.open(audio_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        audio = FSInputFile(audio_path)
        await message.answer_voice(audio, caption="Вот ваша записанная аудиозапись! 🎙️")
        os.remove(audio_path)
    except Exception as e:
        raise e


@dp.callback_query(F.data == 'btn_active_window_screenshot_ru')
async def screenshot_active_window(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return

    try:
        active_window = gw.getActiveWindow()
        if not active_window:
            await call.message.reply("Активного окна не обнаружено. Пожалуйста, убедитесь, что окно активно.")
            return

        left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height

        screenshot_path = "active_window_screenshot.png"
        with mss.mss() as sct:
            region = {"top": top, "left": left, "width": width, "height": height}
            sct_img = sct.grab(region)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=screenshot_path)

        photo = FSInputFile(screenshot_path)
        await call.message.answer_photo(photo, caption="Вот скриншот вашего активного окна! 🖼️")

        os.remove(screenshot_path)

    except Exception as e:
        await call.message.reply(f"⚠ Ошибка: {str(e)}")


def create_virtual_desktop():
    user32 = ctypes.windll.user32
    user32.keybd_event(0x11, 0, 0, 0)  # Нажимаем Ctrl
    user32.keybd_event(0x5B, 0, 0, 0)  # Нажимаем Win
    user32.keybd_event(0x44, 0, 0, 0)  # Нажимаем D (Win + Ctrl + D)
    user32.keybd_event(0x44, 0, 2, 0)  # Отпускаем D
    user32.keybd_event(0x5B, 0, 2, 0)  # Отпускаем Win
    user32.keybd_event(0x11, 0, 2, 0)  # Отпускаем Ctrl


@dp.callback_query(F.data == 'btn_secret_mode_ru')
async def secret_mode_en(call: CallbackQuery):
    if not is_authorized(call.message):
        await call.message.reply("Доступ запрещён!")
        return

    try:
        await call.message.answer("Создаем новый виртуальный рабочий стол...")
        create_virtual_desktop()

        await call.message.answer("Приглушение громкости системы...")
        set_volume_pycaw(0)

        await call.message.answer("Активирован секретный режим! 🔒 Теперь открыт новый виртуальный рабочий стол.")

    except Exception as e:
        error = await call.message.answer(f"⚠ Ошибка: {str(e)}")
        await asyncio.sleep(10)
        await error.delete()


@dp.callback_query(F.data == 'btn_clipboard_text_ru')
async def send_clipboard_text(call: CallbackQuery):
    try:
        if not is_authorized(call.message):
            await call.message.reply("Доступ запрещён!")
            return

        clipboard_text = pyperclip.paste()

        if not clipboard_text:
            await call.message.answer("Буфер обмена пуст! 📝")
        else:
            await call.message.answer(f"Содержимое буфера обмена:\n\n{clipboard_text}")

    except Exception as e:
        error = await call.message.answer(f"⚠ Ошибка: {str(e)}")
        await asyncio.sleep(10)
        await error.delete()


def apply_dnd_mode(enabled):
    if enabled:
        os.system('powershell.exe -Command "New-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings -Name NOC_GLOBAL_SETTING_TOASTS_ENABLED -Value 0 -PropertyType DWORD -Force | Out-Null"')
    else:
        os.system('powershell.exe -Command "Remove-ItemProperty -Path HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings -Name NOC_GLOBAL_SETTING_TOASTS_ENABLED -ErrorAction SilentlyContinue | Out-Null"')



def create_personal_account_markup_ru(dnd_enabled: bool):
#    dnd_button_text = "Выкл 'Не беспокоить' ❌" if dnd_enabled else "Вкл 'Не беспокоить' ✅"
    dnd_callback_data = 'btn_disable_dnd_ru' if dnd_enabled else 'btn_enable_dnd_ru'

    btn_back_ru = InlineKeyboardButton(text="Назад 🔙", callback_data="btn_back_ru")
    edit_favorites_ru = InlineKeyboardButton(text="Редактировать избранное ❤️", callback_data='edit_favorites')
    change_disk_button = InlineKeyboardButton(text="Сменить диск 💾", callback_data="change_disk")
    main_browser_button = InlineKeyboardButton(text="Основной браузер 🌐", callback_data="select_main_browser")

    return InlineKeyboardMarkup(inline_keyboard=[
        [btn_back_ru],
#        [InlineKeyboardButton(text=dnd_button_text, callback_data=dnd_callback_data)],
        [change_disk_button],
        [main_browser_button],
        [edit_favorites_ru],
    ])


def create_browser_selection_markup():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Google Chrome 🌐", callback_data="set_browser_chrome")],
        [InlineKeyboardButton(text="Edge 🔍", callback_data="set_browser_edge")],
        [InlineKeyboardButton(text="Firefox 🦊", callback_data="set_browser_firefox")],
        [InlineKeyboardButton(text="Opera 🌍", callback_data="set_browser_opera")],
        [InlineKeyboardButton(text="Opera GX 💬", callback_data="set_browser_opera_gx")],
    ])


@dp.callback_query(lambda call: call.data == 'personal_account_ru')
async def personal_account_ru(call: types.CallbackQuery):
    await call.message.delete()
    global do_not_disturb_enabled, browser
    username = call.from_user.username or "Не указан"
    user_id = call.from_user.id

#    dnd_status = "вкл✅" if do_not_disturb_enabled else "выкл❌"

    text = f"""
👤 ЛИЧНЫЙ АККАУНТ — {username} :

🌍 Язык: 🇷🇺

📁 Основной диск: {disk_path}

🌐 Основной браузер: {browser}

🛠️ Версия: Pro v1.1 

🆔 Ваш ID: {user_id}
    """

    message = await call.message.answer(text, reply_markup=create_personal_account_markup_ru(do_not_disturb_enabled))
    user_data[call.from_user.id] = {"message_id": message.message_id}


@dp.callback_query(lambda call: call.data == 'select_main_browser')
async def select_main_browser(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выберите основной браузер:", reply_markup=create_browser_selection_markup())


@dp.callback_query(lambda call: call.data.startswith("set_browser_"))
async def set_browser(call: types.CallbackQuery):
    global browser
    browser_map = {
        "set_browser_chrome": "Google Chrome",
        "set_browser_edge": "Edge",
        "set_browser_firefox": "Firefox",
        "set_browser_opera": "Opera",
        "set_browser_opera_gx": "Opera GX"
    }

    browser = browser_map.get(call.data, "Неизвестный браузер")

    settings = load_settings()
    settings["browser"] = browser

    save_settings(settings)

    await call.answer(f"Основной браузер изменён на {browser}!")
    await personal_account_ru(call)


@dp.callback_query(lambda call: call.data == 'btn_enable_dnd_ru')
async def enable_dnd(call: types.CallbackQuery):
    global do_not_disturb_enabled
    do_not_disturb_enabled = True
    apply_dnd_mode(do_not_disturb_enabled)

    settings = load_settings()
    settings["do_not_disturb_enabled"] = do_not_disturb_enabled
    save_settings(settings)

    await personal_account_ru(call)


@dp.callback_query(lambda call: call.data == 'btn_disable_dnd_ru')
async def disable_dnd(call: types.CallbackQuery):
    global do_not_disturb_enabled
    do_not_disturb_enabled = False
    apply_dnd_mode(do_not_disturb_enabled)

    settings = load_settings()
    settings["do_not_disturb_enabled"] = do_not_disturb_enabled
    save_settings(settings)

    await personal_account_ru(call)


FAVOURITES_FILE = "user_favourites.json"

def load_favourites():
    if os.path.exists(FAVOURITES_FILE):
        with open(FAVOURITES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_favourites():
    with open(FAVOURITES_FILE, 'w') as f:
        json.dump(user_favourites, f)

user_favourites = load_favourites()

available_functions = {
    'btn_shutdown_ru': 'Завершение работы ✅',
    'btn_restart_ru': 'Перезагрузка 🔄',
    'btn_sleep_ru': 'Спящий режим 😴',
    'btn_lock_ru': 'Заблокировать экран 🔒',
    'btn_screenshot_ru': 'Скриншот 📸',
    'btn_switch_layout_ru': 'Изменить язык 🌐',
    'btn_collapse_ru': 'Свернуть окна 🖥',
    'btn_scroll_up_ru': 'Скролл вверх ⬆️',
    'btn_scroll_down_ru': 'Скролл вниз ⬇️',
    'btn_full_screen_ru': 'Полный экран 🖥',
    'btn_volume_ru': 'Изменение звука 🔊',
    'btn_set_brightness_ru': 'Изменение яркости 💡',
    'btn_back_ru': 'Back 🔙',
    'btn_space_ru': 'Пробел',
    'btn_enter_ru': 'Enter',
    'btn_esc_ru': 'ESC',
    'btn_tab_ru': 'TAB',
    'btn_del_ru': 'DEL',
    'btn_backspace_ru': 'Backspace',
    'btn_capslock_ru': 'CAPS Lock',
    'btn_rmb_ru': 'ПКМ',
    'btn_lmb_ru': 'ЛКМ',
    'btn_telegram_ru': 'Telegram ✈️',
    'btn_chrome_ru': 'Google Chrome 🌐',
    'btn_opera_ru': 'Opera 🌍',
    'btn_edge_ru': 'Microsoft Edge 🔍',
    'btn_firefox_ru': 'Firefox 🦊',
    'btn_yandex_ru': 'Яндекс 🔎',
    'btn_discord_ru': 'Discord 💬',
    'btn_steam_ru': 'Steam 🎮',
    'btn_console_ru': 'Консоль 🖥',
    'btn_play_ru': 'Пауза / Продолжить ▶️',
    'btn_next_ru': 'Следующее видео ⏭️',
    'btn_full_video_ru': 'Полный экран видео 📹',
    'btn_sub_ru': 'Вкл/выкл субтитры 🔤',
    'btn_sounds_video_ru': 'Вкл/выкл звук 🔈',
    'btn_mini_player_ru': 'Мини-проигрыватель 📺',
    'btn_update_ru': 'Обновить страницу 🔄',
    'btn_chatgpt_ru': 'ChatGPT 🤖',
    'btn_youtube_ru': 'YouTube ▶️',
    'btn_vk_ru': 'VK 🌐',
    'btn_x_ru': 'X ⚡️',
    'btn_rutube_ru': 'Rutube 🎬',
    'btn_binance_ru': 'Binance 💰',
    'btn_bybit_ru': 'ByBit 💹',
    'btn_okx_ru': 'OKX 🔐',
    'btn_git_ru': 'GitHub 💻',
    'btn_gmail_ru': 'Gmail 📩',
    'btn_wiki_ru': 'Википедия 🔎',
    'btn_systeminfo_ru': 'Информация о системе 💻',
    'btn_power_info_ru': 'Информация о заряде 🔋',
    'btn_ports_info_ru': 'Порты 🔓',
    'btn_disk_usage_ru': 'Диски C и D 💾',
    'btn_screen_expansion_ru': 'Расширение экрана 📺',
    'btn_empty_trash_ru': 'Очистить корзину 🗑',
    'btn_empty_temp_ru': 'Очистка папки %temp% 📁',
    'btn_empty_ram_ru': 'Очистка RAM 📁',
    'btn_clear_startup_ru': 'Очистить автозагрузку 🚀',
    'btn_write_text_ru': 'Написать текст ✍️',
    'btn_send_notification_ru': 'Отправить уведомление 🔔',
    'btn_open_main_browser_ru': 'Открыть основной браузер 🌐',
    'btn_close_browser_ru': 'Закрыть браузер ❌',
    'btn_open_new_tab_ru': 'Создать новую вкладку ➕',
    'btn_close_tab_ru': 'Закрыть вкладку ❌',
    'btn_open_incognito_ru': 'Режим инкогнито 🕵️',
    'btn_open_explorer_ru': 'Открыть Проводник 📂',
    'btn_create_folder_ru': 'Создать папку 📁',
    'btn_create_file_txt_ru': 'Создать файл .txt 📝',
    'btn_create_docx_file_ru': 'Создать файл .docx 📄',
    'btn_webcam_shot_ru': 'Снимок с вебки 📸',
    'btn_webcam_record_ru': 'Запись вебки 🎥',
    'btn_audio_record_ru': 'Запись звука 🎤',
    'btn_clipboard_text_ru': 'Буфер обмена 📋',
    'btn_active_window_screenshot_ru': 'Скриншот активного окна 🖼',
    'btn_secret_mode_ru': 'Секретный режим 🔒',
}


@dp.callback_query(lambda call: call.data == 'favourites_ru')
async def favourites_ru(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    favourites = user_favourites.get(user_id, [])
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=available_functions[func_key], callback_data=func_key)]
        for func_key in favourites
    ])
    markup.inline_keyboard.append([btn_back_ru])

    await call.message.delete()
    await call.message.answer("Избранные команды:", reply_markup=markup)


@dp.callback_query(lambda call: call.data == 'edit_favorites')
async def edit_favorites_handler(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    markup = generate_favourites_markup(user_id)
    await call.message.edit_text("<b>Выберите команды для добавления/удаления из избранного:</b>",
    reply_markup=markup, parse_mode="HTML")

def generate_favourites_markup(user_id):
    favourites = user_favourites.get(user_id, [])
    markup = InlineKeyboardMarkup(inline_keyboard=[])

    for func_key, func_name in available_functions.items():
        if func_key in favourites:
            markup.inline_keyboard.append(
                [InlineKeyboardButton(text=f"{func_name} ✅", callback_data=f'remove_{func_key}')]
            )
        else:
            markup.inline_keyboard.append(
                [InlineKeyboardButton(text=f"{func_name} ❌", callback_data=f'add_{func_key}')]
            )

    markup.inline_keyboard.append(
        [InlineKeyboardButton(text="Назад 🔙", callback_data='btn_back_ru')]
    )
    return markup

@dp.callback_query(lambda call: call.data.startswith('add_'))
async def add_to_favourites_handler(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    func_key = call.data.split('_', 1)[1]
    user_favourites.setdefault(user_id, []).append(func_key)
    save_favourites()
    await call.answer(f"Функция добавлена в избранное.")
    await edit_favorites_handler(call)

@dp.callback_query(lambda call: call.data.startswith('remove_'))
async def remove_from_favourites_handler(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    func_key = call.data.split('_', 1)[1]
    user_favourites[user_id].remove(func_key)
    save_favourites()
    await call.answer(f"Функция удалена из избранного.")
    await edit_favorites_handler(call)


@dp.callback_query(lambda call: call.data == 'personal_account_ru')
async def personal_account_ru(call: CallbackQuery):
    try:
        await call.message.delete()
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

    global do_not_disturb_enabled
    username = call.from_user.username or "Не указан"
    user_id = call.from_user.id

#    dnd_status = "вкл✅" if do_not_disturb_enabled else "выкл❌"

    text = f"""
👤 ЛИЧНЫЙ АККАУНТ — {username} :

🌍 Язык: 🇷🇺

🌐 Основной браузер: {browser}

📁 Основной диск: {disk_path}

🛠️ Версия: Pro v1.1

🆔 Ваш ID: {user_id}
    """

    message = await call.message.answer(text, reply_markup=create_personal_account_markup_ru(do_not_disturb_enabled))
    user_data[call.from_user.id] = {"message_id": message.message_id}


@dp.callback_query(lambda call: call.data == 'btn_enable_dnd_ru')
async def enable_dnd_ru(call: CallbackQuery):
    global do_not_disturb_enabled
    do_not_disturb_enabled = True

    await update_personal_account_message(call)


@dp.callback_query(lambda call: call.data == 'btn_disable_dnd_ru')
async def disable_dnd_ru(call: CallbackQuery):
    global do_not_disturb_enabled
    do_not_disturb_enabled = False

    await update_personal_account_message(call)


async def update_personal_account_message(call: CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username or "Не указан"
#    dnd_status = "вкл✅" if do_not_disturb_enabled else "выкл❌"

    text = f"""
👤 ЛИЧНЫЙ АККАУНТ — {username} :

🌍 Язык: 🇷🇺

🌐 Основной браузер: {browser}

📁 Основной диск: {disk_path}

🛠️ Версия: Pro v1.1

🆔 Ваш ID: {user_id}
    """

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(reply_markup=create_personal_account_markup_ru(do_not_disturb_enabled))
    await call.answer(f"Режим 'Не беспокоить' {'включен' if do_not_disturb_enabled else 'отключен'}")


async def update_personal_account_message_voise(call: CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username or "Не указан"
#    dnd_status = "вкл✅" if do_not_disturb_enabled else "выкл❌"

    text = f"""
👤 ЛИЧНЫЙ АККАУНТ — {username} :

🌍 Язык: 🇷🇺

🌐 Основной браузер: {browser}

📁 Основной диск: {disk_path}

🛠️ Версия: Pro v1.1

🆔 Ваш ID: {user_id}
    """

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(reply_markup=create_personal_account_markup_ru(do_not_disturb_enabled))


def get_all_drives():
    partitions = psutil.disk_partitions()
    drives = []

    for partition in partitions:
        drive = partition.device
        drives.append(drive)

    return drives

@dp.callback_query(lambda call: call.data.startswith('change_disk_'))
async def change_disk(call: CallbackQuery):
    new_disk = call.data.split('_')[2]

    global disk_path
    disk_path = new_disk

    save_disk_path(new_disk)
    await update_personal_account_message_disk(call)
    await call.answer(f"Диск изменён на {new_disk}")

@dp.callback_query(lambda call: call.data == 'change_disk')
async def change_disk_prompt(call: CallbackQuery):
    drives = get_all_drives()

    drive_buttons = [
        [InlineKeyboardButton(text=f"Перейти на {drive}", callback_data=f"change_disk_{drive}")]
        for drive in drives
    ]

    drive_buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_personal_account")])

    await call.message.edit_text("Выберите диск:", reply_markup=InlineKeyboardMarkup(inline_keyboard=drive_buttons))
    await call.answer()


@dp.callback_query(lambda call: call.data == 'back_to_personal_account')
async def back_to_personal_account(call: CallbackQuery):
    await personal_account_ru(call)
    await call.answer()


@dp.callback_query(lambda call: call.data.startswith('change_disk_'))
async def change_disk(call: CallbackQuery):
    new_disk = call.data.split('_')[2]

    global disk_path
    disk_path = new_disk

    await update_personal_account_message_disk(call)
    await call.answer(f"Диск изменен на {new_disk}")



async def update_personal_account_message_disk(call: CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username or "Не указан"
# dnd_status = "вкл✅" if do_not_disturb_enabled else "выкл❌"

    text = f"""
👤 ЛИЧНЫЙ АККАУНТ — {username} :

🌍 Язык: 🇷🇺

🌐 Основной браузер: {browser}

📁 Основной диск: {disk_path}

🛠️ Версия: Pro v1.1

🆔 Ваш ID: {user_id}
    """

    await call.message.edit_text(text)
    await call.message.edit_reply_markup(reply_markup=create_personal_account_markup_ru(do_not_disturb_enabled))


async def send_start_message(user_id: int):
    try:
        await bot.send_message(ADMIN_ID, f"🚀 <b>Бот запущен пользователем!</b>\nID пользователя: <code>{user_id}</code>", parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка отправки сообщения админу: {e}")

async def start_bot():
    print(f"smartPC Pro | Lexium\n")
    print(f"Бот был успешно запущен с ID: {authorized_user_id}")
    await bot.delete_webhook(drop_pending_updates=True)

    user_id = authorized_user_id
    await send_start_message(user_id)

    try:
        await bot.send_message(authorized_user_id, "<b>smartPC Pro | Lexium работает</b>🚀", parse_mode="HTML")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        import logging

        logging.basicConfig(level=logging.WARNING)
        logging.getLogger('aiogram').setLevel(logging.WARNING)

        asyncio.run(start_bot())
    except Exception as e:
        print(f"Ошибка запуска: {e}")
