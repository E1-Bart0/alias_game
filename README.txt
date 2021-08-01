Сайт для многопользовательской игры в Алиас (Возможно, запущен http://172.104.139.91/)

Created on Python 3.9
Создадим venv, установим библиотеки и активируем venv:

Windows в cmd:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Alias/manage.py runserver

Linux:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Alias/manage.py runserver

В браузере переходим на http://127.0.0.1:8000

env.
prod:
APP_HOST=0.0.0.0
APP_PORT=80
DATABASE_HOST=alias_db
docker:
APP_HOST=0.0.0.0
APP_PORT=8000
DATABASE_HOST=alias_db
local:
APP_HOST=127.0.0.1
APP_PORT=8000
DATABASE_HOST=127.0.0.
