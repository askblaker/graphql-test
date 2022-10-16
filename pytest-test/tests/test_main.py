import os
import sys
import requests

try:
    URL_FROM_ENV = os.environ["TEST_URL"]
except KeyError:
    print("PLEASE SET TEST_URL!")
    sys.exit(1)


def test_get_number():
    query = """
    {
        getNumber
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    assert response.json() == {"data": {"getNumber": 4}}


def test_get_string():
    query = """
    {
        getString
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    assert response.json() == {"data": {"getString": "Hello worlds!"}}


def test_get_fake_persons():
    query = """
    {
        getFakePersons {
            id
            name
            number
        }
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    persons = []
    for i in range(1000):
        persons.append({"id": str(i), "name": "test_" + str(i), "number": i})
    ret = response.json()["data"]["getFakePersons"]
    for i, person in enumerate(persons):
        assert person == ret[i]


def test_get_persons_empty():
    query = """
    {
        getPersons {
            id
            name
            number
        }
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    assert response.json() == {"data": {"getPersons": []}}


def test_insert_person():
    query = """
    mutation {
        addPerson(input: {
            name: "Test"
            number: 0
        }) {
            id
            name
            number
        }
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    returned = response.json()["data"]["addPerson"]
    assert returned["name"] == "Test"
    assert returned["number"] == 0


def test_get_persons_with_test_person():
    query = """
    {
        getPersons {
            id
            name
            number
        }
    }
    """
    response = requests.post(URL_FROM_ENV, json={"query": query})
    assert response.status_code == 200
    assert response.json() == {
        "data": {"getPersons": [{"id": "0", "name": "Test", "number": 0}]}
    }
