import pytest
import status

from tests.vcr import vcr


def test_base_resource_action_urls(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.action_urls == resource.default_action_urls


def test_base_resource_get_full_url(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.get_full_url('list') == 'http://example.com/users'
    assert resource.get_full_url('create') == 'http://example.com/users'
    assert resource.get_full_url('retrieve', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('update', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('partial_update', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('destroy', 1) == 'http://example.com/users/1'


def test_base_resource_get_full_url_with_append_slash(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users', append_slash=True)
    assert resource.get_full_url('list') == 'http://example.com/users/'
    assert resource.get_full_url('create') == 'http://example.com/users/'
    assert resource.get_full_url('retrieve', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('update', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('partial_update', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('destroy', 1) == 'http://example.com/users/1/'


def test_base_resource_get_full_url_with_invalid_action(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    with pytest.raises(ValueError) as execinfo:
        resource.get_full_url('listy')
    assert 'No url match for "listy"' in str(execinfo)


def test_base_resource_build_request_instance(base_resource):
    resource = base_resource(
        api_root_url='http://example.com', resource_name='users',
        json_encode_body=True
    )
    request = resource.build_request_instance(
        1, action_name='update', method='PUT', params={}, body={'body': True},
        headers={}, timeout=3
    )
    assert request.url == 'http://example.com/users/1'
    assert request.method == 'PUT'
    assert request.body == '{"body": true}'


def test_custom_resource_action_urls(custom_resource, action_urls):
    resource = custom_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.action_urls == action_urls


def test_custom_resource_get_full_url(custom_resource):
    resource = custom_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.get_full_url('list', 1) == 'http://example.com/1/users'
    assert resource.get_full_url('create', 1) == 'http://example.com/1/users'
    assert resource.get_full_url('retrieve', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('partial_update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('destroy', 1, 2) == 'http://example.com/1/users/2'


@vcr.use_cassette()
def test_resource_list(reqres_resource):
    response = reqres_resource.list()
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users'


@vcr.use_cassette()
def test_resource_create(reqres_resource):
    body = {'name': 'morpheus', 'job': 'leader'}
    response = reqres_resource.create(body=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.method == 'POST'
    assert response.url == 'https://reqres.in/api/users'


@vcr.use_cassette()
def test_resource_retrieve(reqres_resource):
    id = 2
    response = reqres_resource.retrieve(id)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users/2'


@vcr.use_cassette()
def test_resource_update(reqres_resource):
    id = 2
    body = {'name': 'morpheus', 'job': 'zion resident'}
    response = reqres_resource.update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PUT'
    assert response.url == 'https://reqres.in/api/users/2'


@vcr.use_cassette()
def test_resource_partial_update(reqres_resource):
    id = 2
    body = {'name': 'morpheus', 'job': 'zion resident'}
    response = reqres_resource.partial_update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PATCH'
    assert response.url == 'https://reqres.in/api/users/2'


@vcr.use_cassette()
def test_resource_destroy(reqres_resource):
    id = 2
    response = reqres_resource.destroy(id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.method == 'DELETE'
    assert response.url == 'https://reqres.in/api/users/2'
