```python
import requests
import streamlit as st

# function to retrieve pokemon data from PokeAPI
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        return None

# streamlit app
def app():
    st.title("PokeAPI App")
    pokemon_name = st.text_input("Enter Pokemon Name:")
    if pokemon_name:
        pokemon_data = get_pokemon_data(pokemon_name.lower())
        if pokemon_data:
            abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
            st.write(f"Abilities of {pokemon_name.capitalize()}:")
            for ability in abilities:
                st.write(f"- {ability.capitalize()}")
        else:
            st.write(f"Pokemon {pokemon_name.capitalize()} not found!")
```