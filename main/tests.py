from django.core import mail
from django.urls import reverse

from project import settings


def test_homepage(client):
    url = reverse('main')
    response = client.get(url)
    assert response.status_code == 200


def test_contact_form_view(client, faker):
    form_data = {'name': faker.word(), 'message': faker.text()}
    response = client.post(reverse('contact_form'), form_data) 

    assert response.status_code == 302
    assert response.url == reverse('main')

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == 'New Contact Form Submission'
    assert email.body == f'Name: {form_data["name"]}\nMessage: {form_data["message"]}'
    assert email.from_email == settings.DEFAULT_FROM_EMAIL
    assert email.to == [settings.CONTACT_FORM_EMAIL]

    messages = list(response.wsgi_request._messages)
    assert len(messages) == 1
    assert str(messages[0]) == 'Messages sent!'
