import typing
import strawberry
from strawberry.asgi import GraphQL

persons_store = []


@strawberry.type
class Person:
    name: str
    number: int
    id: str


@strawberry.input
class PersonInput:
    name: str
    number: int


def get_fake_persons():
    persons = []
    for i in range(1000):
        persons.append(Person(name="test_" + str(i), number=i, id=str(i)))
    return persons


def get_persons():
    return persons_store


@strawberry.type
class Mutation:
    @strawberry.field
    def add_person(self, input: PersonInput) -> Person:
        id = 0
        if len(persons_store) > 0:
            id = len(persons_store) + 1
        new_person = Person(name=input.name, number=input.number, id=id)
        persons_store.append(new_person)
        return new_person


@strawberry.type
class Query:
    getPersons: typing.List[Person] = strawberry.field(resolver=get_persons)
    getFakePersons: typing.List[Person] = strawberry.field(resolver=get_fake_persons)
    getString: str = strawberry.field(lambda: "Hello worlds!")
    getNumber: int = strawberry.field(lambda: 4)


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = GraphQL(schema)
