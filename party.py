import directories
import toml
import pokemon

"""
Add a pokemon to a players party
If the party is full, the pokemon should instead be added to their pc

Args:
    username (string): The username of the player
    pokemon (A Pokemon class instance defined in pokemon.py)
"""
def addPartyMember(username: str, pokemon: pokemon.Pokemon):
    filename = f"{directories.players_directory}{username}.toml"
    
    # Load the existing player save file
    with open(filename, 'r') as file:
        data = toml.load(file)
    
    # Check for an open slot and fill it
    # TODO If no open slot is found add it to the pc
    for partySlot in data.get("pokemon", []):
         if partySlot.get("name", "") == "":
              pokemon.loadPokemonTOML(partySlot)
              break

    # Write the updated data back to the TOML file
    with open(filename, 'w') as file:
        toml.dump(data, file)