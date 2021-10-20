import json

from flask import Flask, request, Response
import requests

from pokeApi_module import get_pok_details
from sql_queries import find_owners
from DB_module import update_type_table, get_pokemon_with_type, get_pokemon_with_trainer, evolve_pokemon, \
    delete_pokemon, add_pokemon
from config import port, host

app = Flask(__name__)


@app.route('/')
def start():
    return Response("server up and running")


# route to http://127.0.0.1:3000/updateTypes/<name to update pokemon types>
# updates the "type" table corresponding the pokeApi
@app.route('/updateTypes/<pokemon_name>', methods=['PUT'])
def update_types(pokemon_name):
    req = get_pok_details(pokemon_name)
    data = req.json()['types']
    update_type_table(pokemon_name, data)
    return Response("ok", status=200)


# route to http://127.0.0.1:3000/addPokemon
# adds a new pokemon to the DB, body:{"name":"***","id":**,"height":**,"weight:":**}
@app.route('/addPokemon', methods=['POST'])
def addPokemon():
    info = request.get_json()
    print(info)
    req = get_pok_details(info['name'])
    add_pokemon(req, info)
    return Response("ok")

# route to http://127.0.0.1:3000/pokemon_by_type/<type>
# returns all the pokemon of the certain type
@app.route('/pokemon_by_type/<type>', methods=['GET'])
def get_pokemon_by_type(type):
    names = get_pokemon_with_type(type)
    return Response(json.dumps(names), 200)

# route to http://127.0.0.1:3000/get_pokemon_by_trainer/<trainer>
# returns all pokemon of certain trainer
@app.route('/get_pokemon_by_trainer/<trainer_name>', methods=['GET'])
def get_pokemon_by_trainer(trainer_name):
    try:
        names = get_pokemon_with_trainer(trainer_name)
        return Response(json.dumps(names), 200)
    except Exception as e:
        return Response("error: " + str(e), 408)

# route to http://127.0.0.1:3000/trainer_by_pokemon/<pokemon>
# returns all trainers of certain pokemon
@app.route('/trainer_by_pokemon/<pokemon_name>', methods=['GET'])
def get_trainer_by_pokemon(pokemon_name):
    try:
        owners = find_owners(pokemon_name)
        return Response(json.dumps(owners), 200)
    except Exception as e:
        return Response("error: " + str(e), 402)

# route to http://127.0.0.1:3000/evolve/<pokemon_id>/<trainer_name>
# evolves the pokemon of trainer to next type
@app.route('/evolve/<pokemon_id>/<trainer_name>')
def evolve(pokemon_id, trainer_name):
    try:
        req = get_pok_details(pokemon_id)
        pokemon_info = req.json()
        species_url = pokemon_info['species']['url']
        species_info = requests.get(species_url, verify=False).json()
        evolution_url = species_info['evolution_chain']['url']
        evolution_chain_info = requests.get(evolution_url, verify=False).json()
        chain_item = evolution_chain_info['chain']
        if chain_item['evolves_to']:
            chain_item = chain_item['evolves_to']
            name = chain_item[0]['species']['name']
            evolve_pokemon(name, trainer_name, pokemon_id)
        else:
            return Response("cannot evolve pokemon")
        return Response("ok")
    except Exception as e:
        return Response("error: " + str(e))

# route to http://127.0.0.1:3000/delete_pokemon_by_trainer/<trainer_name>/<pokemon_id>
# deletes pokemon
@app.route('/delete_pokemon_by_trainer/<trainer_name>/<pokemon_id>', methods=['DELETE'])
def delete_pokemon_by_trainer(trainer_name, pokemon_id):
    try:
        delete_pokemon(pokemon_id, trainer_name)
        return Response("ok", 200)
    except Exception as e:
        return Response("error: " + str(e), 408)


if __name__ == '__main__':
    app.run(host=host, port=port)
