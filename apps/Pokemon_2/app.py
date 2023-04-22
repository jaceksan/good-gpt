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

# streamlit app
def app():
    st.title("Pokemon Abilities")
    name = st.text_input("Enter Pokemon Name:")
    if name:
        abilities = get_pokemon_data(name.lower())
        if abilities:
            st.write(f"{name.capitalize()} has the following abilities:")
            for ability in abilities:
                st.write(f"- {ability.capitalize()}")
        else:
            st.write(f"Pokemon '{name.capitalize()}' not found.")