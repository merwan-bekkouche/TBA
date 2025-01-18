""" Define the Room class."""

from character import Character

class Room:
    """Description des rooms"""

    def __init__(self, room):
        """Define the constructor"""
        self.id = room['id']
        self.name = room['name']
        self.description = room['description']
        self.exits = room['exits']
        self.inventory = set()

    def get_exits(self):
        """Retourne les sorties d'une room"""
        return self.exits

    def get_exits_npc(self):
        """Retourne toutes les exits possibles pour un NPC"""
        exits = []
        for myexit in self.exits:
            if myexit['npcOK']:
                exits.append(myexit)
        return exits

    def get_exit(self, direction):
        """Retourne room in the given direction if it exists."""
        if direction in self.exits.keys():
            return self.exits[direction]
        return None

    def get_exit_string(self):
        """Return a string describing the room's exits."""
        exit_string = "\nQue faire ?"
        for step in self.exits:
            exit_string += f"\n{str(step['id'])}. {step['description']}"
        return exit_string

    def get_inventory(self):
        """Retourne l'inventaire room"""
        if not self.inventory:
            return "\nRien de plus ici."
        inventory_contents = "\nOn voit :"
        for item in self.inventory:
            if isinstance(item, Character):
                inventory_contents += self.red_string(f"\n  - {item}")
            else:
                inventory_contents += f"\n  - {item}"
        return inventory_contents

    def get_characters(self):
        """Retourne les NPC dans la room"""
        npc =[]
        for item in self.inventory:
            if isinstance(item, Character):
                npc.append(item)
        return npc

    def get_fighters(self):
        """Retourne les NPC combatant"""
        npc =[]
        for item in self.inventory:
            if isinstance(item, Character):
                if item.combat:
                    npc.append(item)
        return npc

    def get_thalker(self):
        """Retourne les NPC combatant"""
        for item in self.inventory:
            if isinstance(item, Character):
                if item.msgs:
                    return item
        return None

    def get_long_description(self):
        """Return a long description of this room including exits."""
        return f"\n{self.red_string(self.name)}\n{self.description}\n{self.get_exit_string()}"

    def get_short_description(self):
        """Return a short description of this room."""
        return f"\n{self.red_string(self.name)}\n{self.description}"

    def red_string(self, message):
        """Retourne ue string rouge sur MacOS terminal"""
        return f"\033[91m{message}\033[0m"

    def get_room_temperature(self):
        """ Si une clim et moteur du groupe électro gene temérature dépasse pas 30°"""
        clim_flag = False
        moteur_flag = False
        for item in self.inventory:
            if item.name.lower() == "clim":
                clim_flag = True
            if item.name.lower() == "moteur":
                moteur_flag = True

        if clim_flag and moteur_flag:
            return 30
        return 0

    def print_exits(self):
        """Imprime les exist"""
        print(self.exits)
