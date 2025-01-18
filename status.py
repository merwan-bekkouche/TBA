""" Player Status module"""

import sys

class PlayerStatus():
    """ Additional player parameters."""

    def __init__(self, speed_factor=20):
        """
        Initialise les variable du player.
        speed_factor: À chaque déplacement ajoute speed_facor au temps en minutees.
        Plus valeur élevée plus le jeu est difficile.
        """

        # Initialisation des variables

        self.temperature = {
            'now': 28,      # Température
            'min': 28,      # Début de journée
            'max': 35,      # max atteint après max_after heures
            'hplost': 32,   # Température à partir de la quelle on perd des points de vie
            'max_after': 6  # Temparture max au bout de six heures
        }

        self.gtime = {
            'speed_factor': speed_factor,
            'now': 0,       # Minutes dans le jeu
            'start': 6,     # Heure début jeu
            'start_minutes': 0, # Minute de début du jeu
            'victory': 18,  # Heure de victoire (faut être encore vivant)
            'delta_time': 1 # Nombre de speed_factor entre deux actions
        }

        self.player = {
            'hp': 100,
            'water': 0,
            'weight': 0,
            'max_weight': 30, #Kg
            'xp': 0,
            'duo': 1 #2 pour en équipe
        }

        self.gtime['now'] = self.gtime['start']  * 60
        self.gtime['start_minutes'] = self.gtime['now']


    def update_time(self, minutes=0):
        """Met à jour le temps en fonction du mode choisi."""
        if minutes>0:
            self.gtime['delta_time'] = minutes // self.gtime['speed_factor']
            self.gtime['now'] += minutes
        else:
            # En minutes
            self.gtime['delta_time'] = 1
            self.gtime['now'] += self.gtime['speed_factor']

        # Quondition de victoire
        if self.gtime['now'] >= self.gtime['victory'] * 60:
            self.player['xp'] += 500
            print( self.yellow_string(f"VICTOIRE!!! {self.player['xp']}XP/2000XP") )
            sys.exit()


    def set_hp(self, value):
        """Ajoute/soustrait des hp"""
        self.player['hp'] += value

    def get_hp(self):
        """Retourne les hp du player"""
        return self.player['hp']

    def update_hp(self):
        """ Actualise les HPs"""

        # Condition pour commencer à perdre HP
        if self.temperature['now'] > self.temperature['hplost']:

            if self.player['water'] > 0:
                self.player['hp'] -= 10 * self.gtime['delta_time'] * self.player['duo']
            else:
                self.player['hp'] -= 20 * self.gtime['delta_time'] * self.player['duo']


    def update_water(self):
        """ Actualise l'eau"""
        self.player['water'] -= 0.1 * self.player['duo'] * self.gtime['delta_time']


    def updade_temperature(self, room_temperature=0):
        """Met à jour la température en fonction de l'heure"""

        external_temperature = round(
            self.temperature['min'] +
            (self.temperature['max'] - self.temperature['min']) *
            (self.gtime['now'] - self.gtime['start_minutes']) /
            (self.temperature['max_after'] * 60),
            1
        )

        # Ne pas dépasser le max possible
        if self.gtime['now'] > self.gtime['start_minutes'] + self.temperature['max_after'] * 60:
            external_temperature = self.temperature['max']

        if room_temperature >0:
            self.temperature['now'] = min(room_temperature, external_temperature)
        else:
            self.temperature['now'] = external_temperature


    def get_time(self):
        """Retourne l'heure actuelle du jeu sous forme de chaîne 'HH:MM'."""
        hours = self.gtime['now'] // 60
        minutes = self.gtime['now'] % 60
        return f"{hours:02}:{minutes:02}"

    def get_and_update(self, room_temperature=0):
        """ Update toutes la valeurs et retourne le ststus du joueur"""
        status_str = self.status_str()
        self.updade_temperature(room_temperature)
        self.update_hp()
        self.update_water()
        self.update_time()
        return status_str

    def status_str(self):
        """Fabique le status"""
        return self.yellow_string(
            f"\n{self.get_time()} {self.temperature['now']}°C 100% humidité "
            f"{self.player['hp']}HP {round(self.player['water'], 1)}l {self.player['weight']}kg/"
            f"{round(self.player['max_weight'] * self.player['duo'])} {self.player['xp']}XP"
        )

    def set_water(self,litres=0):
        """ Initialise eau"""
        self.player['water'] += round(litres,1)

    def yellow_string(self, message):
        """Crée uns tring jaune sur MacOS"""
        return f"\033[93m{message}\033[0m"
