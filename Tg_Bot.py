import asyncio
from obswebsocket import obsws, requests as obs_requests
import flet as ft
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes
import logging
import os
import json

# ---------------Настройки проги
settings = {
    "TOKEN": "8303303957:AAEK7n-NLAub_SfiocEpArld-0p8TV4ZN9s",
    "OBS_HOST": "localhost",
    "OBS_PORT": 4455,
    "OBS_PASSWORD": "123456",
    "OBS_TEXT_SOURCE": "text_input",
}

name_file_settings = "settings.json"

def load_settings_json():
    if not os.path.exists(name_file_settings):
        with open(name_file_settings, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    if os.path.exists(name_file_settings):
        with open(name_file_settings, "r", encoding="utf-8") as f:
            data = json.load(f)
    return data

def save_settings_json(data):
    with open(name_file_settings, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

settings_for_file = load_settings_json()


TOKEN = settings_for_file["TOKEN"]
OBS_HOST = settings_for_file["OBS_HOST"]
OBS_PORT = settings_for_file["OBS_PORT"]
OBS_PASSWORD = settings_for_file["OBS_PASSWORD"]
OBS_TEXT_SOURCE = settings_for_file["OBS_TEXT_SOURCE"]
ws = None
obs_connected = False

logging.getLogger("websocket").setLevel(logging.CRITICAL)
logging.getLogger("obswebsocket").setLevel(logging.CRITICAL)
#----------------Настройки закончились


queue = asyncio.Queue()
print(TOKEN, OBS_HOST, OBS_PORT, OBS_PASSWORD, OBS_TEXT_SOURCE)

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    messages = [msg.strip() for msg in text.split("⭕️") if msg.strip()]

    # сохраняем chat_id и показываем кнопку при первом сообщении
    if "chat_id" not in context.bot_data:
        context.bot_data["chat_id"] = update.message.chat.id

        keyboard = [[KeyboardButton("/clean")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await context.bot.send_message(
            chat_id=context.bot_data["chat_id"],
            text="Бот в сети",
            reply_markup=reply_markup
        )

    # кладём сообщения в очередь
    for msg in messages:
        await queue.put(msg)

async def Clean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await queue.put("__CLEAR__")
    await update.message.reply_text("Все сообщения очищены")

# -------------------- запуск бота --------------------

async def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND, log))

    app.add_handler(CommandHandler("Clean", Clean))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # text = '⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!⭕️ Татьяна Тимакова, Здравствуйте, помолитесь, пожалуйста, за меня. Новая работа, нужна память и силы, а их нет. И ничего не хочется делать⭕️ Надежда просит: пожалуйста помолитесь, за сына Максима, пропал без вести 1 год 8 месяцев назад. Знаю, что он жив - чтобы он был с Господом. Завтра снова еду в госпиталь, ухаживать за ранеными. Чтобы Бог усмотрел мой путь.⭕️ Даша пишет: помолитесь пожалуйста за меня, за духовный рост и избавление от вредных привычек.⭕️ Гуля пишет: благодарю Бога за вас и программу «Помолитесь за меня»!!! Будьте благословенны!!! Прошу ваших молитв за сына Александра, чтобы он посвятил Богу свою жизнь, и прошу за мужа Михаила!!!'
    # await log(text, None)


def flet_main(page: ft.Page):
    page.title = "Молитвенные просьбы"
    page.window.width = 1600
    page.window.height = 900
    asyncio.create_task(page.window.center())
    page.theme_mode = ft.ThemeMode.DARK

    def open_settings(e):
        settings_dialog.open = True
        page.update()

    def close_settings(e):
        settings_dialog.open = False
        page.update()

    def open_add_message(e):
        add_messages.open = True
        page.update()

    def close_add_messages(e):
        add_messages.open = False
        page.update()

    add_messages = ft.AlertDialog(
        title=ft.Text("Добавить сообщение"),
        modal=True,
        content=ft.Container(
            width=600,
            height=500,
            padding=20,
        )
    )
    settings_dialog = ft.AlertDialog(
        title=ft.Text("Настройки"),
        modal=True,
        content=ft.Container(
            width=600,
            height=350,
            padding=20
        )
    )

    def settings_field():
        TEXT_TOKEN = ft.Text("Токен из тг")
        TOKEN_field = ft.TextField(value=settings_for_file["TOKEN"],  width=600)
        TEXT_OBS_TEXT_SOURCE = ft.Text("Имя поля в OBS")
        OBS_TEXT_SOURCE_field = ft.TextField(value=settings_for_file["OBS_TEXT_SOURCE"], width=600)
        TEXT_OBS_PORT = ft.Text("OBS порт")
        OBS_PORT_field = ft.TextField(value=settings_for_file["OBS_PORT"], width=600)
        TEXT_OBS_PASSWORD = ft.Text("Пароль от OBS")
        OBS_PASSWORD_field = ft.TextField(value=settings_for_file["OBS_PASSWORD"], width=600)

        settings_dialog.content.content = ft.Column(
            expand=True,
            spacing=5,
            controls=[
                TEXT_TOKEN,
                TOKEN_field,
                TEXT_OBS_TEXT_SOURCE,
                OBS_TEXT_SOURCE_field,
                TEXT_OBS_PORT,
                OBS_PORT_field,
                TEXT_OBS_PASSWORD,
                OBS_PASSWORD_field
        ])

        def save_settings_on(e):
            updates = {
                "TOKEN": TOKEN_field.value,
                "OBS_TEXT_SOURCE": OBS_TEXT_SOURCE_field.value,
                "OBS_PORT": OBS_PORT_field.value,
                "OBS_PASSWORD": OBS_PASSWORD_field.value
            }
            settings_for_file.update(updates)
            save_settings_json(settings_for_file)
            page.update()

            settings_dialog.open = False
            page.update()


        settings_dialog.actions = [
            ft.Button("Сохранить", on_click=save_settings_on),
            ft.Button("Закрыть", on_click=close_settings)
        ]

    def def_add_message():
        TEXT_INPUT = ft.Text("Вставьте молитвенные просьбы")
        INPUT_FLUED = ft.TextField(width=600, height=350, multiline=True, min_lines=10, max_lines=10)
        SEND_BUTTON = ft.Button(
            "Отправить",
            on_click=lambda e: send_to_queue(e, INPUT_FLUED)
        )
        CLOES_BUTTON = ft.Button(
            "Закрыть",
            on_click= close_add_messages
        )

        add_messages.content.content = ft.Column(
            expand=True,
            spacing=5,
            controls=[
                TEXT_INPUT,
                INPUT_FLUED
            ]
        )
        add_messages.actions = [
            SEND_BUTTON,
            CLOES_BUTTON
        ]


    def send_to_queue(e, text_field):
        text = text_field.value

        messages = [msg.strip() for msg in text.split("⭕️") if msg.strip()]

        for msg in messages:
            print(f"Добавлено: {msg[:50]}")


        text_field.value = ""
        text_field.update()

        page.update()

        async def add_to_queue():
            for msg in messages:
                await queue.put(msg)

        # Запускаем асинхронную задачу
        asyncio.create_task(add_to_queue())

        add_messages.open = False
        page.update()




    def_add_message()
    settings_field()

    page.overlay.append(settings_dialog)
    page.overlay.append(add_messages)

    page.appbar = ft.AppBar(
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                tooltip="Настройки",
                on_click=open_settings,
            ),
            ft.IconButton(
                icon=ft.Icons.ADD,
                tooltip="Добавить",
                on_click=open_add_message,
            )
        ]
    )

    chat = ft.Row(expand=True, spacing=10, wrap=True, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)

    delete_all_button = ft.Button(content="Удалить всё")

    def delete_all_messages(e):
        asyncio.create_task(queue.put("__CLEAR__"))

    delete_all_button.on_click = delete_all_messages

    def connect_obs():
        global ws, obs_connected
        try:
            if ws:
                try:
                    ws.disconnect()
                except:
                    pass

            ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
            ws.connect()
            obs_connected = True
            update_obs_status()
            return True

        except Exception as e:
            obs_connected = False
            update_obs_status()
            return False

    def reconnect_obs(e=None):
        page.snack_bar = ft.SnackBar(
            ft.Text("Попытка переподключения к OBS...")
        )
        page.snack_bar.open = True
        page.update()
        if connect_obs():
            page.snack_bar = ft.SnackBar(
                ft.Text("Успешно подключено к OBS")
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("OBS недоступен")
            )
        page.snack_bar.open = True
        page.update()

    def update_obs_status():
        if obs_connected:
            status_dot.bgcolor = "green"
            status_text.value = "OBS: подключён"
            status_text.color = "green"
        else:
            status_dot.bgcolor = "red"
            status_text.value = "OBS: отключён"
            status_text.color = "red"

        page.update()

    async def obs_connection_watcher():
        global obs_connected, ws
        while True:
            await asyncio.sleep(0.5)
            if not ws:
                continue
            try:
                # websocket-client флаг
                connected = ws.ws.connected
            except Exception:
                connected = False
            if obs_connected and not connected:
                obs_connected = False
                update_obs_status()
                page.snack_bar = ft.SnackBar(
                    ft.Text("Connection lost! OBS отключился")
                )
                page.snack_bar.open = True
                page.update()

    async def blink_obs_status():
        while True:
            if not obs_connected:
                status_dot.visible = not status_dot.visible
                page.update()
            else:
                status_dot.visible = True
            await asyncio.sleep(0.6)

    reconnect_button = ft.Button(
        content="Переподключиться к OBS",
        on_click=reconnect_obs
    )
    status_dot = ft.Container(
        width=16,
        height=16,
        border_radius=8,
        bgcolor="red"
    )

    status_text = ft.Text(
        value="OBS: отключён",
        color="red",
        size=14
    )

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.alignment.Alignment.CENTER,
            content=chat
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                delete_all_button,
                reconnect_button,
                status_dot,
                status_text
            ]
        )
    )

    async def updater():
        while True:
            msg = await queue.get()

            if msg == "__CLEAR__":
                chat.controls.clear()
                page.update()
                continue

            # Обработка клавиш Ctrl+Shift+F1…F12
            def on_keyboard(e: ft.KeyboardEvent):
                if e.key.startswith("F"):
                    try:
                        # Получаем номер F-клавиши (например, F1 → 1, F12 → 12)
                        f_number = int(e.key[1:])
                        index = f_number - 1  # переводим в индекс списка (0-based)

                        # Проверяем, что сообщение с таким индексом существует
                        if 0 <= index < len(chat.controls):
                            msg_container = chat.controls[index]

                            # Создаем "фейковое" событие для input_file
                            class DummyEvent:
                                def __init__(self, control):
                                    self.control = control

                            dummy_event = DummyEvent(msg_container)
                            input_file(dummy_event)  # вызываем обработку
                            update_numbers()  # обновляем номера
                        else:
                            print(f"Сообщение с индексом {index} не существует.")
                    except ValueError:
                        pass  # если e.key не число после F — игнорируем

            # Привязываем обработчик
            page.on_keyboard_event = on_keyboard



            def input_file(e):
                global ws, obs_connected

                message_container = e.control
                while not isinstance(message_container, ft.Container):
                    message_container = message_container.parent

                text_container = message_container.content.controls[0]
                content = text_container.controls[1]
                text_to_save = content.value

                for msg in chat.controls:
                    msg.bgcolor = "#607D8B"
                message_container.bgcolor = "#FF0000"
                page.update()

                if not obs_connected:
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Нет соединения с OBS. Нажмите «Переподключиться»")
                    )
                    page.snack_bar.open = True
                    page.update()
                    return

                try:
                    ws.call(
                        obs_requests.SetInputSettings(
                            inputName=OBS_TEXT_SOURCE,
                            inputSettings={"text": text_to_save},
                            overlay=True
                        )
                    )


                except Exception:
                    obs_connected = False
                    update_obs_status()
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Соединение с OBS потеряно")

                    )
                    page.snack_bar.open = True
                    page.update()

            # Функция для обновления порядковых номеров
            def update_numbers():
                for idx, msg_container in enumerate(chat.controls, start=1):
                    text_column = msg_container.content.controls[0]
                    number_text = text_column.controls[0]
                    number_text.value = str(idx)
                page.update()

            # Функция удаления сообщения
            def delete_message(e):
                message_container = e.control.parent.parent.parent
                if message_container in chat.controls:
                    chat.controls.remove(message_container)
                    update_numbers()  # пересчитываем номера
                    page.update()

            def toggle_edit(e):
                button = e.control

                message_container = button
                while not isinstance(message_container, ft.Container):
                    message_container = message_container.parent

                column = message_container.content.controls[0]
                text_container = column.controls[1]

                if not hasattr(button, "editing") or not button.editing:
                    button.editing = True
                    text = text_container.value

                    edit_field = ft.TextField(
                        value=text,
                        autofocus=True,
                        multiline=True,
                        expand=True
                    )
                    column.controls[1] = edit_field
                    button.content = "Сохранить"
                    print("1")

                else:
                    button.editing = False

                    field = text_container

                    column.controls[1] = ft.Text(
                        field.value,
                        text_align=ft.TextAlign.CENTER,
                        selectable=True
                    )

                    button.content = "Ред"
                    print("2")
                page.update()


            message_container = ft.Container(
                bgcolor="#607D8B",
                border_radius=10,
                padding=10,
                width=370,
                height=330,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    f"{len(chat.controls) + 1}",
                                    size=23,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    msg,
                                    size= 17,
                                    text_align=ft.TextAlign.CENTER,
                                    selectable=True
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Button(
                                    content="В эфир",
                                    on_click= input_file,
                                    bgcolor="green",
                                ),
                                ft.Button(
                                    content="Удалить",
                                    on_click=delete_message
                                ),
                                ft.Button(content="Ред", on_click=toggle_edit)
                            ]
                        )
                    ]
                )
            )

            chat.controls.append(message_container)
            page.update()

    connect_obs()
    asyncio.create_task(blink_obs_status())
    asyncio.create_task(obs_connection_watcher())
    asyncio.create_task(start_bot())
    asyncio.create_task(updater())

ft.run(flet_main)
