import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import User
from project import settings
from project.asgi import application
from project.mixins.admins import ImageAdminMixin


def test_asgi_application(client):
    # Создание клиента для выполнения HTTP запросов

    # Выполнение ASGI приложения
    response = client.get('/')

    # Проверка, что ASGI приложение существует и доступно
    assert application is not None

    # Проверка, что ответ получен успешно
    assert response.status_code == 200


from project.wsgi import application


def test_wsgi_application(client):
    # Создание клиента для выполнения HTTP запросов

    # Выполнение ASGI приложения
    response = client.get('/')

    # Проверка, что ASGI приложение существует и доступно
    assert application is not None

    # Проверка, что ответ получен успешно
    assert response.status_code == 200


def test_main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    from manage import main

    try:
        main()
    except SystemExit as e:
        assert e.code == 1
    except Exception as e:
        pytest.fail(f"main() raised an exception: {e}")