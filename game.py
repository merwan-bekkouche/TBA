"""Description: Game class"""

import os
import readline
from obsidian_parser import Parser
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from character import Character


class Game:
    """Classe principale"""

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.items = []
        self.characters = []

        # Parsing Obsidian Canvas
        level1 = os.path.join("Jeux", "LVL1", "00MapLVL1.canvas")
        self.parser = Parser("obsidian", level1)

    def setup(self):
        """Initialisation"""

        # Setup commands
        # self.direction= set(["N","NORD","OUEST","O","S","SUD","E","EST",'U',"UP",'D',"DOWN"])
        self.commands["help"] = Command("help", ": afficher cette aide", Actions.help, 0)
        self.commands["quit"] = Command("quit", ": quitter le jeu", Actions.quit, 0)
        # go = Command("go", ": se déplacer dans une direction (N, E, S, O)", Actions.go, 1)
        # self.commands["go"] = go
        self.commands["back"]= Command(
            "back",": permet de retourner dans la salle précédente",Actions.back,0
        )
        self.commands["history"]= Command(
            "history",": obtenir l'historique du parcours effectué",Actions.history,0
        )
        self.commands["look"]= Command(
            "look",": regarder autour de vous",Actions.look,0
        )
        self.commands["take"]= Command(
            "take",": prendre un objet (take all pour tout prendre)",Actions.take,1
        )
        self.commands["drop"]= Command("drop",": déposer un objet",Actions.drop,1)
        self.commands["check"]= Command("check",": vérifier son inventaire",Actions.check,0)
        self.commands["talk"]= Command("talk",": parler à un NPC",Actions.talk,0)
        self.commands["use"]= Command("use",": utiliser un objet",Actions.use,1)
        self.commands["wait"]= Command("wait",": attendre 2 heures sans bouger",Actions.wait,0)
        self.commands["fight"]= Command("fight",": continuer combat",Actions.fightc,0)

        self.commands["1"]= Command("1", ": Effectuer action 1", Actions.number, 0)
        self.commands["2"]= Command("2", ": Effectuer action 2", Actions.number, 0)
        self.commands["3"]= Command("3", ": Effectuer action 3", Actions.number, 0)
        self.commands["4"]= Command("4", ": Effectuer action 4", Actions.number, 0)
        self.commands["5"]= Command("5", ": Effectuer action 5", Actions.number, 0)

        # Print the welcome message
        self.player = Player(input("\nEntrez votre nom: "))

        # Setup rooms
        for room in self.parser.get_rooms():
            self.rooms.append(Room(room))
            if room['items']:
                for item in room['items']:
                    self.items.append(Item(item))
                    self.rooms[-1].inventory.add(self.items[-1])

            if room['characters']:
                for character in room['characters']:
                    self.characters.append(Character(character))
                    self.rooms[-1].inventory.add(self.characters[-1])

            # Setup player and starting room
            if self.parser.get_start_room() == room['id']:
                self.player.current_room = self.rooms[-1]


    def play(self):
        """Play the game"""

        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        readline.set_history_length(10)
        while not self.finished:
            # Get the command from the player
            cmd = input("> ")
            # Process cmd
            self.process_command(cmd.lower())

    def process_command(self, command_string):
        """Process the command entered by the player"""

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        if command_word not in self.commands:
            print("!!!Commande inconnue!!!")
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)


    def print_welcome(self):
        """Print the welcome message"""

        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        self.player.print_room()


    def get_room_byid(self, room_id):
        """Retourne la room correspondant à un room_id (fichier Markdown)"""

        for room in self.rooms:
            if room_id == room.id:
                return room
        return None


def main():
    """Create a game object and play the game"""
    os.system('clear')
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
