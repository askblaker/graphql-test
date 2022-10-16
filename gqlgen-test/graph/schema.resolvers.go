package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"
	"gqlgen-test/graph/generated"
	"gqlgen-test/graph/model"
	"strconv"
)

// AddPerson is the resolver for the addPerson field.
func (r *mutationResolver) AddPerson(ctx context.Context, input model.PersonInput) (*model.Person, error) {
	id_string := ""
	if len(person_store) == 0 {
		id_string = strconv.Itoa(len(person_store))
	} else {
		id_string = strconv.Itoa(len(person_store) + 1)
	}
	new_person := model.Person{
		Name:   &input.Name,
		Number: &input.Number,
		ID:     &id_string,
	}
	person_store = append(person_store, new_person)
	return &new_person, nil
}

// ItsTrue is the resolver for the itsTrue field.
func (r *mutationResolver) ItsTrue(ctx context.Context, number *int) (*bool, error) {
	mybool := true
	return &mybool, nil
}

// GetString is the resolver for the getString field.
func (r *queryResolver) GetString(ctx context.Context) (*string, error) {
	toReturn := "Hello worlds!"
	return &toReturn, nil
}

// GetNumber is the resolver for the getNumber field.
func (r *queryResolver) GetNumber(ctx context.Context) (*int, error) {
	toReturn := 4
	return &toReturn, nil
}

// GetPersons is the resolver for the getPersons field.
func (r *queryResolver) GetPersons(ctx context.Context) ([]*model.Person, error) {
	var new_pointer_slice []*model.Person
	for _, v := range person_store {
		new_pointer := &v
		new_pointer_slice = append(new_pointer_slice, new_pointer)
	}
	return new_pointer_slice, nil
}

// GetFakePersons is the resolver for the getFakePersons field.
func (r *queryResolver) GetFakePersons(ctx context.Context) ([]*model.Person, error) {
	var personsToReturn []*model.Person
	for i := 0; i <= 1000; i++ {
		name := "test_" + strconv.Itoa(i)
		id := strconv.Itoa(i)
		number := i
		newPerson := model.Person{Name: &name, Number: &number, ID: &id}
		personsToReturn = append(personsToReturn, &newPerson)
	}
	return personsToReturn, nil
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }

// !!! WARNING !!!
// The code below was going to be deleted when updating resolvers. It has been copied here so you have
// one last chance to move it out of harms way if you want. There are two reasons this happens:
//   - When renaming or deleting a resolver the old code will be put in here. You can safely delete
//     it when you're done.
//   - You have helper methods in this file. Move them out to keep these resolver files clean.
var person_store []model.Person
