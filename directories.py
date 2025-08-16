import requests, json
import os            

def ReturnJson(theme):

    theme_url = f"https://raw.githubusercontent.com/avalon60/ctk_theme_builder/develop/user_themes/{theme}"
    theme_dir = f"assets/user_themes/temp_{theme}"

    if os.path.exists(theme_dir):
        return theme_dir
    else :
        response = requests.get(theme_url)
        response.raise_for_status()

        # return response.json()
    
        with open(theme_dir, "w") as f:
            json.dump(response.json(), f, indent=4)
        return theme_dir
        


ThemeOptions = {
    "Blue": "blue", 
    "Dark Blue": "dark-blue", 
    "Green": "green",
    # "Anthracite": ReturnJson("Anthracite.json"),
    # "Cobalt": ReturnJson("Cobalt.json"),
    # "DaynNight": ReturnJson("DaynNight.json"),
    # "GhostTrain": ReturnJson("GhostTrain.json"),
    # "Greengage": ReturnJson("Greengage.json"),
    # "GreyGhost": ReturnJson("GreyGhost.json"),
    # "Hades": ReturnJson("Hades.json"),
    # "Harlequin": ReturnJson("Harlequin.json"),
    # "MoonlitSky": ReturnJson("MoonlitSky.json"),
    # "NeonBanana": ReturnJson("NeonBanana.json"),
    # "NightTrain": ReturnJson("NightTrain.json"),
    # "Oceanix": ReturnJson("Oceanix.json"),
    # "Sweetkind": ReturnJson("Sweetkind.json"),
    # "BlueTestCard": ReturnJson("TestCard.json"),
    # "TrojanBlue": ReturnJson("TrojanBlue.json")
}


WindowsFonts = {
    'Arial'   :   'C:\Windows\Fonts\\arial.ttf',
    'Comic'   :   'C:\Windows\Fonts\comic.ttf',
    'Impact'   :   'C:\Windows\Fonts\impact.ttf',
    'Monbaiti'   :   'C:\Windows\Fonts\monbaiti.ttf',
    'Segoesc'   :   'C:\Windows\Fonts\segoesc.ttf',
    'Simfang' :  'C:\Windows\Fonts\simfang.ttf',
    'Simhei' : 'C:\Windows\Fonts\simhei.ttf',
    'Simkai' : 'C:\Windows\Fonts\simkai.ttf',
    'Tahoma'   :   'C:\Windows\Fonts\\tahoma.ttf',
    'Taile'   :   'C:\Windows\Fonts\\taile.ttf',
    'Times'   :   'C:\Windows\Fonts\\times.ttf',
}

