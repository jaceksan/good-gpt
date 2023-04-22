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

# main function to display abilities of a pokemon
def display_pokemon_abilities():
    st.title("Pokemon Abilities")
    pokemon_name = st.text_input("Enter Pokemon Name:")
    if pokemon_name:
        pokemon_data = get_pokemon_data(pokemon_name.lower())
        if pokemon_data:
            abilities = pokemon_data["abilities"]
            st.write(f"**{pokemon_name.capitalize()}** has the following abilities:")
            for ability in abilities:
                st.write(f"- {ability['ability']['name'].capitalize()}")
        else:
            st.write("Pokemon not found. Please enter a valid Pokemon name.")

# run the program
if __name__ == "__main__":
    display_pokemon_abilities()
```