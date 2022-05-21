# Foodgram-project-react

## **Описание**
Проект Foodgram позволяет пользователям делиться любимыми рецептами и просматривать рецепты других пользователей. После добавления рецептов в корзину покупок доступна удобная опция - можно скачать список всех необходимых ингредиентов для приготовления с нужным количеством. 

**Технологи:**
* Python
* Django REST Framework
* Docker
* React

![Yamdb_final workflow](https://github.com/Anastasia-prog-create/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)

### О проекте:

Клонировать репозитозиторий можно командами ниже:
```sh
git clone https://github.com/Anastasia-prog-create/foodgram-project-react.git
cd foodgram-project-react
```
Для работы с проектом в директории infra/ cоздайте и заполните файл .env необходимыми переменными.
Пример наполнения файла .env:
```
SECRET_KEY = 'your_secret_key'

DB_ENGINE=django.db.backends.postgresql
DB_NAME=db_name
POSTGRES_USER=login
POSTGRES_PASSWORD=password
DB_HOST=container_name
DB_PORT=port_number
```
### URLS проекта:
Все запросы к API начинаются с /api/, доступные адреса:
* http://84.252.143.61/api/users/
* http://84.252.143.61/api/tags/
* http://84.252.143.61/api/recipes/
* http://84.252.143.61/api/ingredients/

### Автор проекта:
Кривошеева Анастасия - студент 6 когорты pythonplus Яндекс Практикума.
