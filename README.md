# Тестовое задание

[Оригинальный текст задания тут](https://docs.google.com/document/d/1otqyCQ2N1Pn3i8L1LgSHBJvhjdvjXsVWChQzLiS-l68/edit)

Напишите код приложения для Django (Python 3), в котором у пользователей 
(пользователей в системе может быть очень много) есть помимо основных полей 2 дополнительных: 
ИНН (уникально, ИНН может начинаться с нуля) и счет (в рублях, с точностью до копеек). 

Также есть форма состоящая из полей (в приоритете  использование REST API или же чистый Django):
Выпадающий список со всеми пользователями в системе, со счета которого нужно перевести деньги

+ Поле для ввода одного или нескольких ИНН пользователей, на счета которых будут переведены деньги
+ Поле для указания какую сумму нужно перевести с одного счета на другие
+ Необходимо проверять есть ли достаточная сумма у пользователя, со счета которого списываются средства, 
и есть ли пользователи с указанным ИНН в БД. При валидности введенных данных необходимо указанную сумму 
списать со счета указанного пользователя и перевести на счета пользователей с указанным ИНН в 
равных частях (если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет).


> Обязательно наличие unit-тестов.
> Требуется реализовать только бэк. Фронт и шаблоны можно не настраивать.
> Код в приватном репозитории. 

# Вопросы

+ Разрешен перевод денег только от авторизованного пользователя 
или даем ему выбрать от какого пользователя делаем перевод?

+ Если переводим 0.98р на 3-х пользователей, сообщаем, что не можем перевести, или переводим 0.96р,
а 2 лишние копейки не переводим?

+ Запрет на создание пользователя без ИНН, так как он должен быть уникальным?

+ Использовать ручное управление транзакциями вместо ATOMIC_REQUESTS = True при переводе?

# Решение

ATOMIC_REQUESTS = True

    позволяет не беспокоится о транзакциях БД
    
100% покрытие кода тестами
    
    дает возможность вовремя увидеть что, что-то сломалось
    
Создано приложение proccessing

    в ней модель Transaction для регистрации всех операций с банковскими счетами пользователя.
    Любой банк и любой пользователь всегда хочет видеть историю операций, это помогает найти проблемы
    и быстро их порешать.
    Если все операции как поступления денег списание и переводы регистрировать в этой таблице,
    то мы получаем движения и остатки по счетам, но так как разрабатываем приложения для 
    highload, то проводим денормализацию БД и в пользователях добавляем поле balance - где будет
    храниться конечный остаток по счету, хотя в таблице транзакций это всё можно получить.
    
AUTH_USER_MODEL = 'extension_user.ExtensionUser'

    Позволяет нам использовать нативного пользователя и расширять на наше усмотрение. Очень полезно.

ИНН пользователя

    Так как поле уникально, и оно имеет все планы стать естественным первичным ключем и так как по
    нему часто делается поиск, проводим следующие операции 
    + unique=True     - делает поле уникальным
    + db_index=True   - создаем иднекс для этого поля
    + validators=[validate_inn]  - прописываем валидаторы причем делаем проверку при сохранении
      это дает полный контроль
    + blank=False, null=False  - избавляет нас от проблем с неверными значениями
    + так как ИНН - может содержать нули, то удобнее хранить данные в виде строки, хотя можно
      хранить и в виде числа, и потом при выводе добавлять нули, но так как мы используем индексацию
      и валидацию, вполне можно использовать в качестве типа поля строку.
    + ИНН в модели пользователя может быть естественным ключом, но для будущих GenericRelation 
      оставил ещё и сурогатный ключ ID

Уровень изоляции БД выбипаем в зависимости от использования БД
    
    + необходимо помнить об уровне изоляции БД и выбрать в зависимости от задачи, 
      более высоки уровень требует больше ресурсов
    + возможно лучше установить возможно лучший вариант 'SERIALIZABLE'
    + ['READ-UNCOMMITTED', 'READ-COMMITTED', 'REPEATABLE-READ', 'SERIALIZABLE']

# TODO:
+ ~~создать виртуально окружение для проекта~~
+ ~~прописать .gitignore~~
+ ~~создать проект djagno~~
+ ~~создать requirements.txt с django, djangorestframework~~
+ ~~сделать первоначальную настройку проекта~~
+ ~~вынести все секретные и важные данные в отдельный файл, который не будет комититься~~
+ ~~сделать коммит~~
+ ~~создать расширенную модель с пользователей~~
+ ~~не забыть в настройках прописать расширенную модель пользователя AUTH_USER_MODEL~~
+ ~~создаем миграции и мигрируем~~
+ ~~создать приложение с транзакциями~~
+ ~~установить DRF~~
+ ~~сделать сериализаторы DRF~~
+ ~~сделать viewsets DRF~~
+ ~~сделать вариант с DRF~~
+ ~~только залогиненые пользователи могут работать с DRF~~
+ сделать тесты DRF
+ сменить тип репозитория на приватный
+ перепроверить все ли важные данные за пределами репозитория, изменить пароли и 
  сделать деплой на сервер


### Примечание 

Для денег использую только Decimal чтобы не потерять точность значения

---

# Установка

Клонируем этот репозиторий

```git
git clone https://github.com/programishka/review_code.git
```

Создан специальный Makefile чтобы сделать установку максимально простой.
*Установим вируальное окружение*

```shell script
make setupvenv
```

Теперь необходимо активировать виртуальное окружение

```shell script
make bootstrap
```

Для запуска в режиме разработчика используем команду

```shell script
make start
```

### P.S.

для более удобного деплоя можно использовать команду

```shell script
make deploy
```
