# Define the Room class.

class Room:
    """
    This class represents a room in a text-based adventure game. A room has a name, a description, and possible exits leading to other rooms.

    Attributes:
        name (str): The name of the room.
        description (str): A brief description of the room.
        exits (dict): A dictionary where keys are directions (e.g., 'north', 'east') and values are the corresponding Room objects.

    Methods:
        __init__(self, name, description): The constructor.
        get_exit(self, direction): Returns the room in the specified direction if it exists.
        get_exit_string(self): Returns a string listing all available exits.
        get_long_description(self): Returns a detailed description of the room, including its exits.
        """
    # Define the constructor. 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
    
    # Define the get_exit method.
    def get_exit(self, direction):

        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None
    
    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: " 
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes {self.description}\n\n{self.get_exit_string()}\n"
