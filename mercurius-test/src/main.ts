"use strict";

import Fastify from "fastify";
import mercurius from "mercurius";

const app = Fastify({
  // logger: true
});

const schema = `
  type Query {
    getString: String
    getNumber: Int
    getPersons: [Person]
    getFakePersons: [Person]
  }

  type Mutation {
    addPerson(input: PersonInput): Person
  }

  input PersonInput {
    name: String
    number: Int
  }

  type Person {
    name: String
    number: Int
    id: String
  }
`;

interface Person {
  name: string;
  number: number;
  id: string;
}

const persons: Person[] = [];

const resolvers = {
  Query: {
    getString: async () => "Hello worlds!",
    getNumber: async () => 4,
    getPersons: async () => persons,
    getFakePersons: async () => {
      const newPersons = [];
      for (let i = 0; i < 1000; i++) {
        newPersons.push({
          id: i.toString(),
          name: "test_" + i.toString(),
          number: i,
        });
      }
      return newPersons;
    },
  },
  Mutation: {
    addPerson: async (obj: any, args: any, ctx: any) => {
      persons.push({ ...args.input, id: args.input.number.toString() });
      return args.input;
    },
  },
};

app
  .register(mercurius, {
    schema,
    resolvers,
    graphiql: true,
    path: "/graph",
  })
  .after((err: any) => {
    /* eslint-disable-next-line @typescript-eslint/strict-boolean-expressions */
    if (err) throw err;
  });

const PORT = 8003;
app.listen({ host: "0.0.0.0", port: PORT }, () => {
  console.log(`Server running on port ${PORT}`);
});
