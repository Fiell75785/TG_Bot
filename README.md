# 🙏 TG_Bot — Prayer Requests Bot for OBS Studio

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Flet](https://img.shields.io/badge/Flet-GUI-orange.svg)](https://flet.dev)
[![OBS Studio](https://img.shields.io/badge/OBS-WebSocket-purple.svg)](https://obsproject.com)

> Telegram-бот для сбора молитвенных просьб с интеграцией в OBS Studio.
> Оператор управляет просьбами через элегантный графический интерфейс на Flet.

---

## ✨ Возможности

| Компонент | Функционал |
|-----------|------------|
| 🤖 **Telegram-бот** | • Принимает молитвенные просьбы от пользователей<br>• Автоматически разбивает сообщения по разделителю `⭕️` |
| 🖥️ **Графический интерфейс (Flet)** | • Просмотр всех просьб в виде карточек<br>• Отправка в эфир (меняет текст в OBS)<br>• Редактирование текста просьбы<br>• Удаление отдельных просьб / очистка всех<br>• Ручное добавление просьб<br>• Настройка подключения к OBS и токена бота<br>• Автономный режим |
| 🎬 **Интеграция с OBS Studio** | • WebSocket-соединение<br>• Отправка текста в текстовый источник сцены |
| ⌨️ **Горячие клавиши** | • `Ctrl+Shift+F1…F12` — мгновенная отправка заготовленных сообщений в эфир |
| 🔄 **Авто-переподключение** | • Умный индикатор статуса OBS<br>• Кнопка ручного переподключения |

---

## 📋 Требования

- **Python** — версия **3.12** (обязательно)
- **OBS Studio** с установленным плагином `obs-websocket`

---

## 🚀 Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Fiell75785/TG_Bot.git
cd TG_Bot
pip install -r install.txt
python Tg_Bot.py
