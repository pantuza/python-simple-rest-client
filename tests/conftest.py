import pytest

from simple_rest_client.resource import BaseResource, Resource
from simple_rest_client.api import API


@pytest.fixture
def base_resource():
    return BaseResource


custom_action_urls = {
    'list': '{}/users',
    'create': '{}/users',
    'retrieve': '{}/users/{}',
    'update': '{}/users/{}',
    'partial_update': '{}/users/{}',
    'destroy': '{}/users/{}'
}


@pytest.fixture
def action_urls():
    return custom_action_urls


class CustomResource(Resource):
    action_urls = custom_action_urls


@pytest.fixture
def custom_resource():
    return CustomResource


@pytest.fixture
def reqres_resource():
    return Resource(
        api_root_url='https://reqres.in/api/', resource_name='users',
        json_encode_body=True
    )


@pytest.fixture
def api():
    return API(api_root_url='https://reqres.in/api/', json_encode_body=True)


@pytest.fixture
def reqres_api(api):
    api.add_resource(resource_name='users')
    api.add_resource(resource_name='login')
    return api
