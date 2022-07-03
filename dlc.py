import requests 

class DLC:
    """
    A simple structure to hold DLC <app_id> and <app_description>
    """
    def __init__(self, game_id):
        self.game_id = game_id # passed in by console args
        self.game_title = None
        self.app_data = {}
        self.response = None 
    
    def get_response(self):
        """
        Performs a GET on a steam dlc page for a given <app_id> of game
        """
        try:
            head_text = 'Steam DLC Page: '
            title = requests.get("https://store.steampowered.com/dlc/{0}".format(self.game_id)).text

            if title.find('Welcome to Steam') != -1:
                return -1

            self.game_title = title[title.find(head_text) + len(head_text): title.find('</title>')]
            title = self.game_title.replace(' ', '_')
            # makes request for up to 2^16 dlc items
            self.response = requests.get("https://store.steampowered.com/dlc/{0}/{1}/ajaxgetfilteredrecommendations/?query=&start=0&count=65536&dynamic_data=&tagids=&sort=newreleases&app_types=&curations=&reset=false".format(self.game_id, title))
            return self.response 
        except:
            print("Could parse with game id {0}".format(self.game_id))
            return -1

    def get_HTML(self):
        """
        Returns the raw HTML response
        """
        return self.response.text
    
    def get_gametitle(self):
        return self.game_title
    
    def get_appdata(self):
        """
        Parse steam dlc page raw HTML for appdata
        """
        raw = self.get_HTML()
        try:
            # find recommendations table on steam DLC page
            rec_rows = raw
            dlc_str = "data-ds-appid="
            dlc_desc = "color_created\'>"

            # parse out appdata
            while True:
                # <app_id>
                if rec_rows.find(dlc_str) == -1:
                    break
                rec_rows = rec_rows[rec_rows.find(dlc_str):]
                rec_rows = rec_rows[len(dlc_str) + 2:]
                app_id = rec_rows[:rec_rows.find('\\')]
                
                # <app_desc>
                rec_rows = rec_rows[rec_rows.find(dlc_desc) + len(dlc_desc):]
                app_desc = rec_rows[:rec_rows.find('<')]
                app_desc = app_desc.replace('&amp;', '&') # replace HTML interpretation of &'s

                self.app_data[app_id] = app_desc

                rec_rows = rec_rows[rec_rows.find('<') + 1:]

            
            return self.app_data

        except:
            print("Could not parse HTML")
            return None
