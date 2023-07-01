import sys

from bot import bot, admin_bot
from settings import commands_bot, commands_bot_admin


def main():
    """Обработка manage.py команд."""
    try:
        command = sys.argv[1]
    except IndexError:
        print("Введите команду")
    else:
        if command in commands_bot:
            getattr(bot, command)()
        elif command in commands_bot_admin:
            getattr(admin_bot, command)()
        else:
            raise Exception("Введена некорретная команда")


if __name__ == "__main__":
    main()
