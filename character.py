""" NPCs module"""

class Character():
    """ Classe NPCs"""

    def __init__(self, character):
        """Initialisation NPC"""

        self.name = character['name']
        self.msgs = character['msgs']
        self.msgs_index = 0
        self.description = character['description']
        self.hp = character['hp']
        self.static = character['static']
        self.combat = character['combat']

    def __str__(self):
        """ Retourne description NPC"""

        return f"{self.name} : {self.description}"

    def get_msg(self):
        """ Retourne phrase dans le dialoguie avec NPC"""

        if self.msgs_index >= len(self.msgs):
            return "Plus rien à dire"

        message = self.msgs[self.msgs_index].strip()

        if self.msgs_index + 1 == len(self.msgs):
            if self.combat:
                # Dernier message et combat
                return str(self.combat)+"|"+message

        self.msgs_index += 1
        return message
