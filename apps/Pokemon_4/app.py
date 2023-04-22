def get_pokemon_abilities(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        abilities = [ability["ability"]["name"] for ability in data["abilities"]]
        return abilities
    else:
        return None

st.title("Pokemon Abilities Finder")
pokemon_name = st.text_input("Enter the name of a Pokemon:")

if st.button("Find Abilities"):
    abilities = get_pokemon_abilities(pokemon_name)
    if abilities:
        st.write(f"Abilities of {pokemon_name.capitalize()} are:")
        for ability in abilities:
            st.write(ability)
    else:
        st.write("Pokemon not found. Please check the name and try again.")