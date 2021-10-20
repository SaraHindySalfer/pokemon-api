from flask import Response
from config import connection


# receives data from server and updates type table
def update_type_table(pokemon_name, data):
    for type in data:
        type = type['type']['name']
        try:
            ids = []
            with connection.cursor() as cursor:
                query = f"select id from pokemon where name='{pokemon_name}'"
                cursor.execute(query)
                result = cursor.fetchall()
                for i in result:
                    ids.append(i['id'])
                connection.commit()
            for id in ids:
                with connection.cursor() as cursor:
                    query = f"insert into type (pokemon_id,pokemon_type) values({id},'{type}')"
                    cursor.execute(query)
                    connection.commit()
        except Exception as e:
            return Response("Error: " + str(e), 403)


# receives data as request and adds a new pokemon to the pokemon table
def add_pokemon(req, info):
    try:
        if req.status_code != 404:
            data = req.json()['types']
            for i in data:
                with connection.cursor() as cursor:
                    query = f"INSERT into type (pokemon_id,pokemon_type) VALUES ({info['id']},'{i['type']['name']}') "
                    cursor.execute(query)
                    connection.commit()
            with connection.cursor() as cursor:
                query = f"INSERT into pokemon (id,name ,weight,height) VALUES ({info['id']},'{info['name']}','{info['weight']}','{info['height']}') "
                cursor.execute(query)
                connection.commit()
    except Exception as e:
        return Response("error: ", str(e))


# returns pokemon names that are of the given type
def get_pokemon_with_type(type):
    names = []
    try:
        with connection.cursor() as cursor:
            query = f"select pokemon.name from pokemon,type where pokemon.id=type.pokemon_id and type.pokemon_type='{type}' "
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                names.append(i['name'])

    except Exception as e:
        return Response("error: " + str(e), 403)
    return names


# returns pokemon names that have the given trainer
def get_pokemon_with_trainer(trainer_name):
    with connection.cursor() as cursor:
        query = f"SELECT pokemon.name from pokemon , OwnedBy where pokemon.id=OwnedBy.pokemon_id and trainer_name='{trainer_name}';"
        cursor.execute(query)
        result = cursor.fetchall()
        names = []
        for i in result:
            names.append(i['name'])
        return names


# updates pokemon to the new one he evolved to
def evolve_pokemon(name, trainer_name, pokemon_id):
    with connection.cursor() as cursor:
        query = f"SELECT id from pokemon where name ='{name}';"
        cursor.execute(query)
        result = cursor.fetchall()
        id = result[0]['id']
    with connection.cursor() as cursor:
        query = f"SELECT * FROM OwnedBy WHERE pokemon_id={pokemon_id} and trainer_name='{trainer_name}';"
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return Response("trainer and pokemon do not match")
    with connection.cursor() as cur:
        query2 = f"update OwnedBy set pokemon_id={id} where trainer_name='{trainer_name}' and pokemon_id={pokemon_id}"
        cur.execute(query2)
        connection.commit()


# deletes pokemon from table
def delete_pokemon(pokemon_id, trainer_name):
    with connection.cursor() as cursor:
        query = f"DELETE FROM OwnedBy WHERE pokemon_id = {pokemon_id} and trainer_name = '{trainer_name}';"
        cursor.execute(query)
        connection.commit()
