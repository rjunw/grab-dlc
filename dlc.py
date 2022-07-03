import requests 

class DLC:
    """
    A simple structure to hold DLC <app_id> and <app_description>
    """
    def __init__(self, game_id):
        self.game_id = game_id # passed in by console args
        self.app_data = {}
    
    def get_HTML(self):
        # GET request to dlc page
        response = requests.get("https://store.steampowered.com/dlc/{0}/".format(self.game_id))
        return response 
    
    def get_appdata(self):
        # parse using the steam store recommendations table
        return self.app_data
