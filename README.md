# Выбор победителя конкурса для Instagram

Скрипт ```main.py``` выбирает одного рандомного победителя конкурса в Instagram который выполнил 3 условия:
1. Отметил в комментарии реального пользователя Instagram;
2. Лайкнул пост с розыгрышем;
3. Подписался на аккаунт.

### Как установить

У вас уже должен быть установлен Python 3. Если его нет, то установите.
Так же нужно установить необходимые пакеты:
```
pip3 install -r requirements.txt
```

### Как пользоваться скриптом

Для работы скрипта нужно создать файл ```.env``` с переменными INSTAGRAM_LOGIN (логин от Instagram) и ISTAGRAM_PASSWORD (пароль от Instagram) 
в директории где лежит скрипт. Вставьте ваш логин/пароль в файл ```.env```:
```
ISTAGRAM_PASSWORD = 'python3'
INSTAGRAM_LOGIN = 'BestLanguage'
```

### Запуск скрипта
Для запуска скрипта вам необходимо запустить командную строку и ввести команду:
```
>>> python3 main.py https://www.instagram.com/p/ссылкаНаПостСрозыгрышем/ аккаунтНаКоторыйДолжныПодписаться 
```

### Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
