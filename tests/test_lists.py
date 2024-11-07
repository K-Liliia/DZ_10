from faker import Faker
from pytest_steps import test_steps

fake = Faker()

import requests

base_url='https://api.clickup.com/api/v2'
headers = {'Authorization': 'pk_2144419997_FYG8LWOXN4N816EUCCV0E0YAGXF3LEUI'}

@test_steps('Get all list')
def test_get_lists():
    response = requests.get(base_url + '/folder/90122619397/list?archived=false', headers=headers)
    assert response.status_code == 200
    yield

@test_steps('Create a new list')
def test_create_list():
    body = {'name': fake.name(), 'content': fake.text()}
    print(body)
    response = requests.post(base_url + '/folder/90122619397/list', headers=headers, data=body)
    assert response.status_code == 200, f'Request has status {response.text}'
    yield

@test_steps('Get all folderless lists')
def test_get_no_folder_lists():
    response = requests.get(base_url + '/space/90121459531/list', headers=headers)
    assert response.status_code == 200
    yield

@test_steps('Create no folderless list')
def test_create_no_folder_list():
    body = {'name': fake.first_name(), 'content': fake.name()}
    print(body)
    response = requests.post(base_url + '/space/90121459531/list', headers=headers, data=body)
    assert response.status_code == 200
    yield

@test_steps('Get list by id')
def test_get_list_by_id():
    response = requests.get(base_url + '/list/901205382998', headers=headers)
    assert response.status_code == 200
    yield

@test_steps('Create new list','Update list by id')
def test_update_list_by_id():
    body = {'name': fake.first_name(), 'content': fake.text()}
    print(body)
    response = requests.post(base_url + '/folder/90122619397/list', headers=headers, data=body)
    assert response.status_code == 200, f'Request has status {response.text}'
    list_id = response.json()['id']
    print('List id is: '+ list_id)
    yield
    updated_body = {'name': fake.first_name(), 'content': fake.address()}
    response_new = requests.put(f'{base_url}/list/{list_id}', headers=headers, data=updated_body)
    assert response_new.status_code == 200, f'Request has status {response_new.text}'
    yield

@test_steps('Create new list', 'Update the list')
def test_delete_list_by_id():
    body = {'name': fake.name(), 'content': fake.text()}
    print(body)
    response = requests.post(base_url + '/folder/90122619397/list', headers=headers, data=body)
    assert response.status_code == 200, f'Request has status {response.text}'
    list_id = response.json()['id']
    yield
    print('List id is: ' + list_id)
    updated_body = {'name': fake.first_name(), 'content': fake.address()}
    response_new = requests.delete(f"{base_url}/list/{list_id}", headers=headers, data=updated_body)
    assert response_new.status_code == 200, f'Request has status {response_new.text}'
    yield