import requests

base_url = "https://pokeapi.co/api/v2/"

def api_errors(fonk):
    def wrapper(*args,**kwargs):
        try:
            return fonk(*args,**kwargs)
        except requests.exceptions.HTTPError:
            name = args[0] if args else "Unknown"
            print(f"❌ Pokémon '{name}' not found")
        except requests.exceptions.RequestException as err:
            print(f"❌ Request failed: {err}")
        return None
    return wrapper

def no_data(fonk):
    def wrapper(pokemon,*args,**kwargs):
        if not pokemon:
            print("No pokemon found to display.")
            return
        return fonk(*args,**kwargs)
    return wrapper

@api_errors
def get_pokemon_info(name):
    url = f"{base_url}pokemon/{name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def convert_height(height_dm):
    return height_dm * 10  # decimetre → cm

def convert_weight(weight_hg):
    return weight_hg * 0.1  # hectogram → kg

@no_data
def display_pokemon_info(pokemon):
    print(f"\n=== {pokemon['name'].capitalize()} (ID: {pokemon['id']}) ===")
    print(f"Height: {convert_height(pokemon['height'])} cm")
    print(f"Weight: {convert_weight(pokemon['weight'])} kg")

    types = [t['type']['name'].capitalize() for t in pokemon['types']]
    print(f"Types: {', '.join(types)}")

    abilities = [a['ability']['name'].replace('-', ' ').capitalize() for a in pokemon['abilities']]
    print(f"Abilities: {', '.join(abilities)}")

    print("\nBase Stats")
    for stat in pokemon['stats']:
        name = stat['stat']['name'].replace('-', ' ').capitalize()
        value = stat['base_stat']
        print(f"  {name}: {value}")

if __name__ == "__main__":
    name = input("Enter Pokémon name: ").strip()
    info = get_pokemon_info(name)
    if info:
        display_pokemon_info(info)
