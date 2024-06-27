import directories
import toml
import pokemon
import player

# Acceptable Starters
acceptableStarters = {
    "BULBASAUR", "CHARMANDER", "SQUIRTLE", "PIKACHU"
}

"""
Add a pokemon to a players party
If the party is full, the pokemon should instead be added to their pc

Args:
    username (string): The username of the player
    pokemon (A Pokemon class instance defined in pokemon.py)
"""
def addPartyMember(username: str, pokemon: pokemon.Pokemon):
    filename = f"{directories.players_directory}{username}.toml"
    data = player.loadSave(username)
    if data is not None:
        # Check for an open slot and fill it
        # TODO If no open slot is found add it to the pc
        playerParty = player.getParty(data)
        for partySlot in playerParty:
            if partySlot.get("name", "") == "":
                pokemon.loadPokemonTOML(partySlot)
                break
        player.saveData(username, data)