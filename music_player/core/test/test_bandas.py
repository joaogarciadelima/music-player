import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_banda(banda):
    assert isinstance(banda.id, int)
    assert 'teste' == banda.nome
    assert banda.imagem is not None
    banda.delete()


@pytest.mark.django_db(transaction=True)
def test_get_view_banda(api_client):
    url = reverse(resolve('/api/v1/banda').url_name)
    response = api_client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_banda_without_login(client, genero):
    url = f'/bandas/{genero.id}'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db(transaction=True)
def test_get_view_banda_id(banda, api_client):
    url = reverse(resolve('/api/v1/banda').url_name)
    response = api_client.get(url + f'/{banda.id}')
    assert status.is_success(response.status_code)
    banda.delete()


@pytest.mark.django_db(transaction=True)
def test_post_view_banda(api_client, genero):
    url = reverse(resolve('/api/v1/banda').url_name)
    data = {'nome': 'teste', 'genero_id': genero.id}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_banda_img(api_client, genero, b64_capa):
    url = reverse(resolve('/api/v1/banda').url_name)
    data = {'nome': 'teste', 'genero_id': genero.id, 'imagem': b64_capa}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
