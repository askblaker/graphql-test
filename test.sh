#!/bin/bash

declare -a libs=( "ariadne" "async-graphql" "gqlgen" "mercurius" )
declare -a commands=( "poetry run uvicorn src.main:app" "cargo run" "go run server.go" "npx ts-node ./src/main.ts" )

pushd .
cd ariadne-test
nohup poetry run uvicorn src.main:app > /dev/null 2>&1 &
serverPID=$!
cd ..
task pytest:ariadne
task perftest:ariadne
kill $serverPID
popd

pushd .
cd async-graphql-test
nohup cargo run --release > /dev/null 2>&1 &
sleep 10
serverPID=$!
cd ..
task pytest:async-graphql
task perftest:async-graphql
kill $serverPID
popd

pushd .
cd gqlgen-test
nohup go run server.go > /dev/null 2>&1 &
sleep 5 # Need to wait for the process to come alive
serverPID=$!
cd ..
task pytest:gqlgen
task perftest:gqlgen
kill $serverPID
popd

pushd .
cd mercurius-test
nohup npx ts-node ./src/main.ts > /dev/null 2>&1 &
sleep 5 # Need to wait for the process to come alive
serverPID=$!
cd ..
task pytest:mercurius
task perftest:mercurius
kill $serverPID
popd