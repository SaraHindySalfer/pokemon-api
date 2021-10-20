import json
import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    db="sql_intro",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


# insert pokemon to table
def insert_pokemon(i):
    try:
        with connection.cursor() as cursor:
            id = i['id']
            name = i['name']
            weight = i['weight']
            height = i['height']
            query = f"INSERT into pokemon (id,name, height,weight) VALUES ({id},'{name}', {height},{weight}) "
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print("error in inserting content", e)


# insert trainer to table
def insert_trainer(trainer_details, i):
    # do we need to check for duplicate rows or let them get thrown by the exception
    trainers = i['ownedBy']
    try:
        for i in trainers:
            name = i['name']
            town = i['town']
            if name not in trainer_details:
                trainer_details.append(name)
                with connection.cursor() as cursor:
                    query = f"INSERT into trainer (name,town) values ('{name}', '{town}')"
                    cursor.execute(query)
            else:
                pass
            connection.commit()
    except Exception as e:
        print("Error", e)


# insert pokemon owned by trainer to table
def insert_owned_by(i):
    for j in i["ownedBy"]:
        id = i["id"]
        name = j["name"]
        try:
            with connection.cursor() as cursor:
                query = f"INSERT into OwnedBy (pokemon_id , trainer_name) VALUES ({id},'{name}') "
                cursor.execute(query)
                connection.commit()
        except Exception as e:
            print("error in inserting content", e)

# insert data to trainer and pokemon tables
def insert_data():
    trainer_details = []
    try:
        with open('pokemon_data.json', "r") as pokemon_data:
            content = json.load(pokemon_data)
            for i in range(len(content)):
                insert_pokemon(content[i])
                insert_trainer(trainer_details, content[i])
            for j in range(len(content)):
                insert_owned_by(content[j])

    except Exception as e:
        print("error", e)

# query to select the heaviest pokemon
def heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = 'select name From pokemon where weight=(select max(weight)from pokemon)'
            cursor.execute(query)
            result = cursor.fetchall()[0]['name']
            print(result)
            connection.commit()
    except Exception as e:
        print("error", e)

# query to select pokemon that are the given type
def find_by_type(type):
    type = type
    names = []
    try:
        with connection.cursor() as cursor:
            query = f"SELECT name FROM pokemon where type='{type}'"
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                names.append(i['name'])
            print(names)
    except Exception as e:
        print("error", e)

# query to find owners of specific pokemon
def find_owners(pokemon_name):
    owners = []
    try:
        with connection.cursor() as cursor:
            query = f"select OwnedBy.trainer_name from OwnedBy,pokemon where OwnedBy.pokemon_id=pokemon.id and " \
                    f"pokemon.name='{pokemon_name}' "
            cursor.execute(query)
            result = cursor.fetchall()
            for j in result:
                owners.append(j['trainer_name'])
            print(owners)
            connection.commit()
            return owners
    except Exception as e:
        print("error", e)

# query to find trainers of certain pokemon
def find_roster(trainer_name):
    names = []
    try:
        with connection.cursor() as cursor:
            query = f"SELECT pokemon.name from pokemon , OwnedBy where pokemon.id=OwnedBy.pokemon_id and trainer_name='{trainer_name}';"
            cursor.execute(query)
            result = cursor.fetchall()
            for i in result:
                names.append(i['name'])
            print(names)
    except Exception as e:
        print("error", e)


if __name__ == '__main__':
    insert_data()
