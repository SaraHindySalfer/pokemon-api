import requests

# routes to pokeApi url and returns the details
def get_pok_details(data):
    url = 'https://pokeapi.co/api/v2/pokemon/' + data
    return requests.get(url, verify=False)
