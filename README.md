# Dating application (Django Rest Framework)

###### Адрес хоста: https://dating-apptrix.herokuapp.com
###### Токен авторизации передавать в Header HTTP-запроса: `Authorization:` `Token 4c71b30da6c3ddbb360b17ffd40c43ec9f621bac`

## Список эндпоинтов:

____

### 1. Регистрация пользователя:
**Эндпоинт:** https://dating-apptrix.herokuapp.com/api/client/create/ <br>

**Дополнительная информация:** при регистрациии пользователя на его аватарку накладывается водный знак. Если изображение от пользователя не загружено - используется картинка для аватарки по умолчанию

**Токен авторизации:** Не требуется <br>

**Данные передаются в:** формате form-data <br>

**Метод:** `POST` <br>

**Пример входных параметров:**
* `email:` `email@email.com`
* `password:` `1234`
* `first_name:` `Name`
* `last_name:` `Surname`
* `is_male:` `False`
* `avatar` *(прикрепить изображение PNG или JPEG)* <br>

**Пример ответа:**
```JSON
{
    "client": {
        "id": 2,
        "email": "2@1.com",
        "is_male": false,
        "first_name": "First Name 1",
        "last_name": "Last Name 1",
        "avatar": "/media/photos/2022/03/17/avatarJPEG.jpg"
    }
}
```

**Пример выполненного запроса в Postman:**<br>
![client/create/](https://i.imgur.com/qe9INkJ.png "client/create/")

____

### 2. Авторизация:
**Эндпоинт:** https://dating-apptrix.herokuapp.com/login/ <br>

**Токен авторизации:** Не требуется <br>

**Данные передаются в:** формате JSON <br>

**Метод:** `POST` <br>

**Пример входных параметров:**
```JSON
{
    "username": "email@email.com",
    "password": "1234"
} 
```
<br>

**Пример ответа:**
```JSON
{
    "token": "4c71b30da6c3ddbb360b17ffd40c43ec9f621bac"
}
```

**Пример выполненного запроса в Postman:**<br>
![login/](https://i.imgur.com/CwvtsQt.png "login/")

____

### 3. Деавторизация:
**Эндпоинт:** https://dating-apptrix.herokuapp.com/logout/ <br>

**Токен авторизации:** Требуется <br>

**Данные передаются в:** Header HTTP-запроса <br>

**Метод:** `GET` <br>

**Пример входных параметров (в Header HTTP-запроса):**
`Authorization:` `Token 4c71b30da6c3ddbb360b17ffd40c43ec9f621bac`
<br>

**Пример ответа:**
HTTP-status = 200 OK

**Пример выполненного запроса в Postman:**<br>
![logout/](https://i.imgur.com/rCLup56.png "logout/")

____

### 4. Получение списка всех Клиентов (с фильтрацией):
**Эндпоинт:** https://dating-apptrix.herokuapp.com/api/list <br>

**Токен авторизации:** Требуется <br>

**Данные передаются в:** параметрах URL <br>

**Метод:** `GET` <br>

**Примеры URL с фильтрами:** <br>
`https://dating-apptrix.herokuapp.com/api/list?is_male=false` <br>
`https://dating-apptrix.herokuapp.com/api/list/?first_name=Name&is_male=false` <br>
`https://dating-apptrix.herokuapp.com/api/list?first_name=Name&last_name=Surname&is_male=false`
<br>

**Пример ответа:**
```JSON
{
    "clients": [
        {
            "id": 1,
            "email": "1@1.com",
            "is_male": false,
            "first_name": "First Name 1",
            "last_name": "Last Name 1",
            "avatar": "/media/photos/2022/03/17/avatarJPEG.jpg"
        },
        {
            "id": 2,
            "email": "2@1.com",
            "is_male": false,
            "first_name": "First Name 1",
            "last_name": "Last Name 1",
            "avatar": "/media/photos/2022/03/17/avatarJPEG.jpg"
        }
    ]
}
```

**Пример выполненного запроса в Postman:**<br>
![list/](https://i.imgur.com/9UauT8b.png "list/")

____

### 5. Получение одного Клиента по ID:
**Эндпоинт:** https://dating-apptrix.herokuapp.com/api/client/1/ <br>

**Токен авторизации:** Требуется <br>

**Данные передаются в:** URL <br>

**Метод:** `GET` <br>

**Примеры URL:** <br>
`https://dating-apptrix.herokuapp.com/api/client/1/` <br>
`https://dating-apptrix.herokuapp.com/api/client/2/`

**Пример ответа:**
```JSON
{
    "client": {
        "id": 1,
        "email": "1@1.com",
        "is_male": false,
        "first_name": "First Name 1",
        "last_name": "Last Name 1",
        "avatar": "/media/photos/2022/03/17/avatarJPEG.jpg"
    }
}
```

**Пример выполненного запроса в Postman:**<br>
![retrieve](https://i.imgur.com/aBGl137.png "retrieve")

____

### 6. Симпатия к другому пользователю (match):
**Эндпоинт:** https://dating-apptrix.herokuapp.com/api/client/2/match/ <br>

**Дополнительная информация:** Авторизованный пользователь, отправляя этот запрос оказывает симпатию пользователю, ID которого указан в URL. Если эта симпатия взаимная, то есть в Базе Данных уже существует взаимная симпатия от другого пользователя, то им на почту отправляется уведомительное письмо, а пользователю в ответ на HTTP-запрос приходит почта понравившегося клиента. Если эта симпатия не взаимная, то в ответ на HTTP-запрос приходит сущность `match` с идентификаторами субъекта и объекта симпатии.

**Токен авторизации:** Требуется <br>

**Данные передаются в:** URL <br>

**Метод:** `POST` <br>

**Пример URL:** <br>
`https://dating-apptrix.herokuapp.com/api/client/1/match/`

**Пример ответа, если симпатия не взаимная:**
```JSON
{
    "match": {
        "id": 2,
        "subject_id": 1,
        "object_id": 2
    }
}
```
**Пример ответа, если симпатия взаимная:**
```JSON
{
    "match": "1@1.com"
}
```

**Пример выполненного запроса в Postman:**<br>
![1/match/](https://i.imgur.com/GY2R7YA.png "1/match/")
