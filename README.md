# Mailing Management Service

## Overview
This project aims to develop a mailing management service that allows users to create, administer, and analyze the effectiveness of email campaigns. The service focuses on maintaining current clients through engaging newsletters and informational blasts.

## Features
- **CRUD Operations**: Manage mailing lists with create, read, update, and delete functionalities for both mailings and clients.
- **Scheduling**: Implement scheduled email dispatches using Django APScheduler, allowing for automatic sending based on specified time frames.
- **Client Management**: Maintain client data (email, full name, comments) and associate them with specific mailings.
- **Mailing Settings**: Configure mailing details, including first send date, frequency (daily, weekly, monthly), and mailing status (created, completed).
- **Message Management**: Create and manage email messages that are part of the mailings.

## Technology Stack
- **Django**: The web framework used for backend development.
- **Materialize CSS**: A responsive front-end framework for styling the application.
- **Django APScheduler**: A library for managing scheduled tasks and periodic jobs.
- **Redis**: Used for caching to enhance performance and speed up data retrieval.
- **PostgreSQL**:The database management system used for storing application data.


## Installation and Setup

### 1. Clone the Repository

```bash
git clone git@github.com/Weta12311/MailScheduler.git
cd MailScheduler
```
### 2. Copy the env.example file to .env:

Open.env and replace the values of the variables with your own

```bash
cp .env.example .env
```

### 3. Install Dependencies
The project uses Poetry for dependency management. Ensure Poetry is installed, then run the following command to install all dependencies:
```bash
poetry shell
poetry install
```
### 4. Start Migrations
To start migrations, use the following command:
```bash
python3 manage.py migrate
```

### 5. Create Superuser
Enter the command in the terminal:
```bash
python3 manage.py create_superuser
```

### 6. Load Fixture
Loading test fixtures for the database:
```bash
python3 manage.py loaddata data.json
```

### 7. Create Group
Loading test fixtures for the database:
```bash
python3 manage.py create_groupe
```


### 8. Create Manager and Content-Manager
Enter the command in the terminal:
```bash
python3 manage.py create_staff
```


### 9. Run Server
To run server, use the following command:
```bash
python3 manage.py runserver
```
The server will be available at http://127.0.0.1:8000

## Дополнительная информация для проверяющего
1. Пункт 5 (Create Superuser) создаст суперпользователя
    * email: admin@test.com
    * password: 12345678
2. Пункт 6 (Load Fixture) выполнит загрузку в БД:
   * 5 статей для блога
   * 3 клиентов (владелец superuser)
   * 3 сообщений для рассылки (владелец superuser)
   * 3 рассылки (владелец superuser)
3. Пункт 7 (Create Group) создаст:
   * regular_user - новые зарегестрированные пользователи платформы, имеют доступ только к своим созданным клиентам, сообщениям, рассылкам
   * manager - пользователи имеют только ограниченный доступ к странице рассылки (просмотр списка, детальный просмотр, деактивация), пользователей (просмотр списка, деактивация)
   * content-manager - пользователи имеют доступ только к административной панели модели статей
   * superuser имеет доступ и права ко всей информации приложения
   * К страницам Главная, Блог, имеют доступ все неавторизованные пользователи

4. Пункт 8 (Create Manager and Content-Manager) создаст пользователей, добавит в соответствующие группы (manager, content_manager)
    * email: manager@test.com
    * email: content_manager@test.com
    * password: 12345678
5. Отправка запланированной рассылки осуществляется через интерфейс сайта
6. Мгновенная отправка осуществляется командой
    ```bash
    python3 manage.py send_mail
    ```
   При выполнении команды следуйте инструкции выбора рассылки. При выполнении мгновенной рассылки попытка рассылки сохранется в БД, время следующей отправки не изменяется


