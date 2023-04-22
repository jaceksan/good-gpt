# function to retrieve pokemon data from PokeAPI
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        abilities = [ability['ability']['name'] for ability in data['abilities']]
        return abilities
    else:
        return None

# command line arguments
parser = argparse.ArgumentParser(description='Retrieve Pokemon abilities from PokeAPI.')
parser.add_argument('name', type=str, help='Name of the Pokemon')

# main function
def main():
    args = parser.parse_args()
    name = args.name.lower()
    abilities = get_pokemon_data(name)
    if abilities:
        print(f"{name.capitalize()} has the following abilities:")
        for ability in abilities:
            print(f"- {ability.capitalize()}")
    else:
        print(f"Pokemon '{name.capitalize()}' not found.")

if __name__ == '__main__':
    main()