from dlc import DLC

def get_dlc(app_id):
    game = DLC(app_id)
    try:
        game.get_response()   
        app_data = game.get_appdata()
        print(f"DLCs for game {game.get_gametitle()}:\n")
        for dlc in app_data:
            print(f'{dlc} = {app_data[dlc]}')
    except:
        print('Could not find game with id: {0}'.format(app_id))

if __name__ == "__main__":
    print("Enter Steam game id:")
    app_id = input()
    get_dlc(app_id)