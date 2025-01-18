""" Parse Obsidian Canvas"""

import json
import os
import re

class Parser:
    """ Parser class. """

    # Constructor
    def __init__(self, root, canvas_path):
        self.root = root
        self.steps = []
        self.parse_game_structure(canvas_path) #remplit steps
        self.start_room = self.find_starting_node(canvas_path)

    def get_start_room(self):
        """ Retourne la room de départ dans un Canvas (fichier MD avec tag #start)"""
        return self.start_room

    def read_json(self, file_path):
        """
        Lit un fichier JSON et renvoie son contenu sous forme d'objet Python.
        :param file_path: Chemin du fichier JSON à lire
        :return: Données JSON sous forme d'objet Python (généralement un dictionnaire ou une liste)
        """
        path = os.path.normpath(os.path.join(self.root, file_path))
        with open( path , 'r', encoding='utf-8') as file:
            return json.load(file)
        return None

    def read_markdown(self, file_path):
        """ retourne contenu d'un fichier MD."""
        path = os.path.normpath(os.path.join(self.root, file_path))
        with open( path, 'r', encoding='utf-8') as file:
            return file.read()
        return None

    def find_starting_node(self, canvas_path):
        """Trouver le nœud de départ avec le tag #start."""

        data = self.read_json( canvas_path )

        nodes = {node['id']: node for node in data['nodes']}
        for node in nodes.values():
            file_path = node.get('file')

            if file_path:
                content = self.read_markdown(file_path)
                if '#start' in content:
                    return file_path
        return None

    def parse_game_structure(self, map_path, parsed_maps=None):
        """Analyse la structure du jeu"""

        # Definir liste des maps traitées
        if parsed_maps is None:
            parsed_maps = set()
        # Marquer la map courante comme analysée
        parsed_maps.add(map_path)

        # Lire la carte principale
        data = self.read_json(map_path)

        nodes = {node['id']: node for node in data['nodes']}
        # print(nodes)

        for edge in data['edges']:

            id_from_node = edge['fromNode']
            from_node = nodes[id_from_node]

            id_to_node = edge['toNode']
            to_node = nodes[id_to_node]

            if from_node['type'] == 'file':
                from_file = from_node['file'] #récupère le nom du fichier
            else:
                # print("Autre type interdit")
                continue

            if to_node['type'] == 'file':
                to_file = to_node['file']
            else:
                # print("Autre type interdit")
                continue

            # Si un nœud pointe vers une nouvelle carte et qu'elle n'a pas été analysée
            if to_file.endswith('.canvas') and to_file not in parsed_maps:
                # Analyser récursivement la nouvelle carte
                self.parse_game_structure(to_file, parsed_maps)
                to_file = self.find_starting_node(to_file) #cherche le starting node du canvas

            # Ajouter l'étape courante à la liste des liaisons
            step = {
                'from': from_file,
                'to': to_file,
                'label': edge.get('label', 'unknown'),
                # 'direction': edge.get('toSide', 'unknown')
            }
            # print("step",step)
            self.steps.append(step)
        return True

    def get_md(self, md_file):
        """Analyse fichier MD."""

        content = self.read_markdown(md_file)
        text = ""
        title = "No title"
        items = []
        characters = []

        for line in content.split('\n'):
            if line.strip().startswith('# '):
                title = line.strip().replace('# ', '')
            elif line.strip().startswith('* '):
                # Traiter les lignes d'items
                parts = line.strip().replace('* ', '').split('|')
                if parts[0].strip() == "NPC" and len(parts)>4: # C'est un NPC
                    if parts[5].strip().lower() == "none":
                        combat = ""
                    else:
                        combat = parts[5].strip()
                    characters.append({
                        'name': parts[1].strip(),
                        'description': parts[2].strip(),
                        'hp': int(parts[3].strip()),
                        'static': int(parts[4].strip()),
                        'combat': combat,
                        # Prend toutes les parts restantes à partir de l'index 4
                        'msgs': [part.strip() for part in parts[6:]]
                    })
                elif len(parts) >= 3:  # Vérifier que nous avons bien 3 ou 4 parties
                    if len(parts) == 4:
                        use = parts[3].strip()
                    else:
                        use = ""
                    items.append({
                        'name': parts[0].strip(),
                        'description': parts[1].strip(),
                        'weight': float(parts[2].strip()),
                        'use': use
                    })
            elif '#start' in line.strip().lower():
                continue
            else:
                text += line + '\n'

        # Supprimme saut de lignes en trop
        text = re.sub(r'\n{3,}', '\n\n', text)

        return (title,text,items,characters)

    def get_rooms(self):
        """Récupère toutes les rooms."""

        rooms = []

        # Liste des fichiers room
        md_files = set()
        for edge in self.steps:
            if edge['from'].endswith('.md'):
                md_files.add(edge['from'])
            if edge['to'].endswith('.md'):
                md_files.add(edge['to'])

        # Lire tous les fichiers Markdown
        for md_file in md_files:
            (title,text,items,characters) = self.get_md(md_file)

            exits = []

            i = 1
            for edge in self.steps:
                # On cherche toutes les rooms vers lesquelles pointe md_file
                if edge['from'] == md_file:

                    npc_ok=False
                    if "(NPC)" in edge['label']:
                        npc_ok=True

                    if "(XP)" in edge['label']:
                        xp=500
                    else:
                        xp=0

                    # Supprime (NPC) et/ou (XP) si présents
                    edge_name = edge['label'].replace("(NPC)","").replace("(XP)","").strip()

                    exits.append({"id" : i,
                        "description" : edge_name,
                        "direction": edge['to'],
                        "npcOK": npc_ok,
                        "xp": xp})
                    i += 1

            room = {
                'id': md_file,
                'name': title,
                'description': text,
                'exits': exits,
                'items': items,
                'characters': characters,
            }
            rooms.append(room)

        return rooms
