"""Player module"""

import os
import textwrap
from status import PlayerStatus
from setup import DEBUG
from actions import Actions

class Player:
    """Define the Player class."""

    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.history = []
        self.current_room = None
        self.inventory = set()

        # Game status (time, temperature…)
        self.status = PlayerStatus()

    def move(self, direction):
        """Define the move method."""
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]
        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        # Set the current room to the next room.
        self.history.append(self.current_room)
        self.current_room = next_room
        print(self.current_room.get_long_description())
        self.get_history()
        return True

    def jump(self, choice, game):
        """Arrive dans la pièce choise"""
        # Récupérer toutes les sorties de room courante
        exits = self.current_room.get_exits()
        # Parcourir toutes les sorties de la room
        for myexit in exits:
            if myexit["id"] == choice:
                # Exist correspondant au choice trouvée
                next_room_id = myexit["direction"]
                # Parcourir toute les rooms pour trouver celle avec le bon ID
                for room in game.rooms:
                    if room.id == next_room_id:

                        #Increment XPs
                        if myexit['xp']>0:
                            print(f"Vous gagnez {myexit['xp']}XP !!!\n")
                            self.status.player['xp'] += myexit['xp']
                            myexit['xp'] =0

                        # Room trouvée
                        self.history.append(game.player.current_room)
                        self.current_room = room

                        return self.after_jump(game)

        print(f"\nAucune sortie pour le numéro {choice} !\n")
        return False


    def after_jump(self, game):
        """Finir le jump"""

        self.print_room_start()

        # Epuisement du player
        if self.status.get_hp() <= 0:
            return Actions.dead_player(game)

        # Combat automatique éventuel
        for npc in game.player.current_room.get_characters():
            if npc.combat and not npc.msgs:
                Actions.fight(game, game.player, npc, npc.combat)

        self.print_room_end()

        return True


    def get_history(self):
        """Retoure les lieux visités"""

        if len(self.history) >= 1:
            print("\nVous avez déjà visité les pièces suivantes:")
            for room in self.history:  # Exclut la pièce actuelle de l'historique affiché
                print(f"\t- {room.name}")
        else:
            print("\nVous n'avez visité aucune autre pièce.")
        return True


    def back(self):
        """Define the back method"""
        if len(self.history) >= 1:
            # Set the current room to the previous room
            self.current_room = self.history.pop()

            if not DEBUG:
                os.system('clear')

            self.print_room()
            self.get_history()
            return True
        print("\nVous ne pouvez pas revenir en arrière !\n")
        return False

    def get_inventory(self):
        """retourne inventaire"""

        if self.inventory:
            inventory_contents = "Vous disposez des items suivants :"
            inventory_contents += "\n  - " + "\n  - ".join(str(item) for item in self.inventory)
        else:
            inventory_contents = "\nAucun item disponible."
        return inventory_contents

    def get_item_by_name(self, item_name):
        """Retourne le l'objet name"""

        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def armed(self):
        """Player est-il armé"""
        for item in self.inventory:
            if item.name.lower() == "Fusil" or item.name.lower() == "Automatique" :
                return True
        return False

    def print_room(self):
        """Afficher description room"""
        print( self.status.get_and_update( self.current_room.get_room_temperature() ) )
        print( self.get_description() )


    def print_room_start(self):
        """Afficher description room"""
        print( self.status.get_and_update( self.current_room.get_room_temperature() ) )
        print( self.wrap_string(self.current_room.get_short_description()) )

    def print_room_end(self):
        """Afficher description room"""
        print( self.wrap_string(self.current_room.get_exit_string()) )

    def get_description(self):
        """Retourne description room"""
        return self.wrap_string(self.current_room.get_long_description())

    def wrap_string(self, content, width=60):
        """Affiche de façon lisible sur terminal."""

        # Diviser le contenu en lignes
        lines = content.splitlines()

        wrapped_lines = []
        for line in lines:
            wrapped_lines.append(textwrap.fill(line, width=width) if line.strip() else "")

        # Joindre les lignes traitées avec des sauts de ligne
        wrapped_text = "\n".join(wrapped_lines)
        return wrapped_text
