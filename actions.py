"""The actions module contains the functions that are called when a command is executed."""

import random
import os
from setup import DEBUG
from character import Character

# Description: The actions module.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables
# and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend un paramètre.\n"


class Actions:
    """ All actions needed to play."""

    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """

        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        direction =direction.upper()
        if direction not in  game.direction:
            print("/n caractère non reconnue")
            return False
        #on passe en maj toutes lettre pour comparer et pouvoir écrire lees direction
        direction=direction[0]
        game.player.move(direction)
        return True


    @staticmethod
    def move_characters(game):
        """ Déplacer NPCs entre les rooms où ils peuvent bouger. """

        #Parcourir toutes les rooms du jeu
        for room in game.rooms:
            #Regarder si NPC dans room
            for npc in room.get_characters():
                #Tester si NPC peut bouger
                if npc.static == 0:
                    #Récuperer toutes les rooms où il peut bouger
                    exits = room.get_exits_npc()
                    if exits:
                        #Choisi une room au hasard
                        random_exit = random.choice(exits)
                        random_room = game.get_room_byid(random_exit['direction'])
                        if DEBUG:
                            print(random_room['name'])
                        random_room.inventory.add(npc)
                        room.inventory.remove(npc)
                        continue
                    print("No exit")

    @staticmethod
    def number(game, list_of_words, number_of_parameters):
        """ Déplacemennt dans une des directions choisies. """

        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Déplace NPCs non statiques
        Actions.move_characters(game)

        choice = list_of_words[0]

        if choice.isdigit() and 1 <= int(choice) <= 9:
            choice = int(choice)
            if not DEBUG:
                os.system('clear')
            return game.player.jump(choice, game)

        return False

    @staticmethod
    def wait(game, list_of_words, number_of_parameters):
        """ Attendre deux heures dans une même lieu """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        if not DEBUG:
            os.system('clear')
        game.player.status.update_time(120)
        return game.player.after_jump(game)

    @staticmethod
    def fightc(game, list_of_words, number_of_parameters):
        """ Continuer combat """

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        npcs = game.player.current_room.get_fighters()
        if npcs:
            for npc in npcs:
                return Actions.fight(game, game.player, npc, npc.combat)
        else:
            print("\nPersonne à combattre !")
            return False

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        os.sys.exit()
        # game.finished = True
        # return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("- " + str(command))
        print()
        return True

    @staticmethod
    def history(game, list_of_words, number_of_parameters):
        """ Affiche l'historique des actions."""

        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        return game.player.get_history()

    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """ Retour room antérieure. """

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        return game.player.back()

    @staticmethod
    def look(game, list_of_words, number_of_parameters):
        """ regarde ce qu'il y a dans la room. """

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        print(game.player.current_room.get_inventory())
        return True


    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """Prendre un objet."""

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        name_item = list_of_words[1].lower()

        count_add_items = 0
        # Use a separate list to collect items to remove
        items_to_remove = []
        current_room_inventory = player.current_room.inventory

        for item in current_room_inventory:

            if isinstance(item, Character):
                continue

            if name_item == item.name.lower() or name_item == "all":
                total_weight = round(player.status.player['weight'] + item.weight, 1)
                max_weight = player.status.player['max_weight'] * player.status.player['duo']
                if  total_weight > max_weight:
                    print(
                        f"Limite de poids atteinte, il faut deposer un objet avant "
                        f"d'en prendre un nouveau ({total_weight} > {max_weight}).\n"
                    )
                    return True

                player.status.player['weight'] = total_weight
                if item.weight == 0:
                    print(f"Vous ne pouvez pas prendre '{item.name}'.")
                    return True
                if item.name.lower() == "eau":
                    player.status.set_water(item.weight)
                else:
                    player.inventory.add(item)
                    items_to_remove.append(item)
                print(f"Vous avez pris : '{item.name}'.")
                count_add_items += 1

        # Now remove the items from the inventory after the iteration
        for item in items_to_remove:
            player.current_room.inventory.remove(item)

        if count_add_items > 0:
            print(f"Vous avez pris {count_add_items} objet(s).\n")
            print( player.status.status_str() )
            return True

        print(f"L'objet '{name_item}' n'est pas dans cet endroit.\n")
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """Saisir un obkjet."""

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        name_item = list_of_words[1].lower().strip()

        item = player.get_item_by_name(name_item)

        if item :
            player.inventory.remove(item)
            player.current_room.inventory.add(item)
            print(f"Vous avez déposé l'objet : '{item.name}'.\n")
        else :
            print(f"Vous ne possedez pas cet objet : '{name_item}'.\n")
        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """Inventaire des objets transportés."""

        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        print( game.player.status.status_str() )
        print(f"\n{game.player.get_inventory()}")
        return True

    @staticmethod
    def use(game, list_of_words, number_of_parameters):
        """Utiliser objet"""

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        item = game.player.get_item_by_name(item_name)

        if item:
            if item.use:
                print( game.player.wrap_string( item.use ) )

                # TEST si HP
                if "25HP" in item.use:
                    game.player.status.set_hp(25)
                if "50HP" in item.use:
                    game.player.status.set_hp(50)

                # Item ddisparaît une fois used
                game.player.inventory.remove(item)
                return True

            print(f"L'objet '{item_name}' n'est pas utilisable.")
            return False
        print(f"Vous ne possédez pas {item_name}.")
        return False


    @staticmethod
    def charge(game, list_of_words, number_of_parameters):
        """Charge beamer. Non utilisé"""

        if len(list_of_words) != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        item_name = list_of_words[1]
        item = game.player.inventory.get(item_name, None)
        print(item_name)

        if item_name in game.player.inventory:
            item.charge(game.player.current_room)
            return True
        print(f"L'objet '{item_name}' ne peut pas être chargé ou n'est pas un Beamer.")
        return False


    @staticmethod
    def talk_one(game, list_of_words, number_of_parameters):
        """Parler à un NPC"""

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        npc_name = list_of_words[1].lower().strip()

        for item in player.current_room.inventory :
            if npc_name == item.name.lower() :
                msg = item.get_msg()
                if "|" in msg:
                    #Combat mode
                    (mode,texte)=msg.split("|")
                    print(texte)
                    return Actions.fight(game,player,item,mode)
                if "oui/non" in msg:
                    print(msg.replace("oui/non","").strip())
                    reponse = input("oui ou non >")
                    if reponse.lower() == "oui":
                        print("Je viens avec toi, mes HP s'ajoutent aux tiens")
                        game.player.status.set_hp(item.hp)
                        game.player.status.player['duo'] = 2
                        game.player.current_room.inventory.remove(item)
                else:
                    print(msg)
                return True

        print(f"\nLe NPC '{npc_name}' n'est pas à cet endroit.\n")
        return False


    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        """Parler à un NPC"""

        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        npc = player.current_room.get_thalker()

        if npc:
            msg = npc.get_msg()
            if "|" in msg:
                #Combat mode
                (mode,texte)=msg.split("|")
                print(texte)
                return Actions.fight(game,player,npc,mode)
            if "oui/non" in msg:
                print(msg.replace("oui/non","").strip())
                reponse = input("oui ou non >")
                if reponse.lower() == "oui":
                    print("Je viens avec toi, mes HP s'ajoutent aux tiens")
                    game.player.status.set_hp(npc.hp)
                    game.player.status.player['duo'] = 2
                    game.player.current_room.inventory.remove(npc)
            else:
                print(msg)
            return True

        print("Personne à qui parler.\n")
        return False


    @staticmethod
    def fight(game, player, npc, mode):
        """Combat avec un NPC"""

        #HP perdus player
        if mode == "MainsNues":
            npc_damage_factor = 0.5
        else:
            npc_damage_factor = 1.5

        dice = random.randint(0, 5)
        print(f"NPC dice: {dice}")
        player_damage = round (npc.hp * npc_damage_factor * dice/10) * -1
        player.status.set_hp(player_damage)

        if player.status.get_hp() <= 0:
            print(f"Vous perdez {abs(player_damage)}HP.")
            return Actions.dead_player(game)

        #HP perdus NPC

        if player.armed():
            player_damage_factor = 1.5
        else:
            player_damage_factor = 0.5

        dice = random.randint(1, 6)
        print(f"Player dice: {dice}")
        npc_damage = round (player.status.get_hp() * player_damage_factor * dice/10)
        npc.hp -= npc_damage

        if npc.hp<=0:
            Actions.killed_npc(game, npc)
            print(f"Vous perdez {abs(player_damage)}HP.")
        else:
            print(f"Vous perdez {abs(player_damage)}HP, {npc.name} perd {abs(npc_damage)}HP")
        return True


    @staticmethod
    def killed_npc(game, killed):
        """ NPC tué."""

        for npc in game.player.current_room.get_characters():
            if npc.name == killed.name:
                game.player.current_room.inventory.remove(npc)
                print(f"{killed.name} est mort.")
                return True
        return False

    @staticmethod
    def dead_player(game):
        """ Joueur mort. """
        print( game.player.current_room.red_string("Vous êtes mort !!!") )
        return Actions.quit(game, ["quit"], 0)
