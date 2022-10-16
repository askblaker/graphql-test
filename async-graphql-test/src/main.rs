use async_graphql::{
    http::{playground_source, GraphQLPlaygroundConfig},
    Context, InputObject, Object, SimpleObject, ID,
};
use async_graphql::{EmptySubscription, Schema};
use async_graphql_axum::{GraphQLRequest, GraphQLResponse};
use axum::{
    extract::Extension,
    response::{self, IntoResponse},
    routing::get,
    Router, Server,
};
use futures_util::lock::Mutex;
use slab::Slab;
use std::sync::Arc;

struct Query;
struct Mutation;

#[derive(SimpleObject, InputObject, Clone)]
pub struct Person {
    name: String,
    id: String,
    number: Option<i32>,
}

#[derive(SimpleObject, InputObject, Clone)]
pub struct PersonInput {
    name: String,
    number: Option<i32>,
}

#[Object]
impl Query {
    async fn get_string(&self) -> &str {
        "Hello worlds!"
    }
    async fn get_number(&self) -> &i32 {
        &4
    }
    async fn get_persons(&self, ctx: &Context<'_>) -> Vec<Person> {
        let myvec = ctx.data_unchecked::<Storage>().lock().await;
        myvec.iter().map(|(_, num)| num).cloned().collect()
    }

    async fn get_fake_persons(&self) -> Vec<Person> {
        fn create_persons() -> Vec<Person> {
            let mut persons = Vec::new();
            for i in 0..=1000 {
                let mut owned_string = "test_".to_owned();
                let number_copy = i.clone();
                owned_string.push_str(&number_copy.to_string());
                persons.push(Person {
                    name: owned_string,
                    number: Some(i),
                    id: i.to_string(),
                })
            }
            persons
        }
        create_persons()
    }
}

pub type Storage = Arc<Mutex<Slab<Person>>>;

#[Object]
impl Mutation {
    async fn its_true(&self, _number: i32) -> bool {
        true
    }

    async fn add_person(&self, ctx: &Context<'_>, input: PersonInput) -> Person {
        let mut store = ctx.data_unchecked::<Storage>().lock().await;
        println!("store len: {}", store.len().clone());

        let new_entry = store.vacant_entry();
        let id: ID = new_entry.key().into();
        let number_clone = input.number;
        let name_clone = input.name.clone();

        new_entry.insert(Person {
            name: input.name,
            id: id.to_string(),
            number: input.number,
        });
        println!("Inserted ID: {:#?}", id);
        Person {
            id: id.to_string(),
            number: number_clone,
            name: name_clone,
        }
    }
}

#[tokio::main]
async fn main() {
    let new_store: Storage = Storage::default();
    let my_schema = Schema::build(Query, Mutation, EmptySubscription)
        .data(new_store)
        .finish();

    async fn graphql_handler(
        schema: Extension<Schema<Query, Mutation, EmptySubscription>>,
        req: GraphQLRequest,
    ) -> GraphQLResponse {
        schema.execute(req.into_inner()).await.into()
    }

    async fn playground() -> impl IntoResponse {
        response::Html(playground_source(GraphQLPlaygroundConfig::new(
            "http://localhost:8001",
        )))
    }

    let app = Router::new()
        .route("/graph", get(playground).post(graphql_handler))
        .layer(Extension(my_schema));

    println!("GraphiQL IDE: http://localhost:8001");

    Server::bind(&"0.0.0.0:8001".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
