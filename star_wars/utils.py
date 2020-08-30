import requests


class RequestError(Exception):
    pass


def parse_homeworld_id(api_character_response):
    homeworld_id = api_character_response['homeworld'].split('/')[-2]
    return homeworld_id


def parse_species_name(api_character_response):
    species_url = api_character_response['species']
    species_name = ""
    for specie in species_url:
        species_data = requests.get(specie).json()
        species_name += species_data['name']+"/"

    return species_name[:-1]


def parse_homeworld_data(response_data):
    data = {key: response_data[key]
            for key in ['name', 'population', 'residents']}
    data['known_residents_count'] = len(data['residents'])
    del data['residents']
    return data
