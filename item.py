"""Item module"""

class Item:
    """Item Class"""


    def __init__(self, item):
        """Define the constructor."""

        self.name = item['name']
        self.description = item['description']
        self.weight = item['weight']
        self.use = item['use']


    def __str__(self):
        """The string representation of the command."""
        return  f"{self.name} : {self.description} ({self.weight} kg)"

    def myprint(self):
        """Print for lynter"""
        print(self.name)
