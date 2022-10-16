from ariadne import QueryType, MutationType, make_executable_schema, gql
from ariadne.asgi import GraphQL


type_defs = gql(
    """
type Query {
  getString: String
  getNumber: Int
  getPersons: [Person]
  getFakePersons: [Person]
}

type Mutation {
  addPerson(input: PersonInput): Person
  itsTrue(number: Int): Boolean
}

input PersonInput {
    name: String!
    number: Int!
}

type Person {
  name: String
  number: Int
  id: String
}
"""
)

query = QueryType()
mutation = MutationType()


persons_store = []


@query.field("getString")
async def resolve_hello(_, info):
    return "Hello worlds!"


@query.field("getNumber")
async def resolve_staticnumber(_, info):
    return 4


@query.field("getFakePersons")
async def resolve_fakepersons(_, info):
    persons = []
    for i in range(1000):
        persons.append({"name": "test_" + str(i), "id": str(i), "number": i})
    return persons


@query.field("getPersons")
async def resolve_get_persons(_, info):
    return persons_store


@mutation.field("addPerson")
async def resolve_addperson(_, info, input):
    if len(persons_store) == 0:
        input["id"] = str(len(persons_store))
    else:
        input["id"] = str(len(persons_store) + 1)
    persons_store.append(input)
    return input


@mutation.field("itsTrue")
async def resolve_itstrue(_, info, number):
    return True


schema = make_executable_schema(type_defs, query, mutation)
app = GraphQL(schema, debug=True)
