# VPN_bot


Description: VPN bot for Talestorm


Used technologies:
-
    - python 3.11.3
    - python-dotenv 1.0.0
    - sqlalchemy 2.0.17
    - aiogram 2.25.1
    - alembic 1.11.1
    - psycopg2-binary 2.9.6


# First launch instructions:

## enviroment:
Create .env file backend/.env and fill it with required keys:
- BOT_TOKEN=...
- ADMIN_BOT_TOKEN=...
- PAYMENTS_TOKEN=...
- DB_ENGINE=...
- DB_NAME=...
- POSTGRES_USER=...
- POSTGRES_PASSWORD=...
- DB_HOST=db
- DB_PORT=5432
- ADMIN_ID_1=...

## db url
Go to db/, open alembic.ini file and change sqlalchemy.url:

sqlalchemy.url = postgresql://**user**:**password**@**DB_HOST**:**DB_PORT**/**DB_NAME**

## postgres user
go to infra/ and set your actual POSTGRES_USER (look at braces {}).

Build and launch containers:
#### docker-compose up -d --build

After that the application is ready to use.