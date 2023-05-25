from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.urls import reverse, resolve

from accounts.forms import UserUpdateForm

User = get_user_model()


def test_login(client, faker):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())
    data['username'] = faker.email()
    data['password'] = faker.word()

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == [
        'Please enter a correct email address and password. Note that both fields may be case-sensitive.']

    password = faker.word()
    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    user.set_password(password)
    user.save()

    data['username'] = user.email
    data['password'] = password

    response = client.post(url, data=data)
    assert response.status_code == 302


def test_registration(client, faker):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    password = faker.word()
    data = {
        'email': user.email,
        'password1': password,
        'password2': faker.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['User with that email already exists']
    assert errors['password2'] == ['The two password fields didn’t match.']

    data['email'] = faker.email()
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['password2'] == [
        'This password is too short. It must contain at least 8 characters.']

    password = faker.password()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302


def test_profile_view(client, login_client, faker):
    url = reverse('profile')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    response = client.get(reverse('profile'))
    assert response.status_code == 200
    assert response.context_data['user'][0] == user
    data = {
        'first_name': faker.word(),
        'last_name': faker.word(),
        'phone': faker.phone_number(),
    }
    response = client.post(reverse('profile'), data=data)
    assert response.status_code == 200


def test_verification_phone_view(client, login_client):
    url = reverse('verify_phone')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    # # Проверка сохранения кода в кэше
    # cache_key = f'verify_code_{user.phone}'
    # assert cache.get(cache_key) is not None

    # Отправка POST-запроса с правильным кодом
    data = {'code': '1234', 'phone': user.phone}
    response = client.post(reverse('verify_phone'), data=data)
    assert response.status_code == 302
    assert response.url == reverse('verify_phone')

    # Проверка изменения статуса телефона пользователя
    user.refresh_from_db()
    assert user.is_phone_valid

    # Отправка POST-запроса с неправильным кодом
    data = {'code': '0000', 'phone': user.phone}
    response = client.post(reverse('verify_phone'), data=data)
    assert response.status_code == 302
    assert response.url == reverse('verify_phone')
