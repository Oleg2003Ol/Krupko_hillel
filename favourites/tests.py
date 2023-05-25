from django.contrib import messages
from django.urls import reverse


def test_favourite(client, login_client, product_factory):
    url = reverse('favourites')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200

    product = product_factory()
    favorite_url = reverse('add_or_remove_favorite', args=[product.id])
    response = client.get(favorite_url, follow=True)

    messages_list = list(messages.get_messages(response.wsgi_request))
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('products')
    assert response.redirect_chain[0][1] == 302
    assert len(messages_list) == 1
    assert str(messages_list[0]) == 'Product add to Favorites!'

    response = client.get(favorite_url, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('products')
    assert response.redirect_chain[0][1] == 302

    messages_list = list(messages.get_messages(response.wsgi_request))
    assert len(messages_list) == 1
    assert str(messages_list[0]) == 'Product delete from Favorites!'
