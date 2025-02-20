from django.urls import reverse

from feedbacks.models import Feedback


def test_feedbacks_list(client, faker, login_client):
    url = reverse('feedbacks')
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    for _ in range(3):
        Feedback.objects.create(
            text=faker.sentence(),
            rating=faker.random_int(min=1, max=5),
            user_id=user.id
            )
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['feedbacks']) == Feedback.objects.count()


def test_create_feedback(client, faker, login_client):
    url = reverse('feedbacks_create')
    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    Feedback.objects.create(
        text=faker.sentence(),
        rating=faker.random_int(min=1, max=5),
        user_id=user.id
    )
    response = client.get(url)
    assert response.status_code == 200
    feedbacks = Feedback.objects.filter(user=user)
    assert feedbacks.count() == 1

