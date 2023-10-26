Шаги требующиеся для запуска модели:

```sh
python -m venv venv
. venv/bin/activate
pip install rasa
rasa train
```

Требуется заполнить файл credentials.yml
Пример можно взять отсюда https://github.com/RasaHQ/rasa/blob/main/examples/moodbot/credentials.yml

В отдельном терминале
```sh
ngrok http 5005
```

В отдельном терминале
```sh
cd actions
rasa run actions
```

В отдельном терминале
```sh
bash start.sh
```
