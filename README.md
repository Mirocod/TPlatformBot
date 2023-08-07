## TPlatformBot

### Видеоинструкции

Обзор проекта и кода - https://vk.com/video-210998646_456239040

Общий обзор возможностей - https://vk.com/video-210998646_456239041

Обзор возможностей пользователя - https://vk.com/video-210998646_456239042

### Модульный Telegram-бот с возможностью редактирования прав доступа, как пользователям, так и группам пользователей

Список модулей

1. Стартовая страница
2. Резервное копирование
3. Профиль пользователя
4. Права доступа
5. Пользователи и группы пользователей
6. Проекты
7. Задачи
8. Потребности
9. Комментарии
10. Языки (сообщения и кнопки)
11. Заказы
12. Подписки

---

Данный бот позволяет создать свою площадку для взаимодействия на некоммерческой основе в мессенджере Telegram и обмениваться ресурсами и компетенциями для реализации различных проектов.

Сам бот разработан на языке программирования **Python** с использованием фреймворка **Aiogram**. База данных - **SQLite3**.

---

**Установка, первичная настройка и запуск**

> Для работы требуется, как минимум, Python 3.8.

*** Загрузка зависимостей ***

> AltLinux

`sudo apt-get install python3-module-pip`

`sudo apt-get install python3-modules-sqlite3`

`python3 -m pip install -r requirements.txt`

*** Запуск ***

`python3 main.py` - AltLinux

*** Конфигурирование ***

Создайте два файла рядом с `main.py`

`config_root_ids`

`config_telegram_bot_api_token`

Запишите в первый Telegram ID пользователей, которым будет предоставлен полный (root) доступ.
Во втором файле должен быть записан api_token бота, который создаётся при помощи @BotFather.

## Тестовая версия

Тестовая версия запущена по ссылке
http://t.me/Test_TPlatform_bot


## Запуск админ панели

1. Необходимо установить пакет Django
   pip install requirements.txt
2. Добавляем информацию в базу данных
   python manage.py makemigrations
   python manage.py migrate
3. Создаем суперпользователя, чтобы зайти в админку
   python manage.py createsuperuser
   Придумываем логин, почту и пароль
4. Запускаем приложение
   python manage.py runserver
5. Переходим по ссылке http://127.0.0.1:8000/admin/ и вводим логин, пароль
