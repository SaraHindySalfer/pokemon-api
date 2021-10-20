# Pokemon
SQL and Flask Pokemons api in python.

## Technologies
* flask
* pymysql

## Description
PokeCorp is a company that tracks pokemon and their trainers around the world. 

 

Until this day, they've been storing all their data together, in the attached JSON file that looks like this: 

 

```
[{ 
    "id": <pokemon_id>, 
    "name": <pokemon_name>, 
    "type": <pokemon_type>, 
    "height": <pokemon_height>, 
    "weight": <pokemon_weight>, 
    "ownedBy": [ 
      {name: <trainer_name>, town: <trainer_town>}, 
      ... 
    ] 
}, 
...] 
```

 

The file has 151 pokemon in it. Each pokemon has some data, as well as an ownedBy field. 

 

The ownedBy field is an array of objects, where each object represents a trainer that owns this pokemon - note that this array might be empty. 

In this project we were required to migrate all of the data to an SQL database, create the tables using plain SQL, and then do all the INSERTs in python using the pymysql package. 

Once we were done, we wrote functions for the following queries:

* **heaviest_ pokemon():** returns the heaviest pokemon (the one with the biggest weight property).
* **find_by_type(type):** receives a pokemon type, and returns all of the pokemon names with that type.
* **find_owners(pokemon __name):** receives the name of a pokemon, and returns the names of all the trainers that own it, or an empty array if no one owns it.
* **find_roster(trainer_name):** receives the name of a trainer, and returns the names of all the pokemon he or she owns.
* **finds_most_owned():** finds the most owned pokemon, meaning the pokemon that has the highest number of owners.

At the next stage, we were required to implement a server with api to the pokemons database. The api:

* `/pokemons/<trainer>` `GET`: returns all the pokemons of a given owner.
* `/trainers/<pokemon>` `GET`: returns all the trainers of a given pokemon.
* `/pokemons` `POST`: adds a new pokemon with the following information: id, name, height, weight, types (all of them).
* `/pokemons/get_by_type/<pokemon_type>` `GET`: returns all pokemons with the specific type.
* `/pokemons/<pokemon_id>` `DELETE`: deletes pokemon.
* `/pokemons/<trainer>` `DELETE`: deletes all pokemons of trainer.
* `/pokemons/types/<pokemon_name>` `PUT`: updates pokemon types.
* `/evolve` `PUT`: [evolves](https://github.com/AyalaGottfried/Pokemon/blob/master/README.md#evolution) specific pokemon of specific trainer.

#### Evolution
1. Get the info of a specific pokemon. 

2. From the pokemon general info, get the species url. 

3. Get the info of the species, by making a request to the species url .

4. From the species info get the evolution chain url.

5. Get the info of the evolution chain, by making a request to the evolution chain url.

6. From the evolution chain info get the chain item.

7. Scan the chain item to find what is the next form of your pokemon.

8. You should end up with the name of the evolved pokemon. 

9. Update the DB accordingly.

## Original database
[Pokémon Data](https://pokeapi.co/)
