// Code generated by github.com/99designs/gqlgen, DO NOT EDIT.

package model

type Person struct {
	Name   *string `json:"name"`
	Number *int    `json:"number"`
	ID     *string `json:"id"`
}

type PersonInput struct {
	Name   string `json:"name"`
	Number int    `json:"number"`
}